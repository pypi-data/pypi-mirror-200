import re
import os
import json
import yaml
import shutil
import pickle
import random
import typing
import tempfile
import requests

from . import exceptions


def _generate_random_labtracks_id() -> int:
    # helper function
    # must be a 6 digit integer, cant be 999999 due special api handling for 999999
    return random.randint(100000, 999998)


# cant type hint client due to awkward import order...
def autogenerate_labtracks_id(client, max_tries=100) -> int:
    """Utility function for autogenerating a labtracks_id that doesn't already exist.
    """
    for n in range(max_tries):
        labtracks_id = _generate_random_labtracks_id()
        try:
            client.get(
                entity_name="subjects",
                filter_property_name="LabTracks_ID",
                filter_operator="eq",
                filter_property_value=labtracks_id,
            )
        except exceptions.NotFoundError:
            return labtracks_id

    else:
        raise Exception(
            "Failed to autogenerate a labtracks_id after %s tries." % n)


def generate_mtrain_lims_upload_bundle(api_base: str, username: str, password: str, foraging_id: str, session_filepath: str) -> typing.Tuple[str, str, str, typing.Callable]:
    temp_dir = tempfile.TemporaryDirectory()

    input_json_path = os.path.join(temp_dir.name, "input.json")
    with open(input_json_path, "w") as f:
        json.dump({
            "inc": {
                "API_BASE": api_base,
                "foraging_id": foraging_id,
                "foraging_file_name": session_filepath,
            }
        }, f)

    # generate secrets file required by mtrain_lims
    mtrain_secrets_path = os.path.join(temp_dir.name, "mtrain_secrets.yml")
    with open(mtrain_secrets_path, "w") as f:
        yaml.dump({
            "username": username,
            "password": password,
        }, f)

    return input_json_path, os.path.join(temp_dir.name, "output.json"), temp_dir.name, lambda: temp_dir.cleanup()


def replace_behavior_session_metadata_dynamic_routing(path: str, labtracks_id: int) -> str:
    """Replace dynamic routing metadata required for an mtrain v2 session upload
    """
    upload_filename = os.path.basename(path)
    # subject id must be serialized in upload filepath
    renamed_upload_filepath = re.sub(
        # this regex isnt great but this is just test code okay...
        r"DynamicRouting1_(\d{6})",
        f"DynamicRouting1_{labtracks_id}",
        upload_filename,
    )
    assert not os.path.isfile(
        renamed_upload_filepath), "Renamed upload shouldnt exist yet."
    shutil.copy(path, renamed_upload_filepath)
    assert os.path.isfile(
        renamed_upload_filepath), "Renamed upload should exist."
    return renamed_upload_filepath


def replace_behavior_session_metadata_doc(path: str, labtracks_id: int, foraging_id: str) -> str:
    """Replace doc metadata required for an mtrain v1 session upload
    """
    upload_filename = os.path.basename(path)
    # subject id must be serialized in upload filepath
    deserialized = os.path.splitext(upload_filename)[0].split("_")
    renamed_upload_filepath = f"{deserialized[0]}_{labtracks_id}_{foraging_id}.pkl"
    assert not os.path.isfile(
        renamed_upload_filepath), "Renamed upload shouldnt exist yet."
    shutil.copy(path, renamed_upload_filepath)
    assert os.path.isfile(
        renamed_upload_filepath), "Renamed upload should exist."

    with open(renamed_upload_filepath, "rb") as f:
        data = pickle.load(f, encoding="latin1")

    data["session_uuid"] = foraging_id
    # overwrite mouse_id everywhere vba looks
    data["items"]["behavior"]["params"]["mouse_id"] = labtracks_id
    data["items"]["behavior"]["cl_params"]["mouse_id"] = labtracks_id
    data["items"]["behavior"]["config"]["behavior"]["mouse_id"] = labtracks_id

    with open(renamed_upload_filepath, "wb") as f:
        pickle.dump(data, f, protocol=0)

    return renamed_upload_filepath


def replace_behavior_session_metadata_passive(path: str, output_filepath: str, labtracks_id: int, session_id: str) -> str:
    with open(path, "rb") as f:
        data = pickle.load(path, encoding="latin1")

    data["mouse_id"] = labtracks_id
    data["session_uuid"] = session_id

    with open(output_filepath, "wb") as f:
        pickle.dump(data, f, protocol=0)

    return output_filepath


def get_regimen_from_github(tag_name: str, github_uri_template="https://raw.githubusercontent.com/AllenInstitute/mtrain_regimens/%s/regimen.yml") -> typing.Dict:
    result = requests.get(github_uri_template % tag_name)
    result.raise_for_status()
    return yaml.load(
        result.content,
        Loader=yaml.FullLoader,
    )
