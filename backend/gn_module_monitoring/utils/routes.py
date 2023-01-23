from typing import Tuple

from flask import Response
from flask.json import jsonify
from geonature.utils.env import DB
from marshmallow import Schema
from sqlalchemy import cast, func, text
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Query
from werkzeug.datastructures import MultiDict

from gn_module_monitoring.monitoring.queries import Query as MonitoringQuery
from gn_module_monitoring.monitoring.schemas import paginate_schema


def get_limit_page(params: MultiDict) -> Tuple[int]:
    return int(params.pop("limit", 50)), int(params.pop("page", 1))


def get_sort(params: MultiDict, default_sort: str, default_direction) -> Tuple[str]:
    return params.pop("sort", default_sort), params.pop("sort_dir", default_direction)


def paginate(query: Query, schema: Schema, limit: int, page: int) -> Response:
    result = query.paginate(page=page, error_out=False, per_page=limit)
    pagination_schema = paginate_schema(schema)
    data = pagination_schema().dump(
        dict(items=result.items, count=result.total, limit=limit, page=page)
    )
    return jsonify(data)


def filter_params(query: MonitoringQuery, params: MultiDict) -> MonitoringQuery:
    if len(params) != 0:
        query = query.filter_by_params(params)
    return query


def sort(query: MonitoringQuery, sort: str, sort_dir: str) -> MonitoringQuery:
    if sort_dir in ["desc", "asc"]:
        query = query.sort(label=sort, direction=sort_dir)
    return query


def geojson_query(subquery) -> bytes:
    subquery_name = "q"
    subquery = subquery.alias(subquery_name)
    query = DB.session.query(
        func.json_build_object(
            text("'type'"),
            text("'FeatureCollection'"),
            text("'features'"),
            func.json_agg(cast(func.st_asgeojson(subquery), JSON)),
        )
    )
    result = query.first()
    if len(result) > 0:
        return result[0]
    return b""
