from src.models.user import db
from datetime import datetime

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # purchase, sale, subscription
    item_type = db.Column(db.String(20), nullable=False)  # business_idea, service, subscription
    item_id = db.Column(db.Integer, nullable=True)  # ID of the purchased item
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, completed, failed, refunded
    payment_method = db.Column(db.String(50), nullable=True)
    stripe_payment_intent_id = db.Column(db.String(100), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # For marketplace transactions
    commission_rate = db.Column(db.Float, default=0.1)  # Platform commission (10%)
    commission_amount = db.Column(db.Float, default=0.0)
    seller_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to seller
    seller = db.relationship('User', foreign_keys=[seller_id], backref='sales')
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type} ${self.amount}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'transaction_type': self.transaction_type,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'seller_id': self.seller_id,
            'seller': self.seller.to_public_dict() if self.seller else None,
            'commission_rate': self.commission_rate,
            'commission_amount': self.commission_amount,
            'seller_amount': self.seller_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

