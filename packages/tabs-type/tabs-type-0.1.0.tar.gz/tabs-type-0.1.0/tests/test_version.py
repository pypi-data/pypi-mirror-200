import re

import pytest
from packaging.version import Version

from tabs_type.version import VersionManager


@pytest.mark.parametrize("package", ["tabs-type"])
def test_get_package_version(package):
    version = VersionManager.get_package_version(package)
    regex = "^(\d+\.)?(\d+\.)?(\*|\d+)$"
    match = re.match(regex, str(version))
    assert match


@pytest.mark.parametrize(
    "versions, expected",
    [
        (["1.0.0", "2.0.0", "3.0.0"], Version("3.0.0")),
        ([Version("1.1.0"), Version("1.2.0"), Version("1.0.1")], Version("1.2.0")),
        (["1.1.3", Version("1.1.1"), "1.1.0"], Version("1.1.3")),
        (["11.0.0", "9.1.0", "8.1.0"], Version("11.0.0")),
    ],
)
def test_get_latest_version(versions, expected):
    assert VersionManager.get_latest_version(versions) == expected
