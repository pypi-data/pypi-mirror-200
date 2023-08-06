# #ifdef SERVER
from pathlib import Path

from testmon_dev.db import DB

SERVER_DATA_VERSION = 3


def copy_suite_execution(con, from_id, to_id):
    con.execute(
        "UPDATE suite_execution SET parent_id = ? WHERE id = ?",
        (from_id, to_id),
    )

    cursor = con.execute(
        "    SELECT id, test_name, duration, failed "
        "    FROM test_execution WHERE suite_execution_id = ?",
        (from_id,),
    )

    while test_execution := cursor.fetchone():
        new_test_execution_id = con.execute(
            "INSERT INTO test_execution (test_name, duration, failed, suite_execution_id) "
            "VALUES (?, ?, ?, ?)",
            (test_execution[1], test_execution[2], test_execution[3], to_id),
        ).lastrowid
        con.execute(
            "INSERT INTO test_execution_file_fp (test_execution_id, fingerprint_id) "
            "SELECT ?, fingerprint_id FROM test_execution_file_fp WHERE test_execution_id = ?",
            (new_test_execution_id, test_execution[0]),
        )

    con.execute(
        "UPDATE test_execution set forced = NULL WHERE suite_execution_id = ?",
        [to_id],
    )


class ServerDatabase(DB):
    def __init__(
        self,
        datafile=".serverdata",
    ):
        Path(datafile).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(
            datafile=datafile,
        )

    def version_compatibility(self):
        return SERVER_DATA_VERSION

    def _test_execution_fk_column(self) -> str:
        return "suite_execution_id"

    def _test_execution_fk_table(self) -> str:
        return "suite_execution"

    def init_tables(self):
        connection = self.con
        super().init_tables()
        connection.executescript(self.create_suite_execution_statement())

    def create_suite_execution_statement(self) -> str:  # pylint: disable=invalid-name
        return """
                CREATE TABLE suite_execution (
                id INTEGER PRIMARY KEY ASC,
                environment_id INTEGER,
                duration FLOAT,
                parent_id INTEGER,
                git_head_0 TEXT,
                git_head_1 TEXT,
                tm_client_version TEXT,
                tm_server_version TEXT,
                FOREIGN KEY(environment_id) REFERENCES environment(id)
            );"""

    def fetch_unknown_files(self, files_checksums, exec_id) -> []:
        self.con.executemany(
            "INSERT INTO temp_files_checksums VALUES (?, ?, ?)",
            [(exec_id, file, checksum) for file, checksum in files_checksums.items()],
        )
        (environment_name, system_packages, python_version,) = self.con.execute(
            """SELECT 
                    e.environment_name, 
                    e.system_packages, 
                    e.python_version 
                FROM
                    suite_execution se, environment e
                WHERE se.id = ? AND 
                      se.environment_id = e.id
        """,
            (exec_id,),
        ).fetchone()
        by_count = dict(  # overwrite items with repeated count
            self.con.execute(
                """
            SELECT
                count(tfc.checksum),
                te.suite_execution_id
            FROM
                test_execution te,
                test_execution_file_fp te_ffp,
                file_fp ffp,
                suite_execution se,
                environment e
            LEFT OUTER JOIN
                temp_files_checksums tfc
            ON
                ffp.filename = tfc.filename AND
                ffp.checksum = tfc.checksum AND
                tfc.exec_id = ?
            WHERE
                se.id = te.suite_execution_id AND
                te.id = te_ffp.test_execution_id AND
                te_ffp.fingerprint_id = ffp.id AND
                se.environment_id = e.id AND
                e.environment_name = ? AND
                e.system_packages = ? AND
                e.python_version = ?
            GROUP BY te.suite_execution_id
            ORDER BY count(tfc.checksum) ASC,
                     te.suite_execution_id ASC
            """,
                (exec_id, environment_name, system_packages, python_version),
            ).fetchmany(100),
        )

        if by_count:
            best_suite_execution_id = list(by_count.values())[-1]
            if best_suite_execution_id != exec_id:
                self.con.execute(
                    "UPDATE suite_execution SET parent_id = ? WHERE id = ?",
                    (best_suite_execution_id, exec_id),
                )
        else:
            best_suite_execution_id = exec_id

        return super().fetch_unknown_files(files_checksums, best_suite_execution_id)

    def initiate_execution(  # pylint: disable= R0913 W0613
        self,
        environment_name: str,
        system_packages: str,
        python_version: str,
    ):
        environment_id, packages_changed = self.fetch_or_create_environment(
            environment_name, system_packages, python_version
        )
        suite_execution_id = self.fetch_or_create_suite_execution(environment_id)
        return {
            "exec_id": suite_execution_id,
            "filenames": list(self.all_filenames()),
            "packages_changed": packages_changed,
        }

    def fetch_or_create_suite_execution(self, environment_id: "int") -> int:
        with self.con as con:
            cursor = con.cursor()
            cursor.execute(
                """
                  INSERT INTO suite_execution
                  (environment_id)
                  VALUES (?)
                  """,
                (environment_id,),
            )
            suite_execution_id = cursor.lastrowid
        return suite_execution_id

    def finish_execution(self, exec_id, duration=None, select=True):
        with self.con as con:
            con.execute(
                "UPDATE suite_execution SET duration = ? WHERE id = ?",
                (duration, exec_id),
            )

    def delete_filenames(self, con):
        pass

    def determine_tests(self, exec_id, files_mhashes):
        (parent_id,) = self.con.execute(
            "SELECT parent_id FROM suite_execution WHERE id = ?", (exec_id,)
        ).fetchone()

        if parent_id:
            env_score = 1
        else:
            env_score, parent_id = self._best_environment(exec_id)

        if parent_id != exec_id:
            with self.con as con:
                copy_suite_execution(con, parent_id, exec_id)

        determined_test = super().determine_tests(exec_id, files_mhashes)
        determined_test["env_score"] = env_score

        return determined_test

    def _best_environment(self, exec_id):
        (environment_name, system_packages, python_version,) = self.con.execute(
            """SELECT 
                    e.environment_name, 
                    e.system_packages, 
                    e.python_version
                FROM
                    suite_execution se, environment e
                WHERE se.id = ? AND 
                      se.environment_id = e.id
        """,
            (exec_id,),
        ).fetchone()
        env_score = None
        executions = self.con.execute(
            """
        SELECT
            count(tfc.checksum),
            te.suite_execution_id,
            e.environment_name,
            e.system_packages,
            e.python_version
        FROM
            test_execution te,
            test_execution_file_fp te_ffp,
            file_fp ffp,
            suite_execution se,
            environment e
        LEFT OUTER JOIN
            temp_files_checksums tfc
        ON
            ffp.filename = tfc.filename AND
            ffp.checksum = tfc.checksum AND
            tfc.exec_id = ?
        WHERE
            se.id = te.suite_execution_id AND
            te.id = te_ffp.test_execution_id AND
            te_ffp.fingerprint_id = ffp.id AND
            se.environment_id = e.id
        GROUP BY te.suite_execution_id,
                    e.environment_name,
                    e.system_packages,
                    e.python_version
        ORDER BY count(tfc.checksum) ASC,
                 te.suite_execution_id ASC
        """,
            (exec_id,),
        ).fetchmany(100)
        if executions:
            executions = [
                list(execution)
                + [
                    sum(
                        [
                            (execution[2] == environment_name) * 0.2,
                            (execution[3] == system_packages) * 0.2,
                            (execution[4] == python_version) * 0.1,
                        ]
                    )
                ]
                for execution in executions
            ]
            executions.sort(key=lambda x: x[5], reverse=True)
            parent_id = executions[0][1]
            env_score = executions[0][5]
            return env_score, parent_id
        return None, None


# #endif
