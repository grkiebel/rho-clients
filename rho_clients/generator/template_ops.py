from ..api import g_api as apx
from ..log_config import get_logger
from ..cmds.sim import Sim
from ..ops.helpers import display_ops_result

sim = Sim()

apx.initialize("http://localhost:8080", get_logger("API-Access"))
