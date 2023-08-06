#!/usr/bin/env python3
# pylint: disable-all

"""Manage revisioned cached files on S3

Copyright (c) 2020-present Eduardo Naufel Schettino

USAGE:

./tmnet.py linux-py39

./tmnet.py linux-py39 --upload
PYTEST_DONT_REWRITE
"""

import json
import os
import subprocess
import configparser
import argparse

from boto3 import session
from _pytest.config.findpaths import locate_config
import botocore

from .testmon_core import get_data_file_path


def git_revisions(max_count=10):
    git_hist_cmd = f'git log -n {max_count} --format="%h"'
    result = subprocess.run(
        git_hist_cmd, shell=True, capture_output=True, text=True, check=True
    )
    return [sha for sha in result.stdout.split("\n") if sha]


def load(client, bucket, environment, revisions, fncache, cached_files):
    try:
        client.download_file(bucket, f"{environment}/{fncache}", fncache)
    except botocore.exceptions.ClientError:  # 404
        print("Cache file not found in Bucket")
        return

    with open(fncache, encoding="utf-8") as file:
        cache = json.load(file)

    # go through revisions
    for rev in revisions:
        # on first match (latest) download cached files
        if rev in cache:
            print(f"Getting cached files for version {rev}")
            for fname, local_path in cached_files.items():
                if fname in cache[rev]:
                    print(f"Downloading file {fname}")
                    try:
                        client.download_file(
                            bucket, f"{environment}/{rev}_{fname}", local_path
                        )
                    except botocore.exceptions.ClientError:
                        print(
                            f"File {environment}/{rev}_{fname} not found. Skipping download..."
                        )
                else:
                    print(f"File {fname} not in S3 cache")
            break


def save(client, bucket, environment, git_rev, fncache, cached_files):
    try:
        client.download_file(bucket, f"{environment}/{fncache}", fncache)
    except botocore.exceptions.ClientError:  # 404
        print("Cache file not found in Bucket")

    try:
        with open(fncache, encoding="utf-8") as file:
            cache = json.load(file)
    except FileNotFoundError:
        cache = {}

    cache[git_rev] = list(cached_files.keys())

    # update cache index file
    with open(fncache, "w", encoding="utf-8") as file:
        json.dump(cache, file)
    print("Uploading tmnet file to S3")
    client.upload_file(fncache, bucket, f"{environment}/{fncache}")

    # save each cache file
    for fname, local_path in cached_files.items():
        print(f"Uploading: {local_path} ...")
        try:
            client.upload_file(local_path, bucket, f"{environment}/{git_rev}_{fname}")
        except FileNotFoundError:
            print(f"File {local_path} not found. Skipping upload...")


def _build_parser(s3info) -> argparse.ArgumentParser:
    """parse command line arguments"""
    parser = argparse.ArgumentParser(description="Manage revisioned cached files on S3")
    # defautl action is to download cache, use --upload to store new cache.
    parser.add_argument(
        "environment",
        help="Identifier for cache environment, cache files are not shared across environments. i.e. linux-py39",
    )
    # S3 params
    parser.add_argument(
        "--s3-bucket",
        help="S3 Bucket, use unique identifier for project.",
        required="tmnet_s3_bucket" not in s3info,
    )
    parser.add_argument(
        "--s3-access-id",
        help="S3 access ID",
        required="tmnet_s3_access_id" not in s3info,
    )
    parser.add_argument(
        "--s3-secret",
        help="S3 secret key",
        required="tmnet_s3_secret_key" not in s3info,
    )
    parser.add_argument(
        "--s3-region",
        help="S3 region name",
        required="tmnet_s3_region" not in s3info,
    )
    parser.add_argument(
        "--s3-endpoint",
        help="S3 endpoint link",
        required="tmnet_s3_endpoint" not in s3info,
    )
    parser.add_argument("--upload", action="store_true", help="upload cache files")

    return parser


def _s3client(
    tmnet_s3_region, tmnet_s3_endpoint, tmnet_s3_access_id, tmnet_s3_secret_key
):
    """create s3 client"""
    s3session = session.Session()
    s3client = s3session.client(
        "s3",
        region_name=tmnet_s3_region,
        endpoint_url=tmnet_s3_endpoint,
        aws_access_key_id=tmnet_s3_access_id,
        aws_secret_access_key=tmnet_s3_secret_key,
    )
    return s3client


def main():
    # read ini file
    config = configparser.ConfigParser()
    _, config_path, _ = locate_config([])
    config.read(config_path or "pytest.ini")

    # TODO: files specification on INI file
    # right now it uses same datafile as testmon
    cached_files = {os.path.basename(get_data_file_path()): get_data_file_path()}

    # TODO: get params S3 params from command line
    s3info = dict(config["pytest.tmnet"]) if "pytest.tmnet" in config else {}

    parser = _build_parser(s3info)
    args = parser.parse_args()

    # overwriting s3info with args
    if args.s3_access_id:
        s3info["tmnet_s3_access_id"] = args.s3_access_id
    if args.s3_secret:
        s3info["tmnet_s3_secret_key"] = args.s3_secret
    if args.s3_bucket:
        s3info["tmnet_s3_bucket"] = args.s3_bucket
    if args.s3_region:
        s3info["tmnet_s3_region"] = args.s3_region
    if args.s3_endpoint:
        s3info["tmnet_s3_endpoint"] = args.s3_endpoint

    # overwriting s3info with env variables
    if "TMNET_S3_SECRET_KEY" in os.environ:
        s3info["tmnet_s3_secret_key"] = os.getenv("TMNET_S3_SECRET_KEY")

    s3client = _s3client(
        s3info["tmnet_s3_region"],
        s3info["tmnet_s3_endpoint"],
        s3info["tmnet_s3_access_id"],
        s3info["tmnet_s3_secret_key"],
    )

    revisions = git_revisions()

    if args.upload:
        save(
            s3client,
            s3info["tmnet_s3_bucket"],
            args.environment,
            revisions[0],
            "_tmnet.json",
            cached_files,
        )
    else:
        # TODO: option to specify revision from command line
        load(
            s3client,
            s3info["tmnet_s3_bucket"],
            args.environment,
            revisions,
            "_tmnet.json",
            cached_files,
        )


if __name__ == "__main__":
    main()
