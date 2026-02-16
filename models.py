from pydantic import BaseModel,Field

class Product(BaseModel):
    id:int
    name:str=Field(...,min_length=1)
    price:float=Field(...,gt=0)
    quantity:int=Field(...,ge=0)

    class config:
        from_attributes=True
# there is no need to use  constructor,Due to usage of BaseModel
    