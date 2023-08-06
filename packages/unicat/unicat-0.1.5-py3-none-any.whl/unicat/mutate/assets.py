from ..asset import UnicatAsset
from ..error import UnicatError


def upload_asset(unicat, localfilepath, folderasset):
    success, result = unicat.api.upload(
        "/assets/upload", {"parent": folderasset.gid}, localfilepath
    )
    if not success:
        raise UnicatError("upload_asset", result)
    return UnicatAsset(unicat, result["asset"])


def create_asset(unicat, parentasset, name):
    success, result = unicat.api.call(
        "/assets/create", {"parent": parentasset.gid, "name": name}
    )
    if not success:
        raise UnicatError("create_asset", result)
    return UnicatAsset(unicat, result["asset"])


def update_asset(unicat, asset, properties):
    success, result = unicat.api.call(
        "/assets/update",
        {**properties, "asset": asset.gid},
    )
    if not success:
        raise UnicatError("update_asset", result)
    return UnicatAsset(unicat, result["asset"])


def delete_asset(unicat, asset):
    success, result = unicat.api.call("/assets/delete", {"asset": asset.gid})
    if not success:
        raise UnicatError("delete_asset", result)
    return UnicatAsset(unicat, result["asset"])


def undelete_asset(unicat, asset):
    success, result = unicat.api.call("/assets/undelete", {"asset": asset.gid})
    if not success:
        raise UnicatError("undelete_asset", result)
    return UnicatAsset(unicat, result["asset"])


def permanent_delete_asset(unicat, asset):
    success, result = unicat.api.call("/assets/permanent_delete", {"asset": asset.gid})
    if not success:
        raise UnicatError("permanent_delete_asset", result)
    if asset.gid in unicat.api.data["assets"]:
        del unicat.api.data["assets"][asset.gid]
    return True
