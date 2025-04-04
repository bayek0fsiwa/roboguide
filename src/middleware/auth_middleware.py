import boto3
from fastapi import HTTPException, Request, status

cognito_client = boto3.client("cognito-idp", region_name="ap-south-1")


def _get_user_detail_from_cognito(access_token: str):
    try:
        user_response = cognito_client.get_user(AccessToken=access_token)
        return {
            attrs["Name"]: attrs["Value"]
            for attrs in user_response.get("UserAttributes", [])
        }
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{e}")


def get_current_user(req: Request):
    all_cookies = req.cookies
    access_token_cookie = all_cookies.get("loki-access")
    if not access_token_cookie:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Not authorized!")
    return _get_user_detail_from_cognito(access_token_cookie)
