from jose import JWTError, jwt
from datetime import datetime, timedelta

#SECRET_KEY FOR THE PASSWORD 
#ALGORITHM TO USE
#EXPIREATION OF USER HOW LONG WILL THE USER LOGGED IN

SECRET_KEY="tErh_bSfNj6wwUPc-81S71ruf8O0Fjdfa0-pN-9mfQY"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data :dict):
    to_encode=data.copy()
    expire=datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt