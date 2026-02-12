from fastapi import FastAPI
from models import Product
app=FastAPI()
@app.get("/")
def greet():
    return "Hello world!"

products=[
    Product(id=1,name="laptop",price=999,quantity=10),
    Product(id=2,name="phone",price=550,quantity=5)
    
]

@app.get("/Product/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    return "404 Not Found"


@app.get("/products")
def get_all_products():
    return products

@app.post("/product")
def add_product(product:Product):
    products.append(product)
    return product

@app.put("/product")
def update_product(id:int,product:Product):
    for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return "updated successfully"
    return "Not found"

@app.delete("/product")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id==id:
            del products[i]
            return "Deleted Successfully"
    return "Not found"