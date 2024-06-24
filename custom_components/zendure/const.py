"""Constants for zendure."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Integration blueprint"
DOMAIN = "zendure"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

ZEN_API_URL = "https://app.zendure.tech/v2"
ZEN_AUTH_PATH = "/auth/app/token"
ZEN_DEVICELIST_PATH = "/productModule/device/queryDeviceListByConsumerId"
ZEN_DEVICEDETAILS_PATH = "/device/solarFlow/detail"
