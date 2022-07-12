import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_version, settings
from app.utilities.middlewares import RequestContextTraceMiddleware

from .routers.todos import todos
from .routers.utils import utils

description = """
This FastAPI Template shows how to build cloud-native scalable APIs
with OpenAPI documentation.
"""

app = FastAPI(
    title="FastAPI Template",
    docs_url="/",
    description=description,
    version=app_version,
    openapi_prefix=settings.root_path,
    root_path=settings.root_path,
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=[
        "http://localhost:3000",
    ],
)
app.add_middleware(RequestContextTraceMiddleware)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(
    todos.router,
    prefix="/v1/todos",
    tags=["todos"],
)
app.include_router(
    utils.router,
    prefix="/v1/utils",
    tags=["utils"],
)


if __name__ == "__main__":
    print("\nDev API Docs: http://localhost:8000\n")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
