import os
import json
from json import JSONDecodeError

import yaml
from loguru import logger
import requests
from requests.structures import CaseInsensitiveDict
from urllib3.exceptions import InsecureRequestWarning
from yaml.composer import ComposerError

from generic_crawler.config import Config
from generic_crawler.actions import ActionSchema

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



### HELPER FUNCTIONS
def apply_custom_assertion(condition, exception, msg):
    if condition:
        raise exception(msg)


## CORE OBJECTS
class ActionReader:
    def __init__(self, path_to_yaml):
        self.path_to_yaml = path_to_yaml
        self._load_yaml()
        self._validate()

    def _load_yaml(self):
        with open(self.path_to_yaml, 'r') as f:
            try:
                self.action = yaml.safe_load(f)
            except ComposerError as ce:
                logger.error(f"you tried loading multiple actions at single yaml file please check your yaml file")
                raise ce


    def _validate(self):
        assert ActionSchema.validate(self.action)
        logger.debug(f"Action {self.action['name']} schema looks good")
        if type(self.action) == list:
            raise ValueError("Only one action can be retrieved at a time. If you have multiple steps or targets, define at your action.yaml file")
        try:
            assert self.action["steps"]
            assert self.action["targets"]
        except KeyError as ke:
            logger.error("Actions must be a single dictionary with steps,targets instructions, use ActionReader to parse your action.yaml file")
            raise ke


class GenericCrawler:
    def __init__(self, config: Config):
        self.token = config.token
        self.endpoint = config.endpoint_url
        logger.debug(f"health checking for service {self.endpoint}")
        health_check_url = f"{self.endpoint}/health/live"
        response = requests.get(health_check_url, verify=False, timeout=10)
        status_code = response.status_code
        content = json.loads(response.content.decode('utf-8'))
        if status_code == 200 and content["detail"] == "OK!":
            self.is_alive = True
            logger.debug("health check success, service is alive!")
        else:
            raise ConnectionError(f"Failed to connect crawler service - {self.endpoint} withe response code: {response.status_code} and reason: {response.reason}")


    def retrieve(self, action):
        self.action = action
        logger.info(f"Requesting from crawl service for action {self.action['name']}, this can take around a minute.")
        headers = CaseInsensitiveDict()
        headers["Authorization"] = f"Bearer {self.token}"
        response = requests.post(f"{self.endpoint}/crawl",
                                 json=self.action,
                                 headers=headers,
                                 verify=False)
        try:
            content = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            logger.warning(f"parsing response content failed, something gone wrong! Returning raw response for debugging purposes")
            return None, response
        logger.info(f"Data retrieval sequence completed, should check whether fail or success")
        return content, response


class FileHandler:
    def __init__(self):
        pass

    def write_to_local_filesystem(self, local_file_path, content):
        bcontent = content.encode('utf-8')
        with open(f"{local_file_path}", 'wb') as f:
            f.write(bcontent)
        logger.success(f"file saved into: {local_file_path}")

    def upload_to_bucket(self):
        raise NotImplementedError




