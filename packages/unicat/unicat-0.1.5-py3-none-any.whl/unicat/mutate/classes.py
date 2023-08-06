from ..class_ import UnicatClass
from ..error import UnicatError


def create_class(unicat, properties):
    success, result = unicat.api.call("/classes/create", properties)
    if not success:
        raise UnicatError("create_class", result)
    return UnicatClass(unicat, result["class"])


def modify_class(unicat, class_, properties):
    success, result = unicat.api.call(
        "/classes/modify",
        {**properties, "class": class_.gid},
    )
    if not success:
        raise UnicatError("modify_class", result)
    return UnicatClass(unicat, result["class"])


def modify_class_modify_layout(unicat, class_, layout_properties):
    success, result = unicat.api.call(
        "/classes/layouts/modify",
        {**layout_properties, "class": class_.gid},
    )
    if not success:
        raise UnicatError("modify_class_modify_layout", result)
    return UnicatClass(unicat, result["class"])


def commit_class(unicat, new_or_working_copy):
    success, result = unicat.api.call(
        "/classes/commit", {"class": new_or_working_copy.gid}
    )
    if not success:
        raise UnicatError("commit_class", result)
    if (
        result["class"] != new_or_working_copy.gid
        and new_or_working_copy.gid in unicat.api.data["classes"]
    ):
        del unicat.api.data["classes"][new_or_working_copy.gid]
    return UnicatClass(unicat, result["class"])


def delete_class(unicat, class_):
    success, result = unicat.api.call("/classes/delete", {"class": class_.gid})
    if not success:
        raise UnicatError("delete_class", result)
    if class_.gid in unicat.api.data["classes"]:
        del unicat.api.data["classes"][class_.gid]
    return True
