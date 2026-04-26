import os

from fastapi import FastAPI

from starlette.staticfiles import StaticFiles

from routers import news, users, favorites, history, ai_chat, admin
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许的源
    allow_credentials=True,     # 允许携带的cookie
    allow_methods=["*"],        # 允许的请求方法
    allow_headers=["*"],        # 允许的请求头
)

for directory in ["media/avatars"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

app.mount("/media", StaticFiles(directory="media", html=False), name="media")

@app.get('/')
async def root():
    return {'message': 'hello world'}


@app.get("/hello/{name}")
async def say_hello(name):
    return {'message': f'hello {name}'}


app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorites.router)
app.include_router(history.router)
app.include_router(ai_chat.router)
app.include_router(admin.router)
