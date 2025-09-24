from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
import json

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Camera Management System", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Security
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-this')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Models
class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    role: str = "user"  # admin, manager, user, viewer
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Camera(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    model: str
    serial_number: str
    arrival_date: datetime
    status: str = "active"  # active, maintenance, inactive, disposed
    location: Optional[str] = None
    responsible_user: Optional[str] = None
    warranty_date: Optional[datetime] = None
    maintenance_schedule: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CameraCreate(BaseModel):
    name: str
    model: str
    serial_number: str
    arrival_date: datetime
    location: Optional[str] = None
    responsible_user: Optional[str] = None
    warranty_date: Optional[datetime] = None
    maintenance_schedule: Optional[str] = None
    notes: Optional[str] = None

class CameraUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    arrival_date: Optional[datetime] = None
    status: Optional[str] = None
    location: Optional[str] = None
    responsible_user: Optional[str] = None
    warranty_date: Optional[datetime] = None
    maintenance_schedule: Optional[str] = None
    notes: Optional[str] = None

class MaintenanceLog(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    camera_id: str
    user_id: str
    maintenance_type: str  # routine, repair, inspection
    description: str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    next_maintenance: Optional[datetime] = None
    cost: Optional[float] = None

class MaintenanceLogCreate(BaseModel):
    camera_id: str
    maintenance_type: str
    description: str
    next_maintenance: Optional[datetime] = None
    cost: Optional[float] = None

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await db.users.find_one({"id": user_id})
    if user is None:
        raise credentials_exception
    return User(**user)

def require_role(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker

def prepare_for_mongo(data):
    """Convert datetime objects to ISO strings for MongoDB storage"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
    return data

def parse_from_mongo(item):
    """Parse ISO strings back to datetime objects"""
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, str) and key.endswith(('_at', '_date')) and 'T' in value:
                try:
                    item[key] = datetime.fromisoformat(value.replace('Z', '+00:00'))
                except ValueError:
                    pass
    return item

# Authentication routes
@api_router.post("/auth/register", response_model=User)
async def register_user(user: UserCreate):
    # Check if user already exists
    existing_user = await db.users.find_one({"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Hash password and create user
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict.pop('password')
    user_obj = User(**user_dict)
    
    # Store in database with hashed password
    user_data = user_obj.dict()
    user_data['password_hash'] = hashed_password
    user_data = prepare_for_mongo(user_data)
    
    await db.users.insert_one(user_data)
    return user_obj

@api_router.post("/auth/login", response_model=Token)
async def login_user(user_data: UserLogin):
    # Find user
    user = await db.users.find_one({"username": user_data.username})
    if not user or not verify_password(user_data.password, user['password_hash']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['id']}, expires_delta=access_token_expires
    )
    
    user_obj = User(**parse_from_mongo(user))
    return {"access_token": access_token, "token_type": "bearer", "user": user_obj}

@api_router.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# Camera routes
@api_router.post("/cameras", response_model=Camera)
async def create_camera(
    camera: CameraCreate,
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    camera_dict = camera.dict()
    camera_obj = Camera(**camera_dict)
    
    # Check if serial number already exists
    existing_camera = await db.cameras.find_one({"serial_number": camera_obj.serial_number})
    if existing_camera:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Camera with this serial number already exists"
        )
    
    camera_data = prepare_for_mongo(camera_obj.dict())
    await db.cameras.insert_one(camera_data)
    return camera_obj

@api_router.get("/cameras", response_model=List[Camera])
async def get_cameras(
    status: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    filter_dict = {}
    
    if status:
        filter_dict["status"] = status
    if location:
        filter_dict["location"] = {"$regex": location, "$options": "i"}
    if search:
        filter_dict["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"model": {"$regex": search, "$options": "i"}},
            {"serial_number": {"$regex": search, "$options": "i"}}
        ]
    
    cameras = await db.cameras.find(filter_dict).to_list(1000)
    return [Camera(**parse_from_mongo(camera)) for camera in cameras]

@api_router.get("/cameras/{camera_id}", response_model=Camera)
async def get_camera(
    camera_id: str,
    current_user: User = Depends(get_current_user)
):
    camera = await db.cameras.find_one({"id": camera_id})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return Camera(**parse_from_mongo(camera))

@api_router.put("/cameras/{camera_id}", response_model=Camera)
async def update_camera(
    camera_id: str,
    camera_update: CameraUpdate,
    current_user: User = Depends(require_role(["admin", "manager"]))
):
    camera = await db.cameras.find_one({"id": camera_id})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    update_data = {k: v for k, v in camera_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    
    # Check serial number uniqueness if being updated
    if "serial_number" in update_data:
        existing_camera = await db.cameras.find_one({
            "serial_number": update_data["serial_number"],
            "id": {"$ne": camera_id}
        })
        if existing_camera:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Camera with this serial number already exists"
            )
    
    update_data = prepare_for_mongo(update_data)
    await db.cameras.update_one({"id": camera_id}, {"$set": update_data})
    
    updated_camera = await db.cameras.find_one({"id": camera_id})
    return Camera(**parse_from_mongo(updated_camera))

@api_router.delete("/cameras/{camera_id}")
async def delete_camera(
    camera_id: str,
    current_user: User = Depends(require_role(["admin"]))
):
    camera = await db.cameras.find_one({"id": camera_id})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    await db.cameras.delete_one({"id": camera_id})
    return {"message": "Camera deleted successfully"}

# Maintenance routes
@api_router.post("/maintenance", response_model=MaintenanceLog)
async def create_maintenance_log(
    maintenance: MaintenanceLogCreate,
    current_user: User = Depends(require_role(["admin", "manager", "user"]))
):
    # Check if camera exists
    camera = await db.cameras.find_one({"id": maintenance.camera_id})
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    maintenance_dict = maintenance.dict()
    maintenance_dict["user_id"] = current_user.id
    maintenance_obj = MaintenanceLog(**maintenance_dict)
    
    maintenance_data = prepare_for_mongo(maintenance_obj.dict())
    await db.maintenance_logs.insert_one(maintenance_data)
    return maintenance_obj

@api_router.get("/maintenance/{camera_id}", response_model=List[MaintenanceLog])
async def get_camera_maintenance(
    camera_id: str,
    current_user: User = Depends(get_current_user)
):
    maintenance_logs = await db.maintenance_logs.find({"camera_id": camera_id}).sort("date", -1).to_list(100)
    return [MaintenanceLog(**parse_from_mongo(log)) for log in maintenance_logs]

# Statistics routes
@api_router.get("/stats")
async def get_statistics(current_user: User = Depends(get_current_user)):
    total_cameras = await db.cameras.count_documents({})
    active_cameras = await db.cameras.count_documents({"status": "active"})
    maintenance_cameras = await db.cameras.count_documents({"status": "maintenance"})
    
    # Cameras by status
    status_pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    status_stats = await db.cameras.aggregate(status_pipeline).to_list(10)
    
    # Cameras needing maintenance (warranty expiring in 30 days)
    thirty_days_from_now = datetime.now(timezone.utc) + timedelta(days=30)
    expiring_warranty = await db.cameras.count_documents({
        "warranty_date": {"$lte": thirty_days_from_now.isoformat(), "$gte": datetime.now(timezone.utc).isoformat()}
    })
    
    return {
        "total_cameras": total_cameras,
        "active_cameras": active_cameras,
        "maintenance_cameras": maintenance_cameras,
        "status_distribution": status_stats,
        "expiring_warranty": expiring_warranty
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Create default admin user if no users exist
    user_count = await db.users.count_documents({})
    if user_count == 0:
        admin_user = {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@company.com",
            "role": "admin",
            "password_hash": get_password_hash("admin123"),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(admin_user)
        logger.info("Default admin user created: username=admin, password=admin123")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()