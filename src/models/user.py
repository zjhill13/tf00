from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='client')  # client, creator
    subscription_tier = db.Column(db.String(20), nullable=False, default='basic')  # basic, inventor, guru
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Relationships
    business_ideas = db.relationship('BusinessIdea', backref='creator', lazy=True)
    services = db.relationship('Service', backref='creator', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type,
            'subscription_tier': self.subscription_tier,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'profile_image': self.profile_image,
            'bio': self.bio
        }

    def to_public_dict(self):
        """Public profile information (without sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'user_type': self.user_type,
            'subscription_tier': self.subscription_tier,
            'profile_image': self.profile_image,
            'bio': self.bio
        }

