from app.core.database import Base, engine
from app.models.db_crypto import CryptoDB

print("🛠️ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")
