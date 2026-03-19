import json
from bson import ObjectId
from mcp_server.registry import tool
from mcp_server.tools.mongodb.client import get_db


def _clean(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict."""
    if isinstance(doc, list):
        return [_clean(d) for d in doc]
    if isinstance(doc, dict):
        return {k: _clean(v) for k, v in doc.items()}
    if isinstance(doc, ObjectId):
        return str(doc)
    return doc


@tool("MongoDB")
def mongo_list_collections() -> str:
    """List all collections in the MongoDB database."""
    db = get_db()
    return json.dumps(db.list_collection_names(), indent=2)


@tool("MongoDB")
def mongo_find(collection: str, filter: str = "{}", limit: int = 20, skip: int = 0) -> str:
    """Find documents in a MongoDB collection. filter as JSON string."""
    db = get_db()
    flt = json.loads(filter) if filter.strip() else {}
    docs = list(db[collection].find(flt, limit=limit, skip=skip))
    return json.dumps(_clean(docs), indent=2)


@tool("MongoDB")
def mongo_find_one(collection: str, filter: str = "{}") -> str:
    """Find a single document in a MongoDB collection. filter as JSON string."""
    db = get_db()
    flt = json.loads(filter) if filter.strip() else {}
    doc = db[collection].find_one(flt)
    return json.dumps(_clean(doc) if doc else None, indent=2)


@tool("MongoDB")
def mongo_insert_document(collection: str, data: str) -> str:
    """Insert a document into a MongoDB collection. data as JSON string."""
    db = get_db()
    doc = json.loads(data)
    result = db[collection].insert_one(doc)
    return json.dumps({"inserted_id": str(result.inserted_id)}, indent=2)


@tool("MongoDB")
def mongo_insert_many(collection: str, data: str) -> str:
    """Insert multiple documents. data as JSON array string."""
    db = get_db()
    docs = json.loads(data)
    result = db[collection].insert_many(docs)
    return json.dumps({"inserted_ids": [str(i) for i in result.inserted_ids], "count": len(result.inserted_ids)}, indent=2)


@tool("MongoDB")
def mongo_update_document(collection: str, filter: str, update: str, upsert: bool = False) -> str:
    """Update a document in a MongoDB collection. filter and update as JSON strings."""
    db = get_db()
    flt = json.loads(filter)
    upd = json.loads(update)
    result = db[collection].update_one(flt, upd, upsert=upsert)
    return json.dumps({
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id else None,
    }, indent=2)


@tool("MongoDB")
def mongo_delete_document(collection: str, filter: str) -> str:
    """Delete a single document from a MongoDB collection. filter as JSON string."""
    db = get_db()
    flt = json.loads(filter)
    result = db[collection].delete_one(flt)
    return json.dumps({"deleted_count": result.deleted_count}, indent=2)


@tool("MongoDB")
def mongo_count(collection: str, filter: str = "{}") -> str:
    """Count documents in a MongoDB collection. filter as JSON string."""
    db = get_db()
    flt = json.loads(filter) if filter.strip() else {}
    count = db[collection].count_documents(flt)
    return json.dumps({"count": count}, indent=2)


@tool("MongoDB")
def mongo_aggregate(collection: str, pipeline: str) -> str:
    """Run an aggregation pipeline on a MongoDB collection. pipeline as JSON array."""
    db = get_db()
    pipe = json.loads(pipeline)
    results = list(db[collection].aggregate(pipe))
    return json.dumps(_clean(results), indent=2)
