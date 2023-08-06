import os
import logging
import argparse
import oss2
import json
import zipfile
import shutil
import time
import tempfile
import uuid

# import common
from . import common
from .lib_repo import LibRepo, LibData, LibType

from .common import get_bucket, zip_dir, unzip_file, upload_file, download_file, OSS_BASE_PATH, get_platform_name, available_config_names, available_arches

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

DEPENDENCY_JSON_FILE_NAME = 'dependencies.json'


def get_default_dep_path():
    return os.path.join(os.getcwd(), DEPENDENCY_JSON_FILE_NAME)

def get_dep(dep_path):
    with open(dep_path, 'r') as f:
        return json.load(f)

def __download_lib_single_part(param: tuple[str, str, bool], created_folders: list[str], backup_folders: list[str]):
    file_key = param[0]
    local_path = param[1]
    need_overwrite = param[2]
    _, zip_name = os.path.split(file_key)
    zip_file_path = os.path.join(local_path, zip_name)
    if os.path.exists(local_path):
        if not need_overwrite:
            logger.info(f'Skip download {zip_name}, because it already exist in {local_path}')
            return
        else:
            bk_path = tempfile.gettempdir()
            bk_path = os.path.join(bk_path, f'lib_repo_bk_{uuid.uuid4().hex}')
            shutil.move(local_path, bk_path)
            backup_folders.append((local_path, bk_path))
    
    os.makedirs(local_path)
    created_folders.append(local_path)
    
    logger.info(f'Downloading {zip_name} to {local_path}')
    download_file(file_key, zip_file_path)
    logger.info(f'End download {zip_name} to {local_path}')

    logger.info(f'Begin unzip {zip_file_path}')
    unzip_file(zip_file_path, local_path)
    os.remove(zip_file_path)
    logger.info(f'End unzip {zip_file_path}')

def bulk_download_lib_files(params: list[tuple[str, str, bool]]):
    '''
    params: list[tuple(file_key, local_path, need_overwrite)]
    '''
    created_folders = []
    backup_folders = [] # (origin_path, backup_path)

    expection = None
    try:
        for data in params:
            __download_lib_single_part(data, created_folders, backup_folders)
    except Exception as e:
        logger.exception(f'Failed to download library. Error: {str(e)}')
        for created_path in created_folders:
            shutil.rmtree(created_path)
        for origin_path, backup_path in backup_folders:
            shutil.move(backup_path, origin_path)
        expection = e
    else:
        for origin_path, backup_path in backup_folders:
            shutil.rmtree(backup_path)

    if expection:
        raise expection

def download_lib(lib: LibData, to_path: str):
    params = []
    header_source_overwrite = False
    if lib.lib_type == LibType.BINARY.value:
        file_key = lib.file_key()
        local_path = os.path.join(to_path, lib.gen_local_path())
        if common.file_exist(file_key):
            params.append((file_key, local_path, False))
            header_source_overwrite = not os.path.exists(local_path)
        else:
            raise Exception(f'Lib files can not be found for {lib.name} ({lib.version})')

    source_file_key = lib.file_key_for_source()
    source_local_path = os.path.join(to_path, lib.gen_local_path_for_source())
    if lib.lib_type == LibType.SOURCE.value and not common.file_exist(source_file_key):
        raise Exception(f'Source can not be found for {lib.name}')
    if common.file_exist(source_file_key):
        params.append((source_file_key, source_local_path, header_source_overwrite))

    header_file_key = lib.file_key_for_header()
    header_local_path = os.path.join(to_path, lib.gen_local_path_for_header())
    if common.file_exist(header_file_key):
        params.append((header_file_key, header_local_path, header_source_overwrite))
    else:
        raise Exception(f'Header can not be found for {lib.name}')

    bulk_download_lib_files(params)

def parse_args():
    description = "Download dependencies lib."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--platform', help='Platform', choices=common.available_platforms())
    parser.add_argument('--arch', help='Lib architecture', choices=common.all_available_arches())
    parser.add_argument('--config', help='Lib config type', choices=common.available_config_names())
    parser.add_argument('--dep', help='The dependencies json file in which the libs will be download from lib repo')
    parser.add_argument('--dest', help='Where download the libs to')

    sub_parsers = parser.add_subparsers(dest='sub_command')
    list_parser = sub_parsers.add_parser('list')

    return parser.parse_args()

def strip(s):
    return s.strip() if s else None

def list_command(args):
    print(str(LibRepo().pull_repo()))

def valid_get_args(args):
    ordered_args = ['platform', 'arch', 'config']
    for index, arg in enumerate(ordered_args):
        if strip(getattr(args, arg)):
            continue
        if index == len(ordered_args) - 1:
            break

        for sub_index in range(index + 1, len(ordered_args)):
            sub_arg = ordered_args[sub_index]
            if strip(getattr(args, sub_arg)):
                raise Exception(f'Invalid arguments. {sub_arg} is setted, but {arg} is not given.')
    return True

def create_link_to_lib(lib: LibData, dest_path: str):
    origin_path = os.path.join(dest_path, lib.name, lib.version)
    link_path_folder = os.path.join(dest_path, lib.name)
    if not os.path.exists(link_path_folder):
        os.makedirs(link_path_folder)
    link_path = os.path.join(link_path_folder, 'current')
    if (os.path.islink(link_path)):
        os.unlink(link_path)

    os.symlink(os.path.abspath(origin_path), link_path, target_is_directory=True)

def lib_get():
    args = parse_args()
    if not valid_get_args(args):
        return

    if args.sub_command == 'list':
        return list_command(args)
    
    platform = strip(args.platform)
    platform = common.get_platform_name() if not platform else platform

    logger.info(f'Reading libs repository info.')
    repo = LibRepo().pull_repo()
    logger.info(f'Read libs repository info successfully.')

    dep_config_file = strip(args.dep) if strip(args.dep) else get_default_dep_path()
    deps = get_dep(dep_config_file)
    downloading_libs = []
    for name, ver in deps.items():
        name = strip(name)
        ver = strip(ver)
        potential_libs = repo.query_libs(name=name, version=ver)
        if not potential_libs:
            raise Exception(f'Library not found. Name: {name}, version: {ver}')
        
        if potential_libs[0].lib_type in (LibType.HEADER_ONLY.value, LibType.SOURCE.value):
            if len(potential_libs) == 1:
                downloading_libs.append(potential_libs[0])
            else:
                raise Exception(f'Multiple libs are found for {name} with version {ver}')
        elif potential_libs[0].lib_type in (LibType.BINARY.value,):
            arch = strip(args.arch)
            config = strip(args.config)
            found_libs = repo.query_libs(name=name, version=ver, platform=platform, arch=arch, config=config)
            if not found_libs:
                print(f'[error] can not find lib from repo. name: {name}, version: {ver}, platform: {platform}, architecture: {arch}, config: {config}')
            else:
                downloading_libs.extend(found_libs)
        else:
            raise Exception(f'Unknown library type: {potential_libs[0].lib_type}, name: {name}, version: {ver}')

    logger.info('Begin Download dependent 3rd libraries.')

    start_time = time.time()
    libs_dest_dir = strip(args.dest) if strip(args.dest) else os.path.split(dep_config_file)[0]
    libs_dest_dir = os.path.join(libs_dest_dir, platform)
    for lib in downloading_libs:
        logger.info(f'---------------Begin download library {lib.name}, version: {lib.version}, platform: {lib.platform}, arch: {lib.arch}, config: {lib.config}----------------')
        download_lib(lib, libs_dest_dir)
        logger.info(f'---------------End download library {lib.name}, version: {lib.version}, platform: {lib.platform}, arch: {lib.arch}, config: {lib.config}----------------')
        create_link_to_lib(lib, libs_dest_dir)
    
    logger.info(f'End download dependent 3rd libraries. Cost time: {str(time.time() - start_time)} seconds.')

if __name__ == '__main__':
    lib_get()
