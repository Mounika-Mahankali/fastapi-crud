from fastapi import Depends,FastAPI
from models import Product
from database import session,engine,Base
import database_models
from fastapi import HTTPException
from utils import hash_pwd,verify_pwd
import models
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer


app=FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Hello"

products=[
    Product(id=1,name="laptop",price=999,quantity=10),
    Product(id=2,name="phone",price=550,quantity=5)
    
]

def get_db():    #injecting db into method
    db=session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    count=db.query(database_models.Product).count()
    if count==0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/Product/{id}")
def get_product_by_id(id:int,db:session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if not db_product:
        raise HTTPException(status_code=404,detail="Product not found")
    return db_product



@app.get("/products")
def get_all_products(db:session=Depends(get_db)):
    # db=session()
    # db.query()
    db_products=db.query(database_models.Product).all()
    return db_products

@app.post("/product")

def add_product(product: Product, db=Depends(get_db)):
    db_product = database_models.Product(**product.model_dump())
    if db_product:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return "product added successfully"
    else:
        raise HTTPException(status_code=404,detail="Product not added")


@app.put("/product/{id}")
def update_product(id:int,product:Product,db:session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "product updated"
    else:
        raise HTTPException(status_code=404,detail="Product not found")

@app.delete("/product/{id}")
def delete_product(id:int,db:session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    else:
        raise HTTPException(status_code=404,detail="Product not found")
    



# AUTHENTICATION & AUTHORIZATION
SECRET_KEY="fOs9sbAvPZ76k1RERrPIk32t4Y28wkxZHkPGOSpQF5c"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINS=30

# HASHING
@app.post("/register")
def register(user:models.user_reg,db:session=Depends(get_db)):
    existing_user=db.query(database_models.User).filter(database_models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="email already registered")
    new_hashed_pwd=hash_pwd(user.pw)
    new_user=database_models.User(
        username=user.username,
        email=user.email,
        hashed_pw=new_hashed_pwd,
        role=user.role

    )
    db.add(new_user)
    db.commit()
    return "user registered successfully"

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm=Depends(),db:session=Depends(get_db)):
    db_user=db.query(database_models.User).filter(database_models.User.username==form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=401,detail="user not found")
    if not db_user.is_active:
        raise HTTPException(status_code=400,detail="user account is inactive")
    if not verify_pwd(form_data.password,db_user.hashed_pw):
        raise HTTPException(status_code=401,detail="Invalid credentials")
    access_token=create_token({'sub':db_user.email})
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }

#JWT TOKEN
def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    to_encode.update({'exp':expire})
    jwt_token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token:str=Depends(oauth2_scheme),db: session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str=payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,detail="Invalid token")
    
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    user=db.query(database_models.User).filter(database_models.User.email==email).first()
    if user is None:
        raise HTTPException(status_code=401,detail="user not found")
    return user

@app.get("/profile")
def get_user(curr_user: database_models.User=Depends(get_current_user)):
    return{
        "username":curr_user.username,
        "email":curr_user.email,
        "role":curr_user.role
    }
    

        