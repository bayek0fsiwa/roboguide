import os
import boto3
from fastapi import APIRouter, Request, HTTPException, Response, status, Depends
from sqlmodel import Session
from decouple import config as decouple_config
from dotenv import load_dotenv
from auth.service import save_to_db
from helper.auth_helper import get_secret_hash
from config.db import get_session
from middleware.auth_middleware import get_current_user


load_dotenv()
router = APIRouter()


cognito_client = boto3.client("cognito-idp", region_name="ap-south-1")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
COGNITO_CLIENT_NAME = os.getenv("COGNITO_CLIENT_NAME")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(req: Request, session: Session = Depends(get_session)) -> dict:
    try:
        user_details = await req.json()
        name = user_details["name"]
        email = user_details["email"]
        password = user_details["password"]
        secret_hash = get_secret_hash(email, "5mnvjmhm7lepe86ja9g3p9tp0m", "flh6afenu2ogbn4uk8bc86u82css7s0hcvtbru29ksre3etrlmd")
        cognito_response = cognito_client.sign_up(
            ClientId = "5mnvjmhm7lepe86ja9g3p9tp0m",
            SecretHash = secret_hash,
            Username = email,
            Password = password,
            UserAttributes=[
            {'Name': 'email', 'Value': email},
            {'Name': 'name', 'Value': name},
        ],
        )
        cognito_id = cognito_response.get("UserSub")
        data_to_save = {"cognito_id": cognito_id, "name": name, "email": email, "password": password}
        if cognito_response.get("UserSub"):
            await save_to_db(data_to_save, session)
        return {"message": "Success. Now please verify your mail. Link has been sent to your mail address."}
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(req: Request, res: Response):
    try:
        user_details = await req.json()
        email = user_details["email"]
        password = user_details["password"]
        secret_hash = get_secret_hash(email, "5mnvjmhm7lepe86ja9g3p9tp0m", "flh6afenu2ogbn4uk8bc86u82css7s0hcvtbru29ksre3etrlmd")
        cognito_response = cognito_client.initiate_auth(
            ClientId = "5mnvjmhm7lepe86ja9g3p9tp0m",
            AuthFlow = "USER_PASSWORD_AUTH",
            AuthParameters = {'USERNAME': email, 'PASSWORD': password, "SECRET_HASH": secret_hash,},
        )
        auth_result = cognito_response.get("AuthenticationResult")
        if not auth_result:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"{e}")
        access_token = auth_result["AccessToken"]
        refresh_token = auth_result["RefreshToken"]
        res.set_cookie("loki-access", access_token, httponly=True, secure=True)
        res.set_cookie("loki-refresh", refresh_token, httponly=True, secure=True)
        return cognito_response
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")


@router.post("/verify-account", status_code=status.HTTP_200_OK)
async def login_user(req: Request):
    try:
        user_details = await req.json()
        email = user_details["email"]
        otp = user_details["otp"]
        secret_hash = get_secret_hash(email, "5mnvjmhm7lepe86ja9g3p9tp0m", "flh6afenu2ogbn4uk8bc86u82css7s0hcvtbru29ksre3etrlmd")
        cognito_response = cognito_client.confirm_sign_up(
            ClientId = "5mnvjmhm7lepe86ja9g3p9tp0m",
            Username = email,
            ConfirmationCode = otp,
            SecretHash = secret_hash,
        )
        return {"message": "User confirmed."}
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_tokens(req: Request, res: Response):
    try:
        all_cookies = req.cookies
        refresh_token_cookie: str = all_cookies.get("loki-refresh")
        user_cognito_id: str  = all_cookies.get("cognito_id")
        secret_hash = get_secret_hash(user_cognito_id, "5mnvjmhm7lepe86ja9g3p9tp0m", "flh6afenu2ogbn4uk8bc86u82css7s0hcvtbru29ksre3etrlmd")
        cognito_response = cognito_client.initiate_auth(
            ClientId = "5mnvjmhm7lepe86ja9g3p9tp0m",
            AuthFlow = "REFRESH_TOKEN_AUTH",
            AuthParameters = {'REFRESH_TOKEN': refresh_token_cookie, "SECRET_HASH": secret_hash,},
        )
        auth_result = cognito_response.get("AuthenticationResult")
        if not auth_result:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"{e}")
        access_token = auth_result["AccessToken"]
        res.set_cookie("loki-access", access_token, httponly=True, secure=True)
        return {"message": "Token refreshed."}
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")


@router.get("/me", status_code=status.HTTP_200_OK)
async def protected_route(user = Depends(get_current_user)):
    try:
        return {"message": "Authenticated!", "user": user}
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")
