
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi import APIRouter, Depends, HTTPException, status

config = Config('.env')  # read config from .env file, may not work, pass the client_id, client_secret directly in register
oauth = OAuth(config)
oauth.register(
    name='github',
    access_token_params=None,
    authorize_params=None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    access_token_url = 'https://github.com/login/oauth/access_token',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

router = APIRouter()

@router.route('/login')
async def login(request: Request):
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('authorize')
    return await oauth.github.authorize_redirect(request, redirect_uri)

@router.get('/authorize')
async def authorize(request: Request):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get('user', token=token)
    #user = await oauth.github.parse_id_token(request, token)
    resp.raise_for_status()
    profile = resp.json()
    request.session["user"] = profile
    # do something with the token and profile
    return {'user': request.session['user']}
