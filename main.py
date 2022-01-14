from uuid import UUID
from fastapi import FastAPI,HTTPException
from typing import List
from models import User,Gender,Role, UserUpdateRequest

#python -m uvicorn main:app --reload

app = FastAPI()

db: List[User] = [
    User(id="c798e9f3-3b42-4264-92b8-c777d27a7835",
         first_name="João",
         last_name="Guelfi",
         gender = Gender.male,
         roles=[Role.student]),
    User(id="2750766a-c138-442d-8455-cf01021ca6fc",
         first_name="Antonio",
         last_name="Tafarelo",
         gender = Gender.male,
         roles=[Role.admin,Role.user]),
]

@app.get("/")
def root():
    
    return {"Hello" : "Mundo "}

@app.get("/api/v1/users")
async def fetch_user():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id:UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

@app.put("/api/v1/user/{user_id}")
async def update_user(user_update : UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user_update.first_name = user_update.first_name
            if user_update.last_name is not None:
                user_update.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user_update.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user_update.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )
