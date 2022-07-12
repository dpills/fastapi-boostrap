from datetime import datetime

from bson.objectid import ObjectId
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.routers.auth.auth import validate_access_token
from app.static_values import mongo_id_regex
from app.utilities.db import db
from app.utilities.logger import logger

from .enums import Status
from .models import ResponseStatus, Todo, TodoRecord, TodoUpdate

router = APIRouter()
security = HTTPBearer()


@router.get("", response_model=list[TodoRecord])
async def get_todos(
    response: Response,
    limit: int = Query(
        500, le=2000, description="Maximum number of todos to return"
    ),
    skip: int = Query(0, description="Number of todos to skip"),
    access_token: HTTPAuthorizationCredentials = Security(security),
    access_token_details: dict = Depends(validate_access_token),
):
    """
    Get todos
    """
    username = access_token_details.get("username")
    response.headers["X-User"] = username

    user_todos = []
    for item in db.todos.find({"owner": username}, limit=limit, skip=skip):
        item["id"] = str(item["_id"])
        del item["_id"]
        user_todos.append(item)

    return user_todos


@router.post("", response_model=ResponseStatus)
async def create_todo(
    payload: Todo,
    response: Response,
    access_token: HTTPAuthorizationCredentials = Security(security),
    access_token_details: dict = Depends(validate_access_token),
):
    """
    Create a new todo
    """
    username = access_token_details.get("username")
    response.headers["X-User"] = username
    data = payload.dict()

    now = datetime.utcnow()
    record = {
        "owner": username,
        "created_date": now,
        "updated_date": now,
        "created_by": username,
        **data,
    }

    r = db.todos.insert_one(record)
    logger.info(f"Created New Todo: {r.inserted_id}")

    return {"status": Status.created}


@router.put("/{id}", response_model=ResponseStatus)
async def update_todo(
    payload: TodoUpdate,
    response: Response,
    id: str = Path(None, description="Todo ID", regex=mongo_id_regex),
    access_token: HTTPAuthorizationCredentials = Security(security),
    access_token_details: dict = Depends(validate_access_token),
):
    """
    Update a todo
    """
    username = access_token_details.get("username")
    response.headers["X-User"] = username
    event_id = ObjectId(id)
    data = payload.dict(exclude_unset=True)

    update_data = {
        **data,
        "updated_date": datetime.utcnow(),
    }

    r = db.todos.update_one(
        {"_id": event_id},
        {"$set": update_data},
    )
    logger.info(f"Updated Event: {r.matched_count}/{r.modified_count}")

    if r.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
            headers={"X-User": username},
        )

    return {"status": Status.edited}


@router.delete("/{id}", response_model=ResponseStatus)
async def delete_todo(
    response: Response,
    id: str = Path(None, description="Todo ID", regex=mongo_id_regex),
    access_token: HTTPAuthorizationCredentials = Security(security),
    access_token_details: dict = Depends(validate_access_token),
):
    """
    Delete a todo
    """
    username = access_token_details.get("username")
    response.headers["X-User"] = username
    event_id = ObjectId(id)

    r = db.events.delete_one({"_id": event_id, "owner": username})
    if r.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
            headers={"X-User": username},
        )
    logger.info(f"Deleting Event {id}: {r}")

    return {"status": Status.deleted}
