from typing import Tuple

from flask import Response
from flask.json import jsonify
from sqlalchemy.orm import Query
from werkzeug.datastructures import MultiDict


def get_limit_offset(params: MultiDict) -> Tuple[int]:
    return int(params.pop("limit", 50)), int(params.pop("offset", 1))


def paginate(query: Query, object_name: str, limit: int, page: int, depth: int = 0) -> Response:
    result = query.paginate(page=page, error_out=False, per_page=limit)
    data = {
        object_name: [res.as_dict(depth=depth) for res in result.items],
        "count": result.total,
        "limit": limit,
        "offset": page - 1,
    }
    return jsonify(data)


def filter_params(query: Query, params: MultiDict) -> Query:
    if len(params) != 0:
        query = query.filter_by(**params)
    return query
