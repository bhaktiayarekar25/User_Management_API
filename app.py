from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Query,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, asc, desc, insert, update, delete
from database import database, engine, Base
from models import User
from schemas import UserCreate, Token, UserPublic, UserUpdate
from auth import verify_password, get_password_hash, create_access_token, decode_access_token
from datetime import timedelta
from typing import List, Optional
import shutil
import os
from contextlib import asynccontextmanager  # ✅ new
# ------------------- APP SETUP -------------------

@asynccontextmanager
async def lifespan(app: FastAPI):  # ✅ replaces @app.on_event
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(title="User Management API", lifespan=lifespan)

Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ------------------- AUTH HELPERS -------------------

async def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = decode_access_token(token)
    username = token_data["username"]

    query = select(User).where(User.username == username)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user = dict(user)
    user["role"] = token_data["role"]
    return user


def require_roles(*allowed_roles):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: requires one of {allowed_roles}",
            )
        return current_user
    return role_checker


# ------------------- ROOT -------------------

@app.get("/")
def root_user():
    return {"message": "API is working, I'm hayat"}


# ------------------- 1️⃣ SIGNUP (Admin only) -------------------

@app.post("/signup")
async def signup(user: UserCreate, current_user=Depends(require_roles("admin"))):
    query = select(User).where(User.username == user.username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(user.password[:72])

    query = insert(User).values(
        username=user.username,
        email=user.email,
        role=user.role,
        password=hashed_password,
        profile_picture=user.profile_picture,
    )
    await database.execute(query)
    return {"message": "User created successfully"}


# ------------------- 2️⃣ LOGIN (JWT TOKEN) -------------------

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    query = select(User).where(User.username == form_data.username)
    user = await database.fetch_one(query)

    print("DEBUG: username entered =", form_data.username)
    print("DEBUG: password entered =", form_data.password)
    if user:
        print("DEBUG: stored hash =", user["password"])
        print("DEBUG: verify_password =", verify_password(form_data.password, user["password"]))
    else:
        print("DEBUG: user not found")

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


# ------------------- 3️⃣ GET OWN PROFILE -------------------

@app.get("/users/me", response_model=UserPublic)
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user


# ------------------- 4️⃣ UPDATE OWN PROFILE -------------------

@app.put("/users/me")
async def update_my_profile(
    user_data: UserUpdate,
    current_user=Depends(get_current_user),
):
    updates = {}
    if user_data.email:
        updates["email"] = user_data.email
    if user_data.password:
        updates["password"] = get_password_hash(user_data.password)

    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    update_query = (
        update(User)
        .where(User.id == current_user["id"])
        .values(**updates)
    )
    await database.execute(update_query)
    return {"message": "Profile updated successfully"}


# ------------------- 5️⃣ GET ALL USERS (Admin only) -------------------

@app.get("/users", response_model=List[UserPublic])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("asc"),
    current_user=Depends(require_roles("admin")),
):
    query = select(
        User.id,
        User.username,
        User.email,
        User.role,
        User.profile_picture,
        User.created_at,
        User.updated_at,
    )

    if search:
        query = query.where(User.username.ilike(f"%{search}%"))

    sort_column = getattr(User, sort_by, User.created_at)
    query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))
    query = query.offset(skip).limit(limit)

    return await database.fetch_all(query)


# ------------------- 6️⃣ CHANGE USER ROLE (Admin only) -------------------

@app.put("/users/{user_id}/role")
async def update_user_role(
    user_id: int,
    role_data: UserUpdate,
    current_user=Depends(require_roles("admin")),
):
    if not role_data.role:
        raise HTTPException(status_code=400, detail="Role is required")

    query = select(User).where(User.id == user_id)
    target_user = await database.fetch_one(query)
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_query = update(User).where(User.id == user_id).values(role=role_data.role)
    await database.execute(update_query)
    return {"message": f"User role updated to '{role_data.role}' successfully"}


# ------------------- 7️⃣ DELETE USER (Admin only) -------------------

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, current_user=Depends(require_roles("admin"))):
    if current_user["id"] == user_id:
        raise HTTPException(status_code=400, detail="Admins cannot delete themselves")

    query = select(User).where(User.id == user_id)
    existing_user = await database.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    delete_query = delete(User).where(User.id == user_id)
    await database.execute(delete_query)
    return {"message": f"User {existing_user['username']} deleted successfully"}


# ------------------- 8️⃣ UPLOAD PROFILE PICTURE -------------------

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


@app.post("/users/me/upload")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max size 2MB")

    filename = f"user_{current_user['id']}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    update_query = (
        update(User)
        .where(User.id == current_user["id"])
        .values(profile_picture=file_path)
    )
    await database.execute(update_query)

    return {
        "message": "Profile picture uploaded successfully",
        "file_path": file_path,
        "size_kb": round(file_size / 1024, 2),
    }
