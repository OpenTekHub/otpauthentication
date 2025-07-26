from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    echo=True,  
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models.user import Base
    Base.metadata.create_all(bind=engine)

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f" Database test failed: {e}")
        return False

def create_user(phone_number: int, name: str, email: str):
    from app.models.user import UserORM, User
    
    db = SessionLocal()
    try:
        db_user = UserORM(
            phone_number=phone_number,
            name=name,
            email=email
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Convert to Pydantic model
        user = User(
            id=db_user.id,
            phone_number=db_user.phone_number,
            name=db_user.name,
            email=db_user.email
        )
        return user
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_user_by_phone(phone_number: int):
    from app.models.user import UserORM, User
    
    db = SessionLocal()
    try:
        stmt = select(UserORM).where(UserORM.phone_number == phone_number)
        result = db.execute(stmt)
        db_user = result.scalar_one_or_none()
        
        if db_user:
            user = User(
                id=db_user.id,
                phone_number=db_user.phone_number,
                name=db_user.name,
                email=db_user.email
            )
            return user
        return None
        
    finally:
        db.close()
