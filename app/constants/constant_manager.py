
from app.constants.app_messages import AppMessages
from app.constants.directory_names import DirectoryNames
from app.constants.route_paths import RoutePaths
from app.constants.route_tags import RouteTags
from app.constants.data_type_constants import DataTypeConstants
from app.constants.api_call_status import APICallStatus

class ConstantManager(AppMessages, DirectoryNames,APICallStatus, RoutePaths, RouteTags,DataTypeConstants):
    def __init__(self) -> None:
        super.__init__()