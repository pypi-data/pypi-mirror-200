from dataclasses import dataclass
from importlib.metadata import version

from packaging.version import Version, parse


@dataclass(frozen=True)
class VersionManager:
    @staticmethod
    def get_latest_version(versions: list[str] | list[Version]) -> Version:
        versions = [parse(e) if isinstance(e, str) else e for e in versions]
        return max(versions)

    @staticmethod
    def get_version(package_name: str) -> Version:
        return parse(version(package_name))
