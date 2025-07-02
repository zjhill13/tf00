from src.models.user import db
from datetime import datetime

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    delivery_time = db.Column(db.String(50), nullable=False)  # e.g., "3 days", "1 week"
    image_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    orders_count = db.Column(db.Integer, default=0)
    
    # Service packages (JSON string)
    packages = db.Column(db.Text, nullable=True)  # JSON string of service packages
    
    def __repr__(self):
        return f'<Service {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'starting_price': self.starting_price,
            'creator_id': self.creator_id,
            'creator': self.creator.to_public_dict() if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'delivery_time': self.delivery_time,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'orders_count': self.orders_count,
            'packages': self.packages
        }

    def to_summary_dict(self):
        """Simplified version for listings"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'starting_price': self.starting_price,
            'creator': self.creator.to_public_dict() if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'delivery_time': self.delivery_time,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'orders_count': self.orders_count
        }

