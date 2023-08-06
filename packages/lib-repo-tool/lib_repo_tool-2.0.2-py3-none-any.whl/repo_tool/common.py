import os
import oss2
import zipfile
import sys
import requests
from urllib import parse
from dataclasses import dataclass

# OSS_BASE_PATH = 'arcsite-x-libs-repo'
OSS_BASE_PATH = 'arcsite-x-libs-repo-2.0'

@dataclass
class BucketInfo:
    endpoint: str
    name: str
    access_key_id: str
    access_key_secret: str
    

BucketInfo.endpoint = os.getenv('file_bucket_endpoint')
BucketInfo.name = os.getenv('file_bucket_name')
BucketInfo.access_key_id = os.getenv('file_bucket_access_key_id')
BucketInfo.access_key_secret = os.getenv('file_bucket_access_key_secret')


BUCKET_OBJECT = None


def get_bucket() -> oss2.Bucket:
    global BUCKET_OBJECT

    if BUCKET_OBJECT:
        return BUCKET_OBJECT

    if not BucketInfo.endpoint or not BucketInfo.name or not BucketInfo.access_key_id or not BucketInfo.access_key_secret:
        raise Exception('File bucket info not complete.')

    auth = oss2.Auth(BucketInfo.access_key_id, BucketInfo.access_key_secret)
    BUCKET_OBJECT = oss2.Bucket(auth, BucketInfo.endpoint, BucketInfo.name)
    
    return BUCKET_OBJECT

def zip_dir(files_dir, dest_file):
    with zipfile.ZipFile(dest_file, 'w', zipfile.ZIP_DEFLATED, True) as ziph:
        _, zip_name = os.path.split(dest_file)
        for root, dirs, files in os.walk(files_dir):
            for f in files:
                fu = f
                if fu.startswith('.') or os.path.join(root, fu) == dest_file:
                    continue
                p = os.path.join(root, fu)
                rel = os.path.relpath(os.path.join(root, fu), files_dir)
                ziph.write(p, rel)
                

def unzip_file(zip_file, dest_dir):
    with zipfile.ZipFile(zip_file, 'r', zipfile.ZIP_DEFLATED, True) as z:
        z.extractall(dest_dir)


def upload_file(file_path, file_key):
    with open(file_path, 'rb') as f:
        get_bucket().put_object(file_key, f)


def remove_file(file_key):
    get_bucket().delete_object(file_key)


def bulk_remove_files(file_keys):
    get_bucket().batch_delete_objects(file_keys)


def file_exist(file_key)->bool:
    return get_bucket().object_exists(file_key)


# def download_file(file_key, to_path):
    # get_bucket().get_object_to_file(file_key, to_path)

def download_file(file_key, to_path):
    url: str = get_bucket().sign_url('GET', file_key, 60 * 30)
    split_result = parse.urlsplit(url)
    new_result = parse.SplitResult('http', 'oss.lib-repo.dev.arcsiteapp.cn', split_result.path, split_result.query, split_result.fragment)

    new_url = parse.urlunsplit(split_result)
    r = requests.get(new_url, stream=True, timeout=10)
    with open(to_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024*10):
            if (chunk):
                f.write(chunk)


def get_file_obj_2_str(file_key, not_exist_exception=False):
    try:
        result = get_bucket().get_object(file_key).read()
        return result
    except oss2.exceptions.NoSuchKey as e:
        if not_exist_exception:
            raise e
        else:
            return None


def upload_file_obj(file_key: str, file_obj):
    get_bucket().put_object(file_key, file_obj)


def is_legal_local_lib_dir(local_path: str, platform: str):
    p = os.path.join(local_path, platform)
    return os.path.exists(p) and os.path.isdir(p)


def get_platform_name() -> str:
    p = sys.platform
    if p.startswith('linux'):
        return 'linux'
    if p.startswith('win32'):
        return 'windows'
    if p.startswith('darwin'):
        return 'macos'


def available_platforms():
    return ['windows', 'macos', 'linux', 'ios', 'android','ios_simulator']


def available_arches(platform: str):
    data = {
        "windows": ['x64'],
        'macos': ['arm64', 'x64'],
        'linux': [],
        'ios': [],
        'android': ['arm64-v8a'],
        'ios_simulator': []
    }

    return data.get(platform, None)

def default_arch_for_platform(platform: str):
    pass

def all_available_arches():
    all_arches = []
    for p in available_platforms():
        arches = available_arches(p)
        if arches:
            all_arches.extend(arches)

    return all_arches


def available_config_names():
    return ['release', 'debug']
