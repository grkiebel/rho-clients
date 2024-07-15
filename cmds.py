from rho_clients.api import g_api as apx
from rho_clients.cmds import cmd_shell as cs
from rho_clients.log_config import get_logger


if __name__ == "__main__":

    apx.initialize("http://localhost:8080", get_logger("API-Access"))

    cs.main()

    print("done")
