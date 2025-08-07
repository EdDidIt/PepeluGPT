from flask import Flask, jsonify, request
from typing import Any, Dict, Tuple
from flask.wrappers import Response

from core.utils import get_logger

LOG = get_logger(__name__)
app = Flask(__name__)


@app.route("/query", methods=["POST"])
def query() -> Tuple[Response, int]:
    data: Dict[str, Any] = request.json or {}
    q: str = data.get("query", "")
    if not q:
        LOG.warning("🟡 Empty query received.")
        return jsonify({"error": "Missing 'query' parameter"}), 400
    # TODO: integrate with orchestrator or engine
    LOG.info("🔵 Processing API query...")
    response: Dict[str, str] = {"answer": "stub"}
    return jsonify(response), 200


def create_app():
    return app
