from .config import check_config
check_config()


from .download import load
from .info import _minder_datasets_info as datasets
from .info import _minder_organizations_info as organizations