import boto3
import os
import requests
import hashlib
import json
from nvos import login
import logging

# 导入全局日志记录器
logger = logging.getLogger(__name__)
daemon_network = "https://nvos-toolchain-dev.nioint.com"
bucket_name = "d-ds-dpt-ndtc-dev"
aws_ak = "AKIATX65TOAHMPVETCXW"
aws_sk = "PI8FWjnhrt1qdLJjaCYzmgg8ADatTjbmaTg1RoZB"
aws_region = "cn-north-1"

def upload_client_script():
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    bucket = s3.Bucket(bucket_name)
    file_path = "/Users/andre.zhao/PycharmProjects/nvos-script/dist/nvosscript-1.0.1-py3-none-any.whl"
    file_name = "/nvos-script/dist/nvosscript-1.0.1-py3-none-any.whl"
    bucket.upload_file(file_path, file_name)

def upload_file(file_path_list, project_space_list):
    logger.info(f"upload_file execute ")
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    for project_space in project_space_list:
        flag = False
        for temp in filter_upload_dir():
            if temp in project_space["project_space"]:
                flag = True
                break
        if not flag:
            continue
        for file_path in file_path_list:
            if project_space["project_space"] in file_path["file_path"]:
                file_name = "%s/%s/%s" % (login.get_user_id(), md5(project_space["git_branch"], project_space["project_space"]),
                                            file_path["file_path"][file_path["file_path"]
                                          .find(os.path.basename(project_space["project_space"])):])
                file_name = file_name.replace("\\", "/")
                bucket = s3.Bucket(bucket_name)
                local_file_path = file_path["file_path"]
                logger.info(f"upload file ossUrl:{file_name} file local full path:{local_file_path}")
                bucket.upload_file(local_file_path, file_name)


def download_file(project_space):
    s3 = boto3.resource('s3', region_name=aws_region, aws_access_key_id=aws_ak,
                        aws_secret_access_key=aws_sk)
    bucket = s3.Bucket(bucket_name)
    for file in project_space["changedFileList"]:
        ossURL = file["ossURL"]
        fileFullPath = file["fileFullPath"]
        try:
            bucket.download_file(ossURL, fileFullPath)
        except Exception:
            logger.info(f"this file sync fail  ossURL:{ossURL} fileFullPath:{fileFullPath}" )
        else:
            logger.info(f"this file sync success  ossURL:{ossURL} fileFullPath:{fileFullPath}")

def save_workspace(workspace_path, project_list):
    url = "%s%s" % (daemon_network, "/workspace/add")
    post_param = {"userId": login.get_user_id(), "fileDirectory": workspace_path, "projectSpaceList": project_list}
    return post_data(url, post_param)


def pull_workspace(workspace, project_list):
    url = "%s%s" % (daemon_network, "/workspace/getChangedFiles")
    post_param = {"userId": login.get_user_id(), "fileDirectory": workspace,"projectSpaceList": project_list}
    return post_data(url, post_param)


def post_data(url, params):
    headers = {"content-type": "application/json"}
    logger.info(f'request url:{url} params:{params}')
    response = requests.post(url, headers=headers, data=json.dumps(params))
    logger.info(f"response status_code: {response.status_code} text: {response.text} \n content:{response.content}")
    if response.status_code == 200:
        response_data = json.loads(response.text)["data"]
        return response_data
    return {}


def md5(git_branch, project_space):
    string = "%s%s" % (git_branch, project_space)
    hash_object = hashlib.md5(string.encode())
    md5_hash = hash_object.hexdigest()
    return md5_hash


def filter_upload_dir():
    return ["ecus", "platform"]