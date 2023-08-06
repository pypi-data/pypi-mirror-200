from fastapi import Security, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKey, APIKeyHeader

temp_api_keys = [
    "69"
]

api_key_header = APIKeyHeader(name="authorization", auto_error=False)

async def get_api_key(api_key_raw: str = Security(api_key_header)):
    try:
        (key_type, api_key) = api_key_raw.split()
        assert(key_type.lower() == 'bearer')
        assert(api_key)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Malformed API KEY. Expecting: Authorization: Bearer {token})"
        )

    if api_key in temp_api_keys:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY."
        )


async def get_user_id(api_key: APIKey=Depends(get_api_key)) -> int:
    return 11


#def get_user(api_key: str = Depends(oauth2_scheme)):
#    pass


# from .jwt import decodeJWT


# class ApiTokenBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super(ApiTokenBearer, self).__init__(auto_error=auto_error)

#     async def __call__(self, request: Request):
#         credentials: HTTPAuthorizationCredentials = await super(ApiTokenBearer, self).__call__(request)
#         print('CREDS 4', credentials)
#         if credentials:
#             if not credentials.scheme == "Bearer":
#                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
#         return credentials.credentials

# #     async def __call__(self, request: Request):
# #         credentials: HTTPAuthorizationCredentials = await super(ApiTokenBearer, self).__call__(request)
# #         if credentials:
# #             if not credentials.scheme == "Bearer":
# #                 raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
# #             if not self.verify_jwt(credentials.credentials):
# #                 raise HTTPException(status_code=403, detail="Invalid token or expired token.")
# #             return credentials.credentials
# #         else:
# #             raise HTTPException(status_code=403, detail="Invalid authorization code.")

# #     def verify_jwt(self, jwtoken: str) -> bool:
# #         isTokenValid: bool = False

# #         try:
# #             payload = decodeJWT(jwtoken)
# #         except:
# #             payload = None
# #         if payload:
# #             isTokenValid = True
# #         return isTokenValid