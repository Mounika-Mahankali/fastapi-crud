from pydantic import BaseModel,Field,EmailStr

class Product(BaseModel):
    id:int
    name:str=Field(...,min_length=1)
    price:float=Field(...,gt=0)
    quantity:int=Field(...,ge=0)

class user_reg(BaseModel):
    username:str
    email:EmailStr
    pw: str=Field(...,min_length=6,max_length=72)
    role: str

class user_login(BaseModel):
    email: EmailStr
    pw: str=Field(...,min_length=6,max_length=72)
    
    class Config:
        from_attributes=True


# there is no need to use  constructor,Due to usage of BaseModel
    