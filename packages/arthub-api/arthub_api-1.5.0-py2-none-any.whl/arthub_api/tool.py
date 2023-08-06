"""
arthub_api.depot
~~~~~~~~~~~~~~

This module provides the operation interface of the ArtHub Blade tool service module
"""
import logging

from . import utils
from . import models
import os

class Storage(object):
    def __init__(self, open_api):
        r"""Used to perform operations to ArtHub Blade tool service, such as create tools.

        :param open_api: class: arthub_api.API.
        """
        self.open_api = open_api

    def fuzzy_match_account(self, name_to_match):
        r"""Fuzzy match an account of person or department.

        :param name_to_match: str. name to match with person or department. Example: "joeydi" or "IEG Global".

        :rtype: arthub_api.Result
                arthub_api.Result.data: list<dict>
                {
                    account_name: str. Example: "joeyding",
                    type: str. "department" or "person",
                }

        """

    def get_account_detail(self, account_name, ):
        r"""Fuzzy match an account of person or department.

        :param name_to_match: str. name to match with person or department. Example: "joeydi" or "IEG Global".

        :rtype: arthub_api.Result
                arthub_api.Result.data: list<dict>
                {
                    account_name: str. Example: "joeyding".
                    type: str. "department" or "person".
                }
        """


    def download_node(self, asset_hub, node, local_dir_path, download_filters, same_name_override,
                      download_temporary_dir_path=None):
        # serially
        task = _DownloadTask(self, asset_hub, node, local_dir_path, download_filters, same_name_override,
                             download_temporary_dir_path=download_temporary_dir_path)
        return _execute_transfer_tasks_concurrently(task)

    def upload_node(self, asset_hub, remote_dir_id, local_path, same_name_override,
                    need_convert, tags_to_create, description):
        # serially
        task = _UploadTask(self, asset_hub, remote_dir_id, local_path, same_name_override, need_convert, tags_to_create,
                           description)
        return _execute_transfer_tasks_concurrently(task)

    def get_node_by_path(self, asset_hub, remote_node_path, simplified_meta=False):
        r"""Get node info by path in depot.

        :param asset_hub: str. Example: "trial".
        :param remote_node_path: str. remote node path to query info. Example: "sdk/1/2".
        :param simplified_meta: (optional) bool. Just basic meta, lower bandwidth consumption.

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when query successful
                arthub_api.Result.is_succeeded(): False when query fail, or node doesn't exist
                arthub_api.Result.data: dic. info of dir
        """

        res = self.open_api.depot_get_root_id(asset_hub)
        if not res.is_succeeded():
            r_ = models.failure_result("get depot root id failed, %s" % res.error_message())
            r_.set_data({"not_exist": False})
            return r_
        root_id = res.first_result()
        res = self.open_api.depot_get_node_brief_by_path(asset_hub, root_id, remote_node_path,
                                                         simplified_meta=simplified_meta)
        if not res.is_succeeded():
            r_ = models.failure_result("get node info by \"%s\" failed, %s" % (
                remote_node_path, res.error_message()))
            r_.set_data({"not_exist": res.is_node_not_exist()})
            return r_
        return models.success_result(res.first_result())

    def download_by_id(self, asset_hub, remote_node_id, local_dir_path, download_filters=[], same_name_override=True,
                       download_temporary_dir_path=None):
        r"""Download asset or directory by id to local directory.

        :param asset_hub: str. Example: "trial".
        :param remote_node_id: int. Example: 110347249755230.
        :param local_dir_path: str. Download target directory path. Example: "D://".
        :param download_filters: (optional) list<query_filter (dict) >. Example: [{"meta": "file_format",
                                                                                "condition": "x != png"}].
                {
                    "meta": filters meta,
                    "condition": filters condition
                }
        :param same_name_override: (optional) bool. When a file with the same name exists in the target path,
                                                    add new version
        :param download_temporary_dir_path: (optional) str. Directory where the downloaded temporary files are stored,
                                                            if None, the stored in local_dir_path

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when the download successful
                arthub_api.Result.is_succeeded(): False when the download fail
                arthub_api.Result.data: list<string>. path of downloaded file and dir, the first element is root path
        """

        res = self.open_api.depot_get_node_brief_by_ids(asset_hub, [remote_node_id], simplified_meta=True)
        if not res.is_succeeded():
            return models.failure_result("get node info by %d failed, %s" % (remote_node_id, res.error_message()))
        return self.download_node(asset_hub, res.first_result(), local_dir_path, download_filters, same_name_override,
                                  download_temporary_dir_path)

    def download_by_path(self, asset_hub, remote_node_path, local_dir_path, download_filters=[],
                         same_name_override=True, download_temporary_dir_path=None):
        r"""Download asset or directory by path to local directory.

        :param asset_hub: str. Example: "trial".
        :param remote_node_path: str. Example: "sdk_test/storage_test/jpg&png".
        :param local_dir_path: str. Download target directory path. Example: "D://".
        :param download_filters: (optional) list<query_filter (dict) >. Example: [{"meta": "file_format", "condition": "x != png"}].
                {
                    "meta": filters meta,
                    "condition": filters condition
                }
        :param same_name_override: (optional) bool. When a file with the same name exists in the target path, add new
                                                    version
        :param download_temporary_dir_path: (optional) str. Directory where the downloaded temporary files are stored,
                                                            if None, the stored in local_dir_path

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when the download successful
                arthub_api.Result.is_succeeded(): False when the download fail
                arthub_api.Result.data: list<string>. path of downloaded file and dir, the first element is the root path
        """

        res = self.get_node_by_path(asset_hub, remote_node_path, simplified_meta=True)
        if not res.is_succeeded():
            return models.failure_result("get node \"%s\" info failed, %s" % (remote_node_path,
                                                                              res.error_message()))

        return self.download_node(asset_hub, res.data, local_dir_path, download_filters, same_name_override,
                                  download_temporary_dir_path)

    def upload_to_directory_by_id(self, asset_hub, remote_dir_id, local_path, same_name_override=True,
                                  need_convert=True, tags_to_create=None, description=None):
        r"""Upload file or directory remote directory, with remote directory id.

        :param asset_hub: str. Example: "trial".
        :param remote_dir_id: int. Example: 110347250886196.
        :param local_path: str. Example: "D:/test/python/1.mp4".
        :param same_name_override: (optional) bool. When a file with the same name exists in the target path, add new
                                                    version
        :param need_convert: (optional) bool. Convert asset after upload (Effective for specific formats, such as video,
                                              model)
        :param tags_to_create: (optional) str[]. Create tags after upload. Example: ["Christmas", "Gun"]
        :param description: (optional) str. Add asset description. Example: "Gun"

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when the upload successful
                arthub_api.Result.is_succeeded(): False when the upload fail
                arthub_api.Result.data: list<id>. id of uploaded file and dir, the first element is the root path
        """

        res = self.open_api.depot_get_node_brief_by_ids(asset_hub, [remote_dir_id], simplified_meta=True)
        if not res.is_succeeded():
            return models.failure_result("get node info by %d failed, %s" % (remote_dir_id, res.error_message()))

        if not self.is_node_directory(res.first_result()):
            return models.failure_result("target node %d is not a directory" % remote_dir_id)

        return self.upload_node(asset_hub, res.first_result()["id"], local_path, same_name_override, need_convert,
                                tags_to_create, description)

    def upload_to_directory_by_path(self, asset_hub, remote_dir_path, local_path, same_name_override=True,
                                    need_convert=True, tags_to_create=None, description=None):
        r"""Upload file or directory remote directory, with remote directory id.

        :param asset_hub: str. Example: "trial".
        :param remote_dir_path: str. Example: "sdk_test/1/2".
        :param local_path: str. Example: "D:/test/python/1.mp4".
        :param same_name_override: (optional) bool. When a file with the same name exists in the target path, add new
                                                    version
        :param need_convert: (optional) bool. Convert asset after upload (Effective for specific formats, such as video,
                                              model)
        :param tags_to_create: (optional) bool. Create tags after upload. Example: ["Christmas", "Gun"]
        :param description: (optional) str. Add asset description. Example: "Gun"

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when the upload successful
                arthub_api.Result.is_succeeded(): False when the upload fail
                arthub_api.Result.data: list<id>. id of uploaded file and dir, the first element is the root path
        """

        res = self.create_directory_by_path(asset_hub, remote_dir_path)
        if not res.is_succeeded():
            return res

        return self.upload_node(asset_hub, res.data, local_path, same_name_override, need_convert,
                                tags_to_create, description)

    def create_directory_by_path(self, asset_hub, remote_dir_path):
        r"""Create directory by path in depot.

        :param asset_hub: str. Example: "trial".
        :param remote_dir_path: str. remote dir path to create. Example: "sdk/1/2".

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when create successful or a dir with the same name already exists
                arthub_api.Result.is_succeeded(): False when create fail
                arthub_api.Result.data: int. id of dir
        """

        res = self.open_api.depot_get_root_id(asset_hub)
        if not res.is_succeeded():
            return models.failure_result("get depot root id failed, %s" % res.error_message())
        root_id = res.first_result()

        remote_dir_path = remote_dir_path.replace('\\', '/')
        dir_path_list = utils.splite_path(remote_dir_path)
        if len(dir_path_list) == 0:
            return root_id

        # try to get exist path
        res = self.open_api.depot_get_node_brief_by_path(asset_hub, root_id, remote_dir_path)
        if res.is_succeeded():
            exist_node = res.first_result()
            if Storage.is_node_directory(exist_node):
                return models.success_result(exist_node["id"])
            else:
                return models.failure_result(
                    "target path \"%s\" isn't a directory but a %s" % (remote_dir_path, exist_node["type"]))
        if not res.is_node_not_exist():
            return models.failure_result(
                "get path \"%s\" info failed, %s" % (remote_dir_path, res.error_message()))

        # create root directory under depot
        project_name = dir_path_list[0]
        res = self.open_api.depot_create_project(asset_hub, project_name, root_id)
        if not res.is_succeeded():
            return models.failure_result("create project \"%s\" failed, %s" % (project_name, res.error_message()))
        current_dir_id = res.direct_result

        dir_path_list.pop(0)
        for name in dir_path_list:
            res = self.open_api.depot_create_directory(asset_hub, [{
                "parent_id": current_dir_id,
                "name": name,
                "allowed_rename": True,
                "return_existing_id": True
            }])
            if not res.is_succeeded():
                return models.failure_result("create directory \"%s\" under %d failed, %s" % (
                    name, current_dir_id, res.error_message()))
            current_dir_id = res.direct_result

        return models.success_result(current_dir_id)

    def delete_node_by_path(self, asset_hub, remote_node_path):
        r"""Upload file or directory remote directory, with remote directory id.

        :param asset_hub: str. Example: "trial".
        :param remote_node_path: str. remote node path tp remove (dir or file). Example: "sdk_test/1/to_remove".

        :rtype: arthub_api.Result
                arthub_api.Result.is_succeeded(): True when the deletion successful or the node doesn't exist
                arthub_api.Result.is_succeeded(): False when the deletion fail
                arthub_api.Result.data: int. id of deleted node
        """

        res = self.get_node_by_path(asset_hub, remote_node_path, simplified_meta=True)
        if not res.is_succeeded():
            if res.data and res.data.get("not_exist"):
                return models.success_result(-1)
            return res

        node_id = res.data["id"]
        api_res = self.open_api.depot_delete_node_by_ids(asset_hub, [
            node_id
        ])
        if not api_res.is_succeeded():
            return models.failure_result("delete node %d failed, %s" % (
                node_id, api_res.error_message()))
        return models.success_result(node_id)
