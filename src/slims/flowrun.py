import logging
from enum import Enum

logger = logging.getLogger('genohm.slims.flowrun')


class Status(Enum):
    DONE = 1
    FAILED = 2


class FlowRun(object):

    def __init__(self, slims_api, index, data):
        self.slims_api = slims_api
        self.index = index
        self.data = data

    def log(self, message):
        logger.info(message)
        body = {
            'index': self.index,
            'flowRunGuid': self.data["flowInformation"]["flowRunGuid"],
            'message': message
        }
        self.slims_api.post("external/log", body)

    def update_status(self, status):
        logger.info("Updating flowrun to status " + status.name)
        body = {
            'index': self.index,
            'flowRunGuid': self.data["flowInformation"]["flowRunGuid"],
            'status': status.name
        }
        self.slims_api.post("external/status", body)

    def check_user_secret(self):
        body = {
            'index': self.index,
            'flowRunGuid': self.data["flowInformation"]["flowRunGuid"],
            'username': self.data["SLIMS_CURRENT_USER"],
            'secret': self.data["flowStepSecret"]
        }
        response = self.slims_api.post("external/userSecretCheck", body)
        if response.status_code != 200:
            logger.info("User secret check failed: " + response.json()["errorMessage"])
            raise Exception("Forbidden access")