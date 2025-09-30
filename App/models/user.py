from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(256), nullable=False) # e.g., 'student', 'staff', 'admin'

    
    def __init__(self, username, password):
        self.user_id = username
        self.set_password(password)


    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

