from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from passlib.hash import bcrypt
from config import get_config
import logging

logger = logging.getLogger(__name__)
config = get_config()

try:
    client = MongoClient(
        config.MONGODB_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000
    )
    # Verify connection
    client.admin.command('ping')
    db = client[config.MONGODB_DB_NAME]
    logger.info(f"Successfully connected to MongoDB database: {config.MONGODB_DB_NAME}")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

class User:
    def __init__(self, email, password_hash=None):
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        if not password:
            raise ValueError("Password cannot be empty")
        return bcrypt.hash(password)

    def verify_password(self, password):
        """Verify a password against the stored hash"""
        if not self.password_hash:
            return False
        try:
            return bcrypt.verify(password, self.password_hash)
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False

    @classmethod
    def find_by_email(cls, email):
        """Find a user by email address"""
        if not email:
            return None

        try:
            user_doc = db.users.find_one({'email': email.lower()})
            if user_doc:
                user = cls(user_doc['email'], user_doc.get('password_hash'))
                # Handle legacy plain text passwords by migrating them
                if 'password' in user_doc and not user_doc.get('password_hash'):
                    logger.warning(f"Migrating legacy password for user: {email}")
                    user.password_hash = cls.hash_password(user_doc['password'])
                    db.users.update_one(
                        {'email': email.lower()},
                        {'$set': {'password_hash': user.password_hash}, '$unset': {'password': ''}}
                    )
                return user
        except Exception as e:
            logger.error(f"Error finding user by email: {e}")
        return None

    def save(self):
        """Save user to database"""
        if not self.email or not self.password_hash:
            raise ValueError("Email and password hash are required")

        try:
            result = db.users.insert_one({
                'email': self.email.lower(),
                'password_hash': self.password_hash
            })
            logger.info(f"User created successfully: {self.email}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error saving user: {e}")
            raise

    @classmethod
    def create_indexes(cls):
        """Create database indexes for better performance"""
        try:
            db.users.create_index('email', unique=True)
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")