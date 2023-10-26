from fastapi import FastAPI, HTTPException, Query, Depends, HTMLResponse
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from contrib.clients.python.service import SSOAgent

app = FastAPI()
SSO_API_KEY = None
SSO_API_SECRET = None


@app.get("/login", response_class=HTMLResponse)
def login_page():
    sso_authentication_route = SSOAgent(SSO_API_KEY).authentication_route
    return f"""
        <html>
        <head>
            <title>Login</title>
        </head>
        <body>
            <h1>Login Page</h1>
            <p>Click <a href="{sso_authentication_route}">here</a> to initiate SSO authentication.</p>
        </body>
        </html>
    """


class AuthTokenQueryParams(BaseModel):
    state: str
    auth_token: str


@app.get("/sso/callback/")
async def sso_callback(params: AuthTokenQueryParams):
    if params.state != 'SUCCESS':
        return JSONResponse(content={'state': 'UNVERIFIED'}, status_code=400)

    # Replace this with your actual SSO logic, for example using an SSO library
    sso = SSOAgent(SSO_API_KEY, SSO_API_SECRET, token=params.auth_token)
    auth = sso.get_user_details()

    if auth is None:
        return JSONResponse(content={'state': 'UNVERIFIED'}, status_code=400)

    # Handle whatever you want here
    return JSONResponse(content={'state': 'VERIFIED'})
