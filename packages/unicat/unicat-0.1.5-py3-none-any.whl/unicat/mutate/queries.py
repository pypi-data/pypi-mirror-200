from ..query import UnicatQuery
from ..error import UnicatError


def create_query(unicat, properties):
    success, result = unicat.api.call("/queries/create", properties)
    if not success:
        raise UnicatError("create_query", result)
    return UnicatQuery(unicat, result["query"])


def update_query(unicat, query, properties):
    success, result = unicat.api.call(
        "/queries/update",
        {**properties, "query": query.gid},
    )
    if not success:
        raise UnicatError("update_query", result)
    return UnicatQuery(unicat, result["query"])


def delete_query(unicat, query):
    success, result = unicat.api.call("/queries/delete", {"query": query.gid})
    if not success:
        raise UnicatError("delete_query", result)
    if query.gid in unicat.api.data["queries"]:
        del unicat.api.data["queries"][query.gid]
    return True
