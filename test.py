#!/usr/bin/env python
"""Entry point to run tests."""

import argparse
import asyncio
import logging
from os import environ
from subprocess import Popen, run, check_call
from time import time

import httpx
import yaml
from synapse._scripts.register_new_matrix_user import request_registration
from nio import AsyncClient

MATRIX_URL, MATRIX_ID, MATRIX_PW = (
    environ[v] for v in ["MATRIX_URL", "MATRIX_ID", "MATRIX_PW"]
)
FULL_ID = f'@{MATRIX_ID}:{MATRIX_URL.split("/")[2]}'
LOGGER = logging.getLogger("syngo.tests.start")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-v", "--verbose", action="count", default=0, help="increment verbosity "
)


def wait_available(url: str, key: str, timeout: int = 10) -> bool:
    """Wait until a service answer correctly or timeout."""

    def check_json(url: str, key: str) -> bool:
        """
        Ensure a service at a given url answers with valid json with a key.
        """
        try:
            data = httpx.get(url).json()
            return key in data
        except httpx.ConnectError:
            return False

    start = time()
    while True:
        if check_json(url, key):
            return True
        if time() > start + timeout:
            return False


async def get_access_token():
    client = AsyncClient(MATRIX_URL, MATRIX_ID)
    resp = await client.login(MATRIX_PW, device_name="test")
    await client.close()
    return resp.access_token


def run_and_test():
    """Launch the bot and its tests."""
    # Start the server, and wait for it
    LOGGER.info("Spawning synapse")
    srv = Popen(
        [
            "python",
            "-m",
            "synapse.app.homeserver",
            "--config-path",
            "/srv/homeserver.yaml",
        ]
    )
    if not wait_available(f"{MATRIX_URL}/_matrix/client/r0/login", "flows"):
        return False

    # Register a user for the bot.
    LOGGER.info("Registering an user")
    with open("/srv/homeserver.yaml") as f:
        conf = yaml.safe_load(f.read())
        secret = conf.get("registration_shared_secret", None)
    request_registration(MATRIX_ID, MATRIX_PW, MATRIX_URL, secret, admin=True)

    # Get its access_token
    LOGGER.info("Get access token")
    environ["MATRIX_ACCESS_TOKEN"] = asyncio.run(get_access_token())
    environ["MATRIX_DOMAIN"] = "tests"

    # Run tests
    LOGGER.info("Runnig unittests")
    check_call(["coverage", "run", "./manage.py", "test"])

    LOGGER.info("Stopping synapse")
    srv.terminate()

    LOGGER.info("Processing coverage")
    for cmd in ["report", "html", "xml"]:
        run(["coverage", cmd])


if __name__ == "__main__":
    args = parser.parse_args()
    fields = ["asctime", "name", "lineno", "levelname", "message"]
    log_format = " - ".join([f"%({field})s" for field in fields])
    logging.basicConfig(level=50 - 10 * args.verbose, format=log_format)
    run_and_test()
