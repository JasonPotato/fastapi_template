"""simple tool to scrape data out of pyroject.toml"""

import sys
import argparse
import requests


def parse_script_args():
    """define script arguments this tool accepts"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api",
        "-a",
        default="/api/v1/health",
        type=str,
        help="the api endpoint that tells us whether the service is healthy",
    )
    parser.add_argument(
        "--url",
        "-u",
        default="http://localhost",
        type=str,
        help="the url to expect the rest api at",
    )
    parser.add_argument(
        "--port",
        "-p",
        default="8000",
        type=str,
        help="the port the pai is running on",
    )

    return parser.parse_args()


def main():
    """main driver"""
    script_args = parse_script_args()
    response = requests.get(
        f"{script_args.url}:{script_args.port}{script_args.api}", timeout=10
    )
    response_json = response.json()
    if (
        response.status_code != 200
        or "status" not in response_json
        or response_json["status"] != "Healthy!"
    ):
        print(f"HTTP status code: {response.status_code}", file=sys.stderr)
        print(response_json, file=sys.stderr)
        sys.exit(1)
    print(f"HTTP status code: {response.status_code}")
    print(response_json["status"])


if __name__ == "__main__":
    main()
