from pydantic import BaseModel
class Product(BaseModel):
    id:int
    name:str
    price:float
    quantity:int
# there is no need to use  constructor,Due to usage of BaseModel
    