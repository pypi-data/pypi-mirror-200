#import os
#import binascii

# import jwt
# >>> encoded = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
# >>> print(encoded)
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg
# >>> jwt.decode(encoded, "secret", algorithms=["HS256"])
# {'some': 'payload'}

# JWT_ALGORITHM=
# JWT_SECRET=binascii.hexlify(os.urandom(24))

# def token_response(token: str):
#     return {
#         "access_token": token
#     }

# def signJWT(user_id: str) -> Dict[str, str]:
#     payload = {
#         "user_id": user_id,
#         "expires": time.time() + 600
#     }
#     token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

#     return token_response(token)


# def decodeJWT(token: str) -> dict:
#     try:
#         decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         return decoded_token if decoded_token["expires"] >= time.time() else None
#     except:
#         return {}