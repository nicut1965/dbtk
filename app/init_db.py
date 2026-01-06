from app.database import engine, SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

ADMIN_EMAIL = "admin@local"
ADMIN_PASSWORD = "admin123"
ADMIN_ROLE = "admin"

def init():
    from app.database import Base
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    admin = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if not admin:
        admin = User(
            email=ADMIN_EMAIL,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            role=ADMIN_ROLE
        )
        db.add(admin)
        db.commit()
        print("Admin inițial creat")

    db.close()

if __name__ == "__main__":
    init()
