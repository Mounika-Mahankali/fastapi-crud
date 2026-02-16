from fastapi import Depends,FastAPI
from models import Product
from database import session,engine
import database_models
from fastapi import HTTPException


app=FastAPI()

database_models.Base.metadata.create_all(bind=engine)

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