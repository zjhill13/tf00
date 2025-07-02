from src.models.user import db
from datetime import datetime

class BusinessIdea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    tags = db.Column(db.Text, nullable=True)  # JSON string of tags
    image_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    sales_count = db.Column(db.Integer, default=0)
    
    # Business plan content
    executive_summary = db.Column(db.Text, nullable=True)
    market_analysis = db.Column(db.Text, nullable=True)
    business_model = db.Column(db.Text, nullable=True)
    financial_projections = db.Column(db.Text, nullable=True)
    marketing_strategy = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<BusinessIdea {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'creator_id': self.creator_id,
            'creator': self.creator.to_public_dict() if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_published': self.is_published,
            'is_featured': self.is_featured,
            'tags': self.tags,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'sales_count': self.sales_count,
            'executive_summary': self.executive_summary,
            'market_analysis': self.market_analysis,
            'business_model': self.business_model,
            'financial_projections': self.financial_projections,
            'marketing_strategy': self.marketing_strategy
        }

    def to_summary_dict(self):
        """Simplified version for listings"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'creator': self.creator.to_public_dict() if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'tags': self.tags,
            'image_url': self.image_url,
            'rating': self.rating,
            'review_count': self.review_count,
            'sales_count': self.sales_count
        }

