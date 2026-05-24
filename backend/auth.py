from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os

load_dotenv()

sec_key=os.getenv("SECRET_KEY")
algorithm_a=os.getenv("ALGORITHM")
access_tkn_expire=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

IST=timezone(timedelta(hours=5,minutes=30))


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(plain_password:str)->str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password:str, hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)


## JWT token creation 

def create_access_token(data:dict)->str:
    to_encode=data.copy()

    expire=datetime.now(IST)+timedelta(minutes=access_tkn_expire)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,sec_key,algorithm=algorithm_a)
    return token

def verify_token(token:str)->str:
    try:
        payload=jwt.decode(token,sec_key,algorithms=[algorithm_a])
        email:str=payload.get("sub")

        if email is None:
            return None
        return email
            
    except JWTError:
        return None
