import json
import re
import shutil
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path

import requests

from .base import Resolver

REGISTRY_REF_REGEX = re.compile(
    r"""
    ^
    (?P<org>[^/]+)       # organization
    /(?P<name>[^@]+)     # name
    @(?P<version>[^:]+)  # version
    (:(?P<subpath>.+))?  # optional subpath
    $
    """,
    re.VERBOSE,
)


def parse_registry_ref(ref: str):
    match = re.match(REGISTRY_REF_REGEX, ref)
    if not match:
        return None
    return match.groupdict()


class RegistryResolver(Resolver):
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.cache_dir = Path.home() / ".hyperrr" / "cache"

    # -------------------------
    # Resolver Interface
    # -------------------------

    def can_resolve(self, ref: str) -> bool:
        return parse_registry_ref(ref) is not None

    def resolve(self, ref: str) -> str:
        parsed = parse_registry_ref(ref)
        if not parsed:
            raise ValueError(f"Invalid registry ref: {ref}")

        org = parsed["org"]
        name = parsed["name"]
        version = parsed["version"]
        subpath = parsed.get("subpath")

        # Step 1: resolve version
        version = self._resolve_version(org, name, version)

        # Step 2: ensure cached
        package_path = self._get_cache_path(org, name, version)

        if not self._is_cache_valid(org, name, version, package_path):
            self._download_and_extract(org, name, version, package_path)

        # Step 3: get file path
        file_path = self._resolve_prompt_file(package_path, subpath)

        # 🔥 FIX: return FILE CONTENT (not path)
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # -------------------------
    # Internal Helpers
    # -------------------------

    def _resolve_version(self, org, name, version):
        url = f"{self.base_url}/v1/resolve/{org}/{name}/{version}"
        res = requests.get(url)

        if res.status_code == 200:
            return res.json()["version"]

        return version

    def _get_cache_path(self, org: str, name: str, version: str) -> Path:
        return self.cache_dir / org / name / version

    def _download_and_extract(
        self,
        org: str,
        name: str,
        version: str,
        cache_path: Path,
    ):
        url = f"{self.base_url}/v1/prompts/{org}/{name}/{version}"

        res = requests.get(url, stream=True)

        print("Downloading:", url)
        print("Status:", res.status_code)

        if res.status_code != 200:
            raise Exception(f"Failed to download package: {res.text}")

        # 🔥 use temp dir
        temp_dir = Path(tempfile.mkdtemp())

        try:
            tar_path = temp_dir / "package.tar.gz"

            # download
            with open(tar_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=1024 * 1024):
                    f.write(chunk)

            # extract
            extract_path = temp_dir / "extracted"
            extract_path.mkdir()

            with tarfile.open(tar_path, "r:gz") as tar:
                self._safe_extract(tar, extract_path)

            # 🔥 replace cache atomically
            if cache_path.exists():
                shutil.rmtree(cache_path)

            cache_path.mkdir(parents=True, exist_ok=True)

            shutil.move(str(tar_path), cache_path / "package.tar.gz")

            # move extracted files
            for item in extract_path.iterdir():
                shutil.move(str(item), cache_path / item.name)

            # 🔥 write metadata
            metadata = {
                "version": version,
                "downloaded_at": datetime.utcnow().isoformat(),
            }

            with open(cache_path / "metadata.json", "w") as f:
                json.dump(metadata, f)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _resolve_prompt_file(self, package_path: Path, subpath: str | None) -> Path:
        if subpath:
            path = package_path / f"{subpath}.prompt"
            if not path.exists():
                raise Exception(f"Prompt not found: {subpath}")
            return path

        path = package_path / "main.prompt"
        if not path.exists():
            raise Exception("main.prompt not found")

        return path

    def _is_cache_valid(self, org, name, version, cache_path: Path) -> bool:
        metadata_path = cache_path / "metadata.json"
        tar_path = cache_path / "package.tar.gz"

        if not cache_path.exists():
            return False

        if not metadata_path.exists() or not tar_path.exists():
            return False

        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
                print("Cache metadata:", metadata)

            # optional: validate checksum later
            return True

        except Exception:
            return False

    # -------------------------
    # Security (important)
    # -------------------------

    def _safe_extract(self, tar: tarfile.TarFile, path: Path):
        for member in tar.getmembers():
            member_path = path / member.name
            if not str(member_path.resolve()).startswith(str(path.resolve())):
                raise Exception("Unsafe tar file detected")

        tar.extractall(path)
