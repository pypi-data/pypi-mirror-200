import os
import sys
import enum
import logging
import subprocess
import typing


logger = logging.getLogger(__name__)


class UploadType(enum.Enum):

    system = "system"
    docker = "docker"


def upload_session(session, upload_type: UploadType = UploadType.system):
    if upload_type == UploadType.system:
        return upload_session_system()
    elif upload_type == UploadType.docker:
        return upload_session_docker()
    else:
        raise Exception("Unexpected upload_type=%s" % upload_type)


def upload_session_system(python_path: typing.Optional[str]):
    pass


def upload_session_docker(
    mtrain_lims_package_dir: str,
    bundle_dir: str,
    input_json_path: str,
    output_json_path: str,
):
    current_dir = os.path.dirname(__file__)
    upload_script_name = "mtrain_lims_upload.sh"
    local_script_path = os.path.join(current_dir,
                                     upload_script_name)

    p = subprocess.Popen([
        "docker",
        "run",
        "-e",
        "HOST_ID=`id -u`",
        "-v",
        f"{bundle_dir}:{bundle_dir}",
        "-e",
        f"UPLOAD_INPUT_JSON={input_json_path}",
        "-e",
        f"UPLOAD_OUTPUT_JSON={output_json_path}",
        "-e",
        f"LIMS2_DEPLOYMENT_DIR={bundle_dir}"
        # "-it",
        "-v",
        f"{mtrain_lims_package_dir}:/pkg",
        "-v",
        f"{local_script_path}:/{upload_script_name}",
        # "mtrain_lims",
        "continuumio/miniconda3:latest",
        f"/{upload_script_name}",
    ])

    return p.wait()


def upload_session_conda(
    conda_dir: str,
    bundle_dir: str,
    input_json_path: str,
    output_json_path: str,
):
    current_dir = os.path.dirname(__file__)
    upload_script_name = "mtrain_lims_upload.sh"
    local_script_path = os.path.join(current_dir,
                                     upload_script_name)

    # p = subprocess.Popen([
    #     "conda",
    #     "activate",
    #     conda_dir,
    #     "&&",
    #     "mtrain_lims"
    # ], shell=True)

    p = subprocess.Popen(
        [f"source activate {conda_dir} && mtrain_lims --input_json={input_json_path} --output_json={output_json_path}"], shell=True)

    # p = subprocess.Popen([
    #     f"conda init bash && conda activate {conda_dir}",
    #     "&&",
    #     f"conda activate {conda_dir}",
    #     "&&",
    #     "mtrain_lims"
    # ], shell=True)

    return p.wait()
