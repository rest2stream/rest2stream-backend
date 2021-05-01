from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from routers import myapi, stream, accounts

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://192.168.1.88:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    myapi.router,
    prefix="/myapi"
)
app.include_router(
    stream.router,
    prefix="/stream"
)
app.include_router(
    accounts.router,
    prefix="/accounts"
)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

