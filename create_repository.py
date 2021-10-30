#!/usr/bin/env python3

import datetime
import hashlib
import json
import zipfile

from pathlib import Path
from zipfile import ZipFile

ROOT_PATH = Path(__file__).resolve().parent
PACKAGES_JSON_PATH = ROOT_PATH / "packages.json"
REPOSITORY_JSON_PATH = ROOT_PATH / "repository.json"
METADATA_FILEAME = "metadata.json"
ICON_FILENAME = "icon.png"

REPOSITORY_BASE_URI = "https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master"

READ_SIZE = 65536


def sha256_of_file(path):
    file_hash = hashlib.sha256()

    with path.open("rb") as f:
        data = f.read(READ_SIZE)
        while data:
            file_hash.update(data)
            data = f.read(READ_SIZE)

    return file_hash.hexdigest()


def create_pcm_from_color_scheme(path, resulting_file):
    with ZipFile(resulting_file, 'w', compression=zipfile.ZIP_DEFLATED) as zip:
        for json_file in path.glob("*.json"):
            if json_file.name == METADATA_FILEAME:
                zip.write(json_file, json_file.name)
                continue
            zip.write(json_file, f"colors/{json_file.name}")

        icon_file = path / ICON_FILENAME
        if icon_file.exists():
            zip.write(icon_file, f"resources/{ICON_FILENAME}")


def install_size_of_zip(zip_path):
    install_size = 0
    with ZipFile(zip_path, 'r') as zip:
        for file in zip.filelist:
            install_size += zip.getinfo(file.filename).file_size
    return install_size


def create_and_get_pcm(path):
    metadata_path = path / METADATA_FILEAME
    if not metadata_path.exists():
        return

    with metadata_path.open("rb") as f:
        metadata_json = json.load(f)

    identifier = metadata_json["identifier"]

    for metadata_version in metadata_json["versions"]:
        version = metadata_version['version']
        pkg_name = f"{identifier}_v{version}_pcm.zip"
        pkg_path = path / pkg_name

        if not pkg_path.exists():
            # create new package as it does not exist yet (new version)
            create_pcm_from_color_scheme(path, pkg_path)

        # fill in package data
        metadata_version['download_sha256'] = sha256_of_file(pkg_path)
        metadata_version['download_size'] = pkg_path.stat().st_size
        metadata_version['download_url'] = f"{REPOSITORY_BASE_URI}/{path.name}/{pkg_name}"
        metadata_version['install_size'] = install_size_of_zip(pkg_path)

    return metadata_json


def write_packages_json(package_array):
    packages_data = {"packages": package_array}

    with PACKAGES_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(packages_data, f, indent=4)


def write_repository_json():
    packages_json_sha256 = sha256_of_file(PACKAGES_JSON_PATH)
    packages_json_update_timestamp = int(PACKAGES_JSON_PATH.stat().st_mtime)
    packages_json_update_time_utc = datetime.datetime.fromtimestamp(packages_json_update_timestamp, tz=datetime.timezone.utc)

    repository_data = {
        "$schema": "https://gitlab.com/kicad/code/kicad/-/raw/master/kicad/pcm/schemas/pcm.v1.schema.json#/definitions/Repository",
        "maintainer": {
            "contact": {
                "web": "https://github.com/pointhi/kicad-color-schemes/"
            },
            "name": "Thomas Pointhuber"
        },
        "name": "kicad-color-schemes repository by @pointhi",
        "packages": {
            "sha256": packages_json_sha256,
            "update_time_utc": packages_json_update_time_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "update_timestamp": packages_json_update_timestamp,
            "url": f"{REPOSITORY_BASE_URI}/packages.json"
        }
    }

    with REPOSITORY_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(repository_data, f, indent=4)


schema = create_and_get_pcm(ROOT_PATH / "solarized-dark")

write_packages_json([schema])
write_repository_json()
