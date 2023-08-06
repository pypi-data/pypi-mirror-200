from ..definition import UnicatDefinition
from ..error import UnicatError


def create_definition(unicat, properties):
    success, result = unicat.api.call("/definitions/create", properties)
    if not success:
        raise UnicatError("create_definition", result)
    return UnicatDefinition(unicat, result["definition"])


def modify_definition(unicat, definition, properties):
    success, result = unicat.api.call(
        "/definitions/modify",
        {**properties, "definition": definition.gid},
    )
    if not success:
        raise UnicatError("modify_definition", result)
    return UnicatDefinition(unicat, result["definition"])


def modify_definition_modify_layout(unicat, definition, layout_properties):
    success, result = unicat.api.call(
        "/definitions/layouts/modify",
        {**layout_properties, "definition": definition.gid},
    )
    if not success:
        raise UnicatError("modify_definition_modify_layout", result)
    return UnicatDefinition(unicat, result["definition"])


def modify_definition_add_childdefinition(unicat, definition, childdefinition):
    success, result = unicat.api.call(
        "/definitions/childdefinitions/add",
        {"definition": definition.gid, "childdefinition": childdefinition.gid},
    )
    if not success:
        raise UnicatError("modify_definition_add_childdefinition", result)
    return UnicatDefinition(unicat, result["definition"])


def modify_definition_remove_childdefinition(unicat, definition, childdefinition):
    success, result = unicat.api.call(
        "/definitions/childdefinitions/remove",
        {"definition": definition.gid, "childdefinition": childdefinition.gid},
    )
    if not success:
        raise UnicatError("modify_definition_remove_childdefinition", result)
    return UnicatDefinition(unicat, result["definition"])


def commit_definition(unicat, new_or_working_copy):
    success, result = unicat.api.call(
        "/definitions/commit", {"definition": new_or_working_copy.gid}
    )
    if not success:
        raise UnicatError("commit_definition", result)
    if (
        result["definition"] != new_or_working_copy.gid
        and new_or_working_copy.gid in unicat.api.data["definitions"]
    ):
        del unicat.api.data["definitions"][new_or_working_copy.gid]
    return UnicatDefinition(unicat, result["definition"])


def delete_definition(unicat, definition):
    success, result = unicat.api.call(
        "/definitions/delete", {"definition": definition.gid}
    )
    if not success:
        raise UnicatError("delete_definition", result)
    if definition.gid in unicat.api.data["definitions"]:
        del unicat.api.data["definitions"][definition.gid]
    return True
