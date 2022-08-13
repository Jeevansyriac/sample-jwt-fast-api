import uvicorn

import db
import model
import schema
from fastapi import FastAPI,Body,Depends

from auth_handler import signJWT
from jwt_bearer import JWTBearer

from db import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)
db = SessionLocal()

app = FastAPI(title="user registration")


# users = []

app = FastAPI()


# (tags is used for grouping)

# Get all Posts
@app.get("/posts", tags=["books"])
def get_posts():
    get_post = db.query(model.book).all()
    return get_post


# get a post by id..
@app.get("/posts/{id}",dependencies=[Depends(JWTBearer())], tags=["books"])
def  get_user(id:str):
    receive_book = db.query(model.book).filter(model.book.id==id).first()
    return receive_book



@app.post("/posts",dependencies=[Depends(JWTBearer())], tags=["books"])
def add_post(data:schema.Base):
    try:
        add_posts= model.book(**data.dict())
        db.add( add_posts)
        db.commit()
        
         
        
    except:
         return{'db error'}
    return data,add_posts

@app.get("/user", tags=["user"])
def get_user():
    gert_users = db.query(model.User).all()
    return gert_users
    
# # for user signup

@app.post("/user/signup", tags=["user"])
# def user_signup(user: schema.user = Body(default=None)):
#     users.append(user) 
#     return signJWT(user.email)

# def check_user(data: schema.user):
#     # for user in User:
#     #     if user.email == data.email and user.password == data.password:
#     #         return True
#         return False

def add_user(user:schema.user):
    # try:
        add_users= model.User(**user.dict())
        db.add( add_users)
        db.commit()
         
    # except:
    #      return{'db error'}
        # return data1
        return signJWT(user.email)


def check_user(data: schema.user):
    v1=db.query(model.User).all()
    for user in v1:

        if user.email == data.email and user.password == data.password:
            return True
        return False




@app.post("/user/login", tags=["user"])
def user_login(user: schema.userlogin = Body(default=None)):
    v2=db.query(model.User).all()
    for user in v2:
        
        if check_user(user):
            return signJWT(user.email)
        return {
            "error": "Wrong login details!"
        }


@app.get('/car',tags=["car"])
def get_car(id:str):
    var1 = db.query(model.car).filter(model.car.id == id).first()
    return var1

@app.post('/car/car_details', tags=["car"])
def post_car(data2:schema.car):
    car_details = model.car(**data2.dict())
    db.add(car_details)
    db.commit()
    return data2

@app.delete('/car/delete_car_details', tags=["car"])
def delete(id:str):
    delete_details=db.query(model.car).filter(model.car.id==id).first()
    db.delete(delete_details)
    db.commit()
    return delete_details

@app.put('/car/update car_details',tags=["car"])
def update(id:str,name:str,company_name:str,price:str):
    update_data = db.query(model.car).filter(model.car.id==id).first()
    if not update_data:
        return 404
        
    update_data.name = name
    update_data.company_name = name
    update_data.price = price

    db.add(update_data)
    db.commit()
    return update_data
    