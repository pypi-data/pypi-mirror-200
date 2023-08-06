import json
import requests
import logging
import typing
import sys
import functools
import subprocess
from copy import deepcopy

from . import exceptions, utils, mtrain_lims

logger = logging.getLogger(__name__)


def logged_in_guard(method):
    """Decorator to protect methods that require the client to be logged in.

    TODO fix this...
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # snapshot self.__logged_in in case you get super unlucky and this value changes between logical statement eval and logging eval
        value = self._logged_in
        if value is False:
            logger.debug("self.__logged_in=%s" % value)
            raise exceptions.MTrainSuperClientException("Not logged in.")

        return method(self, *args, **kwargs)
    return wrapper


class Client:

    SERIALIZE_PARAM_NAMES = ("q", )
    ENTITIES = ("regimens", "states", "subjects",
                "stages", "behavior_sessions", )

    def __init__(self, api_base: str, username: str, password: str, login=True):
        self._logged_in = False
        self.__logged_in = False
        self.__api_base = api_base
        self.__username = username
        self.__password = password
        logger.debug("Initializing. api_base: %s, username: %s, password: %s" % (
            self.__api_base, self.__username, self.__password, ))
        self.__session = requests.Session()
        if login is True:
            logger.debug("Logging in: login=%s" % login)
            self.login()

    def query_mtrain(self, route: str, handler, params: typing.Dict = {}, **kwargs):
        """Serializes params with key "q"
        """
        copied = deepcopy(params)  # dont mutate original args
        for param_name in copied.keys():
            if param_name in self.SERIALIZE_PARAM_NAMES:
                copied[param_name] = json.dumps(copied[param_name])

        resolved_endpoint = f"{self.__api_base}{route}"
        logger.debug("Resolved endpoint: %s" % resolved_endpoint)

        response = handler(
            resolved_endpoint,  # resolved endpoint
            params=copied,
            **kwargs
        )
        logger.debug("Request Status code: %s" % response.status_code)
        response.raise_for_status()
        return response

    def login(self):
        response = self.query_mtrain(
            route="/",
            handler=self.__session.post,
            data={
                "username": self.__username,
                "password": self.__password,
            }
        )
        logger.debug("Login response: %s" % response)
        # TODO add this for soft failure check: "Logged in as {self.__username}" in str(response.content)
        self._logged_in = True
        self.__logged_in = True
        logger.debug("Logged in: %s" % self.__logged_in)
        return response

    def get(self, entity_name: str, filter_property_name: str, filter_property_value: any, filter_operator="eq"):
        if entity_name not in self.ENTITIES:
            raise exceptions.MTrainSuperClientException(
                "Unsupported entity name: %s" % entity_name)

        resolved_route = f"/api/v1/{entity_name}"
        logger.debug("Resolved route: %s" % resolved_route)

        response = self.query_mtrain(
            route=resolved_route,
            handler=self.__session.get,
            params={
                "q": {
                    "filters": [{
                        "name": filter_property_name,
                        "val": filter_property_value,
                        "op": filter_operator,
                    }]
                }
            }
        )
        response_json = response.json()
        logger.debug("Response JSON: %s" % response_json)
        objects = response_json["objects"]
        if not len(objects) > 0:
            raise exceptions.NotFoundError("No objects returned from query.")

        return objects[0]

    def get_state(self, regimen_name: str, stage_name: str):
        """Mainly a convenience function because this is repeated sometimes
        """
        regimen = self.get(
            entity_name="regimens",
            filter_property_name="name",
            filter_property_value=regimen_name
        )
        logger.debug("Fetched regimen: %s" % regimen)
        logger.info("Fetched regimen_id: %s" % regimen["id"])
        for stage in regimen["stages"]:
            if stage["name"] == stage_name:
                break
        else:
            raise exceptions.MTrainSuperClientException("stage_name=%s not found in regimen_name=%s" % (
                stage_name, regimen_name, ))
        logger.debug("Resolved stage: %s" % stage)
        logger.info("Resolved stage_id: %s" % stage["id"])
        return self.get(
            entity_name="states",
            filter_property_name="stage_id",
            filter_property_value=stage["id"],
            filter_operator="eq",
        )

    @logged_in_guard
    def set_state(self, labtracks_id: int, regimen_name: str, stage_name: str):
        state = self.get_state(
            regimen_name=regimen_name,
            stage_name=stage_name,
        )
        logger.debug("Resolved state: %s" % state)
        route = f"/set_state/{labtracks_id}"
        logger.debug("Resolved route: %s" % route)
        return self.query_mtrain(
            route=route,
            handler=self.__session.post,
            data={
                # api requires state to be a json serialized as a string
                "state": json.dumps(state),
            }
        )

    def add_session(self, foraging_id: str, session_filepath: str):
        """Funny thing is that you don't technically need to be logged in for 
        this but you do need a username and password.
        """
        major_version = sys.version_info.major
        minor_version = sys.version_info.minor
        micro_version = sys.version_info.micro
        logger.debug("Python version detected: major=%s, minor=%s, micro=%s" % (
            major_version, minor_version, micro_version))
        if major_version != 3 or minor_version != 7:
            raise NotImplementedError("Not supported yet...perhaps one day...")

        logger.debug("add_session: Supported python version detected.")
        input_filepath, output_filepath, bundle_dir, bundle_cleanup = utils.generate_mtrain_lims_upload_bundle(
            self.__api_base,
            self.__username,
            self.__password,
            foraging_id,
            session_filepath,
        )
        try:
            python_path = sys.executable
            logger.debug(
                "Resolved python path for mtrain_lims subprocess: %s" % python_path)
            p = subprocess.Popen([
                python_path,
                "-m",
                "mtrain_lims",
                f"--input_json={input_filepath}",
                f"--output_json={output_filepath}",
            ], env={"LIMS2_DEPLOYMENT_DIR": bundle_dir})

            exit_code = p.wait()

            if not exit_code in [0]:
                raise exceptions.MTrainSuperClientException(
                    "Non-zero exit for mtrain_lims upload subprocess: %s" % exit_code)

            with open(output_filepath, "r") as f:
                result = json.load(f)

            if result.get("status_code") != 200 or \
                    json.loads(result.get("text", "{}")).get("success") != True:
                raise exceptions.MTrainSuperClientException(
                    "Unexpected upload result. %s" % result)
        finally:
            bundle_cleanup()

    def add_session_docker(self, foraging_id: str, session_filepath: str, mtrain_lims_package_dir: str):
        """Funny thing is that you don't technically need to be logged in for 
        this but you do need a username and password.
        """
        input_filepath, output_filepath, bundle_dir, bundle_cleanup = utils.generate_mtrain_lims_upload_bundle(
            self.__api_base,
            self.__username,
            self.__password,
            foraging_id,
            session_filepath,
        )
        try:
            exit_code = mtrain_lims.upload_session_docker(
                mtrain_lims_package_dir,
                bundle_dir,
                input_filepath,
                output_filepath,
            )

            if not exit_code in [0]:
                raise exceptions.MTrainSuperClientException(
                    "Non-zero exit for mtrain_lims upload subprocess: %s" % exit_code)

            with open(output_filepath, "r") as f:
                result = json.load(f)

            if result.get("status_code") != 200 or \
                    json.loads(result.get("text", "{}")).get("success") != True:
                raise exceptions.MTrainSuperClientException(
                    "Unexpected upload result. %s" % result)
        finally:
            bundle_cleanup()

    def add_session_conda(self, foraging_id: str, session_filepath: str, conda_dir: str):
        """Funny thing is that you don't technically need to be logged in for 
        this but you do need a username and password.
        """
        input_filepath, output_filepath, bundle_dir, bundle_cleanup = utils.generate_mtrain_lims_upload_bundle(
            self.__api_base,
            self.__username,
            self.__password,
            foraging_id,
            session_filepath,
        )
        try:
            exit_code = mtrain_lims.upload_session_conda(
                conda_dir,
                bundle_dir,
                input_filepath,
                output_filepath,
            )

            if not exit_code in [0]:
                raise exceptions.MTrainSuperClientException(
                    "Non-zero exit for mtrain_lims upload subprocess: %s" % exit_code)

            with open(output_filepath, "r") as f:
                result = json.load(f)

            if result.get("status_code") != 200 or \
                    json.loads(result.get("text", "{}")).get("success") != True:
                raise exceptions.MTrainSuperClientException(
                    "Unexpected upload result. %s" % result)
        finally:
            bundle_cleanup()

    @logged_in_guard
    def add_regimen(self, regimen: dict):
        return self.query_mtrain(
            route="/set_regimen/",
            handler=self.__session.post,
            data=json.dumps(regimen),
        )

    @logged_in_guard
    def add_subject(self, labtracks_id: int, regimen_name: str, stage_name: str):
        state = self.get_state(
            regimen_name=regimen_name,
            stage_name=stage_name,
        )
        logger.debug("Resolved state: %s" % state)
        return self.query_mtrain(
            route="/add_subject/",
            handler=self.__session.post,
            data={
                "LabTracks_ID": labtracks_id,
                "state": json.dumps({
                    # kinda weird might be the correct way to think about this...
                    "id": state["id"],
                    "stage_id": state["stage_id"],
                    "regimen_id": state["regimen_id"],
                }),
            }
        )
