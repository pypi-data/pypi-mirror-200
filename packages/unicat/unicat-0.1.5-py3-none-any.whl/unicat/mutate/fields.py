from ..field import UnicatField
from ..error import UnicatError


def create_field(unicat, properties):
    success, result = unicat.api.call("/fields/create", properties)
    if not success:
        raise UnicatError("create_field", result)
    return UnicatField(unicat, result["field"])


def modify_field(unicat, field, properties):
    success, result = unicat.api.call(
        "/fields/modify",
        {**properties, "field": field.gid},
    )
    if not success:
        raise UnicatError("modify_field", result)
    return UnicatField(unicat, result["field"])


def commit_field(unicat, new_or_working_copy):
    success, result = unicat.api.call(
        "/fields/commit", {"field": new_or_working_copy.gid}
    )
    if not success:
        raise UnicatError("commit_field", result)
    if (
        result["field"] != new_or_working_copy.gid
        and new_or_working_copy.gid in unicat.api.data["fields"]
    ):
        del unicat.api.data["fields"][new_or_working_copy.gid]
    return UnicatField(unicat, result["field"])


def delete_field(unicat, field):
    success, result = unicat.api.call("/fields/delete", {"field": field.gid})
    if not success:
        raise UnicatError("delete_field", result)
    if field.gid in unicat.api.data["fields"]:
        del unicat.api.data["fields"][field.gid]
    return True
