import argparse
from ..api import g_api as apx
from . import cmd_shell as cs
from ..log_config import get_logger


def main(service_url: str = None):
    if not service_url:
        service_url = get_args()
    apx.initialize(service_url, get_logger("API-Access"))
    cs.main()


def get_args():
    parser = argparse.ArgumentParser(description="API Generator")
    parser.add_argument(
        "-url",
        "--rho_service_url",
        help="URL to the rho-service",
        default="http://localhost:8080",
    )

    args = parser.parse_args()
    return args.rho_service_url
