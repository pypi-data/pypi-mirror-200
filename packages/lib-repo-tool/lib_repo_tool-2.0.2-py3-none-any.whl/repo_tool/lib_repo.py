import json
import os
import argparse
import shutil
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum
from datetime import datetime

from .common import available_arches, available_config_names, available_platforms
# import common
from . import common
from dacite import from_dict
from tabulate import tabulate

import logging
logger = logging.getLogger(__name__)

class LibType(Enum):
    BINARY = 'BINARY'
    HEADER_ONLY = 'HEADER_ONLY'
    SOURCE = 'SOURCE'

@dataclass
class LibData:
    name: str
    version: Optional[str]
    platform: Optional[str]
    arch: Optional[str]
    config: Optional[str] # config
    lib_type: Optional[str]
    datetime: Optional[str]

    @classmethod
    def from_dict(cls, data) -> "LibData":
        lib = from_dict(LibData, data)
        return lib

    def to_dict(self):
        return asdict(self)

    def file_key(self):
        if not self.name:
            raise Exception(f'invalid lib data: {self}')
        file_key = os.path.join(common.OSS_BASE_PATH, self.gen_path())
        file_key = os.path.join(file_key, self.get_zip_file_name())

        file_key = file_key.replace('\\', '/')

        return file_key

    def file_key_for_header(self):
        if not self.name:
            raise Exception(f'invalid lib data: {self}')
        file_key = os.path.join(common.OSS_BASE_PATH, self.gen_path_for_header())
        file_key = os.path.join(file_key, self.get_zip_file_name_for_header())

        file_key = file_key.replace('\\', '/')

        return file_key
    
    def file_key_for_source(self):
        if not self.name:
            raise Exception(f'invalid lib data: {self}')
        file_key = os.path.join(common.OSS_BASE_PATH, self.gen_path_for_source())
        file_key = os.path.join(file_key, self.get_zip_file_name_for_source())

        file_key = file_key.replace('\\', '/')

        return file_key
    
    def gen_path_for_header(self):
        return os.path.join(self.name, self.version, 'header')

    def gen_path_for_source(self):
        return os.path.join(self.name, self.version, 'source')

    def gen_path(self):
        if self.lib_type != LibType.BINARY.value:
            raise Exception('Not binary lib.')
        
        return os.path.join(self.name, self.version, 'lib', self.platform, self.arch, self.config)
    
    def gen_local_path_for_header(self):
        return os.path.join(self.name, self.version, 'include')

    def gen_local_path_for_source(self):
        return os.path.join(self.name, self.version, 'source')

    def gen_local_path(self):
        if self.lib_type != LibType.BINARY.value:
            raise Exception('Not binary lib.')
        
        return os.path.join(self.name, self.version, 'lib', self.arch, self.config)
    
    def is_equal(self, other):
        return self.name == other.name and self.version == other.version and self.platform == other.platform and \
            self.arch == other.arch and self.config == other.config and self.lib_type == other.lib_type

    def get_zip_file_name(self):
        return self.name + "_lib.zip"

    def get_zip_file_name_for_header(self):
        return self.name + "_lib_header.zip"

    def get_zip_file_name_for_source(self):
        return self.name + '_lib_source.zip'

    def __str__(self):
        return f'{self.name}\t{self.version}\t{self.platform}\t{self.arch}\t{self.config}\t{self.lib_type}\t{self.datetime}'


class LibRepo:
    def __init__(self):
        self.libs: Optional[list[LibData]] = None
        self.__repo_file_key = os.path.join(common.OSS_BASE_PATH, 'repo.json')
        self.__repo_file_key = self.__repo_file_key.replace('\\', '/')

    def pull_repo(self) -> "LibRepo":
        content = common.get_file_obj_2_str(self.__repo_file_key)
        if not content:
            return self

        libs_data = json.loads(content)
        self.libs = [LibData.from_dict(lib) for lib in libs_data]

        return self

    def push_repo(self) -> "LibRepo":
        if not self.libs:
            return self

        libs = [lib.to_dict() for lib in self.libs]
        common.upload_file_obj(self.__repo_file_key, json.dumps(libs))

        return self

    def add_new_lib(self, lib: LibData):
        if not self.libs:
            self.libs = []

        exist = self.find_lib(lib)
        if exist is not None:
            raise Exception('lib already exist.')
        
        self.libs.append(lib)
        self.push_repo()

    def remove_lib(self, lib: LibData):
        exist = self.find_lib(lib)
        if exist is None:
            raise Exception('Not exist')

        self.libs.remove(exist)
        self.push_repo()
        removed_file_keys = [lib.file_key_for_header(), lib.file_key_for_source()]
        if lib.lib_type == LibType.BINARY.value:
            removed_file_keys.append(lib.file_key)

        common.bulk_remove_files(removed_file_keys)

    def bulk_remove_libs(self, libs: List[LibData]):
        if not libs:
            return

        for l in libs:
            exist = self.find_lib(l)
            if exist is None:
                raise Exception(f'Not exist, lib: {l}')

        for l in libs:
            self.libs.remove(l)
        self.push_repo()

        file_keys = [l.file_key() for l in libs if l.lib_type == LibType.BINARY.value]
        name_versions = set()
        for l in libs:
            name_versions.add((l.name, l.version, l.file_key_for_header(), l.file_key_for_source()))
        for name, version, header_file_key, source_file_key in name_versions:
            exist = self.find_first(name, version)
            if not exist:
                file_keys.extend([header_file_key, source_file_key])
        
        common.bulk_remove_files(file_keys)

    @staticmethod
    def __find_lib(lib: LibData, from_libs: list[LibData]) -> tuple[LibData, int]:
        if not from_libs:
            return None, -1
        
        exist = None
        exist_index = -1
        for index, lb in enumerate(from_libs):
            if lb.is_equal(lib):
                if exist is None:
                    exist = lb
                    exist_index = index
                else:
                    raise Exception('Find duplicate lib.')
        return exist, exist_index

    def find_lib(self, lib: LibData) -> LibData:
        exist, _ = LibRepo.__find_lib(lib, self.libs)
        return exist

    def find_first(self, name: str, version: str) -> LibData:
        if not self.libs:
            return None
        
        for lib in self.libs:
            if lib.name == name and lib.version == version:
                return lib

        return None
    
    def query_libs(self, name: str=None, version: str=None, platform: str=None, arch: str=None, config: str=None) -> list[LibData]:
        if not self.libs:
            return []
        
        query_params = {
            'name': name,
            'version': version,
            'platform': platform,
            'arch': arch,
            'config': config,
        }
        results = []
        for lib in self.libs:
            matched = True
            lib_dict = asdict(lib)
            for key, value in query_params.items():
                if value is not None and value != lib_dict[key]:
                    matched = False
            if matched:
                results.append(lib)

        # assert
        ltype = None
        for res in results:
            if ltype is not None and ltype != res.lib_type:
                raise Exception('Dirty repository! lib-type not match.')

        return results

    @staticmethod
    def stringify(libs: list[LibData]):
        table_headers = ['Name', 'Version', 'Platform', 'Architecture', 'Build Config', 'Lib Type', 'Time']
        table_rows = []
        for l in libs:
            cells = [l.name, l.version, l.platform, l.arch or '', l.config or '', l.lib_type or '', l.datetime or '']
            table_rows.append(cells)

        return str(tabulate(table_rows, headers=table_headers))

    def __str__(self):
        def sort_key(lib: LibData):
            return f'{lib.name}-{lib.version}-{lib.platform}-{lib.arch}-{lib.config}-{lib.lib_type}-{lib.datetime}'
        sorted_libs = sorted(self.libs, key=sort_key)

        return LibRepo.stringify(sorted_libs)

def update_lib(local_path: str, header_path: str, source_path: str, lib: LibData):
    def upload_files(dir_path, zip_file_name, file_key):
        if not os.path.exists(dir_path):
            raise Exception(f'{dir_path} not exist!')
        
        zip_file_path = os.path.join(dir_path, zip_file_name)
        common.zip_dir(dir_path, zip_file_path)
        common.upload_file(zip_file_path, file_key)
        os.remove(zip_file_path)

    if not local_path and not header_path and not source_path:
        raise Exception('Invalid parameters. must have lib-path, header-path or source-path')
    
    uploading_lib = lib
    repo = LibRepo()
    repo.pull_repo()
    exist = repo.find_lib(uploading_lib)

    if exist is not None and exist.lib_type != uploading_lib.lib_type:
        raise Exception("lib type not match.")

    if exist is not None:
        repo.remove_lib(exist)

    if local_path:
        upload_files(local_path, uploading_lib.get_zip_file_name(), uploading_lib.file_key())
    if header_path:
        upload_files(header_path, uploading_lib.get_zip_file_name_for_header(), uploading_lib.file_key_for_header())
    if source_path:
        upload_files(source_path, uploading_lib.get_zip_file_name_for_source(), uploading_lib.file_key_for_source())

    repo.add_new_lib(uploading_lib)


def parse_args():
    description = "Upload your lib to cloud"
    parser = argparse.ArgumentParser(description=description)
    sub_parsers = parser.add_subparsers(dest='sub_command')
    add_parser = sub_parsers.add_parser('add')
    add_parser.add_argument('-f', '--binary_folder', help='The library folder you want to upload.')
    add_parser.add_argument('-n', '--name', help='The library name.', required=True)
    add_parser.add_argument('-v', '--version', help='The library version.', required=True)
    add_parser.add_argument('-p', '--platform', help='Platform the library running.', choices=common.available_platforms())
    add_parser.add_argument('-a', '--arch', help='The library architecture.', choices=common.all_available_arches())
    add_parser.add_argument('-c', '--config', help='The library config type.', choices=common.available_config_names())
    add_parser.add_argument('--header', help='The header folder.')
    add_parser.add_argument('--source', help='The source code folder.')

    remove_parser = sub_parsers.add_parser('remove')
    remove_parser.add_argument('-n', '--name', help='The library name.', required=True)
    remove_parser.add_argument('-v', '--version', help='The library version.')
    remove_parser.add_argument('-p', '--platform', help='Platform the library running.', choices=common.available_platforms())
    remove_parser.add_argument('-a', '--arch', help='The library architecture.', choices=common.all_available_arches())
    remove_parser.add_argument('-c', '--config', help='The library config type.', choices=common.available_config_names())

    return parser.parse_args()

def __validate_header_only_lib_args(args) -> tuple[bool, str]:
    if args.binary_folder or args.platform or args.arch or args.config or args.source:
        return False, 'Too many arguments. Only need -n -v -h for Header-Only library.'

    return True, ''

def __validate_source_lib_args(args) -> tuple[bool, str]:
    if args.binary_folder or args.platform or args.arch or args.config:
        return False, 'Too many arguments. Only need -n -v --source for source.'
    
    return True, ''

def __validate_binary_lib_args(args) -> tuple[bool, str]:
    if not args.platform or not args.arch or not args.config:
        return False, 'Too few arguments. Need -p, -a, -c for prebuilt library.'
    
    repo = LibRepo().pull_repo()
    exist = repo.find_first(args.name, args.version)
    if exist is None or not common.file_exist(exist.file_key_for_header()):
        if not args.header:
            return False, 'Need --header!'
    
    return True, ''

def eval_lib_type(args) -> LibType:
    if not args.binary_folder and not args.header and not args.source:
        raise Exception('Must have -p, -h or --source arguments.')

    if args.binary_folder:
        return LibType.BINARY
    
    if args.source:
        return LibType.SOURCE
    
    if args.header:
        return LibType.HEADER_ONLY
    
    raise Exception('Not known lib type')

def validate_args(args) -> tuple[bool, str]:
    lib_type = eval_lib_type(args)

    if lib_type == LibType.BINARY:
        return __validate_binary_lib_args(args)
    
    if lib_type == LibType.SOURCE:
        return __validate_source_lib_args(args)
    
    if lib_type == LibType.HEADER_ONLY:
        return __validate_header_only_lib_args(args)

def __strip_or_none(s):
    if not s:
        return None
    s = s.strip()
    return s if s else None

def wait_user_input(message: str, valid_inputs: tuple[str]) -> str:
    options = '/'.join(valid_inputs)
    while True:
        result = input(f'{message}\nInput {options}: ')
        if result not in valid_inputs:
            logger.error(f'Invalid input. You must input {options}')
        else:
            return result
        
def wait_user_yes_no(message: str) -> bool:
    user_input = wait_user_input(message, ['yes', 'no'])
    if user_input == 'yes':
        return True
    elif user_input == 'no':
        return False
    else:
        raise Exception('invalid input.')
    
def valid_platform_arch(platform, arch):
    if not platform or not arch:
        return True
    
    availables_archs = common.available_arches(platform)
    return arch in availables_archs

def execute_add(args):
    if not valid_platform_arch(args.platform, args.arch):
        logger.info(f'{args.platform} and {args.arch} architecture are not matched.')
        return

    repo = LibRepo().pull_repo()
    lib_with_same_version = repo.find_first(args.name, args.version)
    uploading_lib_type = eval_lib_type(args).value
    header_path = __strip_or_none(args.header)
    source_path = __strip_or_none(args.source)
    overwrite_header = True
    overwrite_source = True
    if lib_with_same_version is not None:
        if lib_with_same_version.lib_type != uploading_lib_type:
            raise Exception(f'The exist version lib type is: {lib_with_same_version.lib_type}, but you want to upload as: {uploading_lib_type}')
        if lib_with_same_version.lib_type == LibType.BINARY.value:
            if header_path and common.file_exist(lib_with_same_version.file_key_for_header()):
                overwrite_header = wait_user_yes_no(f'Headers of {lib_with_same_version.name} ({lib_with_same_version.version}) have exist. Do you want to replace?')
            if source_path and common.file_exist(lib_with_same_version.file_key_for_source()):
                overwrite_source = wait_user_yes_no(f'Source of {lib_with_same_version.name} ({lib_with_same_version.version}) have exist. Do you want to replace?')

    
    lib_data = LibData(name=args.name, version=__strip_or_none(args.version),
                       platform=__strip_or_none(args.platform),
                       arch=__strip_or_none(args.arch),
                       config=__strip_or_none(args.config),
                       lib_type=uploading_lib_type,
                       datetime=str(datetime.now()))
    
    exist = repo.find_lib(lib_data)
    if exist is None:
        used_header_path = header_path if overwrite_header else None
        used_source_path = source_path if overwrite_source else None
        update_lib(args.binary_folder, used_header_path, used_source_path, lib_data)
    else:
        logger.error(f'The same lib with the version already exist: {str(exist)}')

def execute_remove(args):
    lib_repo = LibRepo().pull_repo()
    platform = __strip_or_none(args.platform)
    platforms = [platform] # [platform] if platform else available_platforms()

    all_libs = []
    for p in platforms:
        libs = lib_repo.query_libs(name=__strip_or_none(args.name), version=__strip_or_none(args.version), platform=p, 
                                    arch=__strip_or_none(args.arch), config=__strip_or_none(args.config))
        if libs:
            all_libs.extend(libs)

    if not all_libs:
        logger.error("Library not found!")
        return

    message = LibRepo.stringify(all_libs)
    confirm = wait_user_yes_no(f'The following libraries will be removed permanently from cloud!\n{message}')
    if confirm:
        lib_repo.bulk_remove_libs(all_libs)
    else:
        logger.info("Remove operation is cancelled!")

def lib_repo():
    args = parse_args()

    if args.sub_command == 'add':
        valid, msg = validate_args(args)
        if valid:
            execute_add(args)
        else:
            raise Exception(msg)
    elif args.sub_command == 'remove':
        execute_remove(args)

if __name__ == "__main__":
    lib_repo()


