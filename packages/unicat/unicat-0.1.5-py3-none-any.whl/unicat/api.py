import requests
import json
import os
from pathlib import Path
import logging
from .utils import hash_data

logger = logging.getLogger("unicat.api")


class UnicatApi:
    """Connect to a Unicat project and have fun.

    Base usage:

        ccapi = UnicatApi(CONFIG["url"], CONFIG["project_gid"], CONFIG["local_asset_folder"])
        success, result = ccapi.connect(CONFIG["secret_api_key"])

        success, result = ccapi.call("/records/root", {"language": "en"})
        root_record = ccapi.data["records"][result["root"]]

    """

    def __init__(self, base_url, project_gid, asset_folder=None):
        self._base_url = base_url
        self._project_gid = project_gid
        self._asset_folder = asset_folder
        if self._asset_folder:
            os.makedirs(str(self._asset_folder), exist_ok=True)
        self._globalapi_url = base_url + "/api"
        self._api_url = base_url + "/api/p/" + project_gid
        self._sync_url = base_url + "/sync"
        self._dam_url = base_url + "/dam/p/" + project_gid
        self._auth_header = None
        self.cc_version = ""
        self.cc_cursor = 0
        self.project_gid = project_gid
        self.project_cursor = 0
        self.data = {
            "cc.users": {},
            "cc.projects": {},
            "cc.projects_members": {},
            "cc.languages": {},
            "records": {},
            "definitions": {},
            "classes": {},
            "fields": {},
            "layouts": {},
            "assets": {},
            "queries": {},
        }

    def _reset_data(self):
        self.data["cc.users"].clear()
        self.data["cc.projects"].clear()
        self.data["cc.projects_members"].clear()
        self.data["cc.languages"].clear()
        self.data["records"].clear()
        self.data["definitions"].clear()
        self.data["classes"].clear()
        self.data["fields"].clear()
        self.data["layouts"].clear()
        self.data["assets"].clear()
        self.data["queries"].clear()

    def update_jwt(self, JWT):
        if not JWT:
            self._auth_header = None
        else:
            self._auth_header = {"Authorization": f"Bearer {JWT}"}

    def connect(self, secret_api_key):
        self._reset_data()
        data = {"api_key": secret_api_key}
        return self._call("post", "/auth", data)

    def init(self):
        self._reset_data()
        return self._call("get", "/init")

    def call(self, endpoint, data=None, method="post"):
        return self._call(method, endpoint, data=data)

    def upload(self, endpoint, data=None, localfilepath=None):
        return self._call_upload(endpoint, data=data, filepath=localfilepath)

    def publish(self, asset):
        return self._call_dam("/publish", asset)

    def transform(self, asset, options=None):
        if options and "key" not in options:
            options["key"] = hash_data(options)
        return self._call_dam("/transform", asset, options=options)

    def download(self, asset, pathname=None, updated_on=None):
        if not self._asset_folder:
            return False
        success, result = self.publish(asset)
        if not success:
            return None
        if not pathname:
            path = os.path.dirname(asset["pathname"])
            name = os.path.basename(result["public_url"])
            pathname = path + "/" + name
        elif not pathname.startswith("/"):
            path = os.path.dirname(asset["pathname"])
            pathname = path + "/" + pathname
        return self._call_media(result["public_url"], pathname, updated_on=updated_on)

    def download_transformed(self, asset, options=None, pathname=None, updated_on=None):
        if not self._asset_folder:
            return False
        success, result = self.transform(asset, options)
        if not success:
            return None
        if not pathname:
            path = os.path.dirname(asset["pathname"])
            name = os.path.basename(result["public_url"])
            pathname = path + "/" + name
        elif not pathname.startswith("/"):
            path = os.path.dirname(asset["pathname"])
            pathname = path + "/" + pathname
        return self._call_media(result["public_url"], pathname, updated_on=updated_on)

    def sync(self):
        data = {
            "cc_cursor": self.cc_cursor,
            "project": self._project_gid,
            "cursor": self.project_cursor,
        }
        success, result = self._call_sync("post", "/get", data=data)
        if not success:
            return None
        self.handle_sync_data(result["sync"])

    def project_member_key(self, project_member):
        return f"{project_member['project_gid']}/{project_member['user_gid']}"

    def _fetch_syncdataitem(self, syncdataitem):
        type_ = syncdataitem["data_type"]
        key = syncdataitem["data_key"]
        if type_ == "cc.projects_members":
            project, member = key.split("/")
            success, result = self.call(  # note the // - global api
                "//members/get", {"project": project, "member": member}
            )
            return success
        map_calls = {
            "cc.users": ["//users/get", "user"],  # note the // - global api
            "cc.projects": [
                "//projects/get",
                "project",
            ],  # note the // - global api
            "assets": ["/assets/get", "asset"],
            "classes": ["/classes/get", "class"],
            "definitions": ["/definitions/get", "definition"],
            "fields": ["/fields/get", "field"],
            "layouts": ["/layouts/get", "layout"],
            "queries": ["/queries/get", "query"],
            "records": ["/records/get", "record"],
        }
        map_call = map_calls[type_]
        success, result = self.call(map_call[0], {map_call[1]: key})
        return success

    def handle_sync_data(self, syncdatalist):
        # result contains a list of cursor/action/data_type/data_key
        # handle each one, updating our cursors as we go
        for item in syncdatalist:
            # skip lagging syncs (older than our latest cursors)
            if item["action"] != "RESTORE END":
                if item["type"] == "cc":
                    if self.cc_cursor >= item["cursor"]:
                        continue
                else:
                    if self.project_cursor >= item["cursor"]:
                        continue
            if item["data_type"] == "cc.version":
                if item["data_key"] != self.cc_version:
                    # alert! version-change mid-program!
                    print("Server version changed!")
                self.cc_version = item["data_key"]
            elif item["action"] == "BACKUP START":
                print("Server database backup started!")
            elif item["action"] == "BACKUP END":
                print("Server database backed up!")
            elif item["action"] == "RESTORE START":
                print("Server database restore  started!")
            elif item["action"] == "RESTORE END":
                print("Server database restored from backup!")
                self.init()
            elif item["action"] == "DELETE":
                # use pop, not del, auto-handles items that aren't in our store
                self.data[item["data_type"]].pop(item["data_key"], None)
            elif item["action"] == "INSERT":
                # we're only interested in inserts that affect our data
                # so project-members for our project should fetch the new
                # membership, but also the new members
                # we're also interested in any base-data for definitions,
                # classes, fields, layouts, and queries
                # NOTE: fetching data auto-updates our local data-store
                if item["data_type"] == "cc.projects_members":
                    project_gid, user_gid = item["data_key"].split("/")
                    if project_gid == self._project_gid:
                        success = self._fetch_syncdataitem(item)
                elif item["data_type"] in (
                    "definitions",
                    "classes",
                    "fields",
                    "layouts",
                    "queries",
                ):
                    success = self._fetch_syncdataitem(item)
            elif item["action"] == "UPDATE":
                # we're only interested in data we already have locally
                if item["data_key"] in self.data[item["data_type"]]:
                    success = self._fetch_syncdataitem(item)
            # always update local cursors
            if item["type"] == "cc":
                self.cc_cursor = item["cursor"]
            else:
                self.project_cursor = item["cursor"]

    def _json_response(self, jsontext):
        try:
            jsondata = json.loads(jsontext)
        except:
            logger.info(f"500 Server error - Invalid response '''\n{jsontext}\n'''")
            return self._response_error(
                500, "Invalid response", info={"response.text": jsontext}
            )

        if "files" in jsondata["data"]:
            jsondata["result"]["data/files"] = jsondata["data"]["files"]
            del jsondata["data"]["files"]

        if jsondata["success"]:
            for key, value in jsondata["result"].items():
                if key == "cc.version":
                    self.cc_version = value
                elif key == "cc.cursor":
                    self.cc_cursor = value
                elif key == "cursor":
                    self.project_cursor = value
            for key, values in jsondata["data"].items():
                if key == "cc.projects_members":  # a list, not a dict
                    self.data[key].update(
                        {self.project_member_key(value): value for value in values}
                    )
                else:
                    self.data[key].update(values)
            return True, jsondata["result"]
        else:
            return False, jsondata["result"]

    def _response_error(self, code, message, info=None):
        return False, {"code": int(code), "message": message, "info": info}

    def _call(self, method, endpoint, data=None):
        if endpoint.startswith("//"):
            url = self._globalapi_url + endpoint[1:]
        else:
            url = self._api_url + endpoint
        requestmethod = getattr(requests, method)
        if method == "post" and data is None:
            data = {}
        response = requestmethod(url, headers=self._auth_header, json=data)
        logger.info(f"{response.status_code} {url}")
        logger.debug(
            f"{response.status_code} {url} REQUEST {json.dumps(data)} RESPONSE {response.text}"
        )
        if "Authorization" in response.headers:
            self.update_jwt(response.headers["Authorization"])
        if "WWW-Authenticate" in response.headers:
            self.update_jwt(None)
        jsontext = response.text
        return self._json_response(jsontext)

    def _call_sync(self, method, endpoint, data=None):
        url = self._sync_url + endpoint
        requestmethod = getattr(requests, method)
        if method == "post" and data is None:
            data = {}
        response = requestmethod(url, headers=self._auth_header, json=data)
        logger.info(f"{response.status_code} {url}")
        logger.debug(
            f"{response.status_code} {url} REQUEST {json.dumps(data)} RESPONSE {response.text}"
        )
        if "Authorization" in response.headers:
            self.update_jwt(response.headers["Authorization"])
        if "WWW-Authenticate" in response.headers:
            self.update_jwt(None)
        jsontext = response.text
        return self._json_response(jsontext)

    def _call_upload(self, endpoint, data, filepath):
        filesize = os.path.getsize(filepath)
        if filesize > 10_000_000:
            logger.info(f"413 Request Entity Too Large '{filepath}' ({filesize})")
            print()
            print(filepath, filesize)
            print()
            return self._response_error(413, "Request Entity Too Large", info=None)
        if not data:
            data = {}
        url = self._api_url + endpoint
        files = {"upload_file": (os.path.basename(filepath), open(filepath, "rb"))}
        response = requests.post(url, headers=self._auth_header, data=data, files=files)
        logger.info(f"{response.status_code} {url}")
        logger.debug(
            f"{response.status_code} {url} REQUEST {json.dumps(data)} FILE {files['upload_file'][0]} RESPONSE {response.text}"
        )
        if "Authorization" in response.headers:
            self.update_jwt(response.headers["Authorization"])
        if "WWW-Authenticate" in response.headers:
            self.update_jwt(None)
        jsontext = response.text
        return self._json_response(jsontext)

    def _call_dam(self, endpoint, asset, options=None):
        gid = asset["gid"]
        version = asset["version"]
        _, ext = os.path.splitext(asset["name"])
        url = self._dam_url + endpoint + f"/{gid}~{version}{ext}"
        if options:
            url += "/" + "/".join(
                f"{str(key)}={str(value)}" for key, value in options.items()
            )
        response = requests.get(url, headers=self._auth_header)
        logger.info(f"{response.status_code} {url}")
        logger.debug(
            f"{response.status_code} {url} REQUEST <get> RESPONSE {response.text}"
        )
        if "WWW-Authenticate" in response.headers:
            self.update_jwt(None)
        jsontext = response.text
        return self._json_response(jsontext)

    def _call_media(self, public_url, pathname, updated_on=None):
        if not self._asset_folder:
            return False
        while pathname.startswith("/") or pathname.startswith("\\"):
            pathname = pathname[1:]
        abs_pathname = Path(self._asset_folder, pathname)
        if os.path.isfile(abs_pathname):
            if updated_on is None:
                return pathname
            if updated_on <= os.path.getmtime(abs_pathname):
                return pathname
        with requests.get(public_url, stream=True) as response:
            logger.info(f"{response.status_code} {public_url}")
            logger.debug(
                f"{response.status_code} {public_url} REQUEST <get> RESPONSE <bytes> INTO {abs_pathname}"
            )
            if response.status_code != 200:
                return False
            abs_path = os.path.dirname(abs_pathname)
            os.makedirs(abs_path, exist_ok=True)
            with open(abs_pathname, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        return pathname
