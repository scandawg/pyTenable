"""
This file contains tests for the Access Control endpoints.
"""
import string
import uuid
from random import choices

import pytest

from tenable.io import TenableIO


@pytest.mark.vcr()
def test_details(api: TenableIO, permission):
    details = api.v3.access_control.details(permission['permission_uuid'])
    assert isinstance(details, dict)
    assert details["permission_uuid"] == permission['permission_uuid']


@pytest.mark.vcr()
def test_details_negative(api: TenableIO):
    with pytest.raises(TypeError):
        api.v3.access_control.details(None)


@pytest.mark.vcr()
def test_get_user_permission(api: TenableIO, user, permission):
    user_permission = api.v3.access_control.get_user_permission(user['uuid'])
    assert isinstance(user_permission, dict)
    assert len(user_permission["permissions_available"]) > 0


@pytest.mark.vcr()
def test_get_user_permission_negative(api: TenableIO):
    with pytest.raises(TypeError):
        api.v3.access_control.get_user_permission(None)


@pytest.mark.vcr()
def test_get_user_group_permission(api: TenableIO):
    group_uuid_to_search = "00000000-0000-0000-0000-000000000000"
    user_group_permission = api.v3.access_control.get_user_group_permission(group_uuid_to_search)
    assert isinstance(user_group_permission, dict)
    assert len(user_group_permission["permissions_available"]) > 0


@pytest.mark.vcr()
def test_get_user_group_permission_negative(api: TenableIO):
    with pytest.raises(TypeError):
        api.v3.access_control.get_user_group_permission(None)


@pytest.mark.vcr()
def test_get_current_user_permission(api: TenableIO):
    current_user_permission = api.v3.access_control.get_current_user_permission()
    assert isinstance(current_user_permission, dict)


@pytest.mark.vcr()
def test_create_and_delete(api: TenableIO, user):
    # Testing creation of permission
    created_permission = _create_permission(api, user['uuid'])
    assert isinstance(created_permission, dict)

    created_permission_uuid = created_permission["permission_uuid"]
    assert isinstance(created_permission_uuid, str)

    # Testing Deletion of the permission
    deleted_permission = _delete_permission(api, created_permission_uuid)
    assert deleted_permission["permission_uuid"] == created_permission_uuid


@pytest.mark.vcr()
def test_update(api: TenableIO, user):
    # Creation permission only to update it later
    created_permission = _create_permission(api, user['uuid'])
    created_permission_uuid = created_permission["permission_uuid"]
    updated_permission = _update_permission(api, created_permission_uuid, user['uuid'])
    assert updated_permission is None

    # Cleaning up after test
    _delete_permission(api, created_permission_uuid)


@pytest.mark.vcr()
def test_list(api: TenableIO):
    permissions = api.v3.access_control.list()
    assert isinstance(permissions, list)


def _create_permission(api: TenableIO, user_uuid: str):
    """
    Invokes the creation API for testing.
    """
    permission = {
        "actions": ["CanView", "CanUse"],
        "objects": [
            {
                "name": "Category,dummy_value",
                "type": "Tag",
                "uuid": f"{str(uuid.uuid4())}"
            }
        ],
        "subjects": [
            {
                "name": "User sub",
                "type": "User",
                "uuid": user_uuid
            }
        ],
        "name": f"test_{_random_string(5)}"
    }
    created_permission = api.v3.access_control.create(permission)
    return created_permission


def _delete_permission(api: TenableIO, permission_uuid: str):
    """
    Invokes the deletion API for testing.
    """
    return api.v3.access_control.details(permission_uuid)


def _update_permission(api: TenableIO, permission_uuid: str, user_uuid: str):
    """
    Invokes the update API for testing.
    """
    permission_to_update = {
        "actions": ["CanView"],
        "objects": [
            {
                "name": "Category,dummy_value",
                "type": "Tag",
                "uuid": permission_uuid
            }
        ],
        "subjects": [
            {
                "name": "User sub",
                "type": "User",
                "uuid": user_uuid
            }
        ],
        "name": f"test_{_random_string(5)}"
    }
    return api.v3.access_control.update(permission_uuid, permission_to_update)


def _random_string(length: int):
    """
    Creates a random string of a given length
    Args:
        length: Length of the string to be generated

    Returns: str

    """
    return "".join(choices(string.ascii_letters, k=length))
