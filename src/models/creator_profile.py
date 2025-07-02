from src.models.user import db
from datetime import datetime

class CreatorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    # Professional Information
    professional_title = db.Column(db.String(200), nullable=True)
    tagline = db.Column(db.String(500), nullable=True)
    years_experience = db.Column(db.Integer, nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    availability = db.Column(db.String(50), nullable=True)  # full-time, part-time, contract, freelance
    
    # Resume and Documents
    resume_url = db.Column(db.String(500), nullable=True)
    portfolio_url = db.Column(db.String(500), nullable=True)
    linkedin_url = db.Column(db.String(500), nullable=True)
    website_url = db.Column(db.String(500), nullable=True)
    github_url = db.Column(db.String(500), nullable=True)
    
    # Skills and Expertise
    skills = db.Column(db.Text, nullable=True)  # JSON array of skills
    industries = db.Column(db.Text, nullable=True)  # JSON array of industries
    languages = db.Column(db.Text, nullable=True)  # JSON array of languages
    certifications = db.Column(db.Text, nullable=True)  # JSON array of certifications
    
    # Location and Contact
    location = db.Column(db.String(200), nullable=True)
    timezone = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Profile Status
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_available_for_hire = db.Column(db.Boolean, default=True)
    profile_completion = db.Column(db.Integer, default=0)  # Percentage 0-100
    
    # Statistics
    total_projects = db.Column(db.Integer, default=0)
    completed_projects = db.Column(db.Integer, default=0)
    client_satisfaction = db.Column(db.Float, default=0.0)  # Average rating
    response_time = db.Column(db.String(50), nullable=True)  # e.g., "within 1 hour"
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('creator_profile', uselist=False))
    work_experiences = db.relationship('WorkExperience', backref='creator_profile', lazy=True, cascade='all, delete-orphan')
    educations = db.relationship('Education', backref='creator_profile', lazy=True, cascade='all, delete-orphan')
    portfolio_items = db.relationship('PortfolioItem', backref='creator_profile', lazy=True, cascade='all, delete-orphan')
    service_packages = db.relationship('ServicePackage', backref='creator_profile', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CreatorProfile for User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'professional_title': self.professional_title,
            'tagline': self.tagline,
            'years_experience': self.years_experience,
            'hourly_rate': self.hourly_rate,
            'availability': self.availability,
            'resume_url': self.resume_url,
            'portfolio_url': self.portfolio_url,
            'linkedin_url': self.linkedin_url,
            'website_url': self.website_url,
            'github_url': self.github_url,
            'skills': self.skills,
            'industries': self.industries,
            'languages': self.languages,
            'certifications': self.certifications,
            'location': self.location,
            'timezone': self.timezone,
            'phone': self.phone,
            'is_verified': self.is_verified,
            'is_featured': self.is_featured,
            'is_available_for_hire': self.is_available_for_hire,
            'profile_completion': self.profile_completion,
            'total_projects': self.total_projects,
            'completed_projects': self.completed_projects,
            'client_satisfaction': self.client_satisfaction,
            'response_time': self.response_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'work_experiences': [exp.to_dict() for exp in self.work_experiences],
            'educations': [edu.to_dict() for edu in self.educations],
            'portfolio_items': [item.to_dict() for item in self.portfolio_items],
            'service_packages': [pkg.to_dict() for pkg in self.service_packages]
        }
    
    def to_summary_dict(self):
        """Simplified version for listings"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'professional_title': self.professional_title,
            'tagline': self.tagline,
            'years_experience': self.years_experience,
            'hourly_rate': self.hourly_rate,
            'availability': self.availability,
            'location': self.location,
            'skills': self.skills,
            'industries': self.industries,
            'is_verified': self.is_verified,
            'is_featured': self.is_featured,
            'is_available_for_hire': self.is_available_for_hire,
            'profile_completion': self.profile_completion,
            'completed_projects': self.completed_projects,
            'client_satisfaction': self.client_satisfaction,
            'response_time': self.response_time
        }

class WorkExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('creator_profile.id'), nullable=False)
    
    company_name = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # Null if current job
    is_current = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(200), nullable=True)
    company_url = db.Column(db.String(500), nullable=True)
    achievements = db.Column(db.Text, nullable=True)  # JSON array of achievements
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<WorkExperience {self.position} at {self.company_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_profile_id': self.creator_profile_id,
            'company_name': self.company_name,
            'position': self.position,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'location': self.location,
            'company_url': self.company_url,
            'achievements': self.achievements,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('creator_profile.id'), nullable=False)
    
    institution_name = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    field_of_study = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=False)
    gpa = db.Column(db.Float, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Education {self.degree} from {self.institution_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_profile_id': self.creator_profile_id,
            'institution_name': self.institution_name,
            'degree': self.degree,
            'field_of_study': self.field_of_study,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_current': self.is_current,
            'gpa': self.gpa,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PortfolioItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('creator_profile.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)
    project_type = db.Column(db.String(100), nullable=True)  # web, mobile, design, business_plan, etc.
    
    # Media and Links
    image_url = db.Column(db.String(500), nullable=True)
    project_url = db.Column(db.String(500), nullable=True)
    demo_url = db.Column(db.String(500), nullable=True)
    github_url = db.Column(db.String(500), nullable=True)
    
    # Project Details
    technologies_used = db.Column(db.Text, nullable=True)  # JSON array
    client_name = db.Column(db.String(200), nullable=True)
    project_duration = db.Column(db.String(100), nullable=True)
    budget_range = db.Column(db.String(100), nullable=True)
    
    # Status and Visibility
    is_featured = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    completion_date = db.Column(db.Date, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PortfolioItem {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_profile_id': self.creator_profile_id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'project_type': self.project_type,
            'image_url': self.image_url,
            'project_url': self.project_url,
            'demo_url': self.demo_url,
            'github_url': self.github_url,
            'technologies_used': self.technologies_used,
            'client_name': self.client_name,
            'project_duration': self.project_duration,
            'budget_range': self.budget_range,
            'is_featured': self.is_featured,
            'is_public': self.is_public,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class ServicePackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('creator_profile.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    
    # Pricing
    price = db.Column(db.Float, nullable=False)
    pricing_type = db.Column(db.String(50), nullable=False, default='fixed')  # fixed, hourly, project
    
    # Service Details
    delivery_time = db.Column(db.String(100), nullable=False)
    revisions_included = db.Column(db.Integer, default=1)
    features = db.Column(db.Text, nullable=True)  # JSON array of features
    requirements = db.Column(db.Text, nullable=True)  # What client needs to provide
    
    # Add-ons and Extras
    addons = db.Column(db.Text, nullable=True)  # JSON array of additional services
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Statistics
    orders_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ServicePackage {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_profile_id': self.creator_profile_id,
            'creator_profile': self.creator_profile.to_summary_dict() if self.creator_profile else None,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'pricing_type': self.pricing_type,
            'delivery_time': self.delivery_time,
            'revisions_included': self.revisions_included,
            'features': self.features,
            'requirements': self.requirements,
            'addons': self.addons,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'orders_count': self.orders_count,
            'rating': self.rating,
            'review_count': self.review_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CreatorReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_profile_id = db.Column(db.Integer, db.ForeignKey('creator_profile.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Review Details
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(200), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    
    # Project Context
    project_type = db.Column(db.String(100), nullable=True)
    service_package_id = db.Column(db.Integer, db.ForeignKey('service_package.id'), nullable=True)
    business_idea_id = db.Column(db.Integer, db.ForeignKey('business_idea.id'), nullable=True)
    
    # Review Metrics
    communication_rating = db.Column(db.Integer, nullable=True)  # 1-5
    quality_rating = db.Column(db.Integer, nullable=True)  # 1-5
    delivery_rating = db.Column(db.Integer, nullable=True)  # 1-5
    value_rating = db.Column(db.Integer, nullable=True)  # 1-5
    
    # Status
    is_verified = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator_profile = db.relationship('CreatorProfile', backref='reviews')
    reviewer = db.relationship('User', foreign_keys=[reviewer_id])
    service_package = db.relationship('ServicePackage', foreign_keys=[service_package_id])
    
    def __repr__(self):
        return f'<CreatorReview {self.rating} stars for Creator {self.creator_profile_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'creator_profile_id': self.creator_profile_id,
            'reviewer_id': self.reviewer_id,
            'reviewer': self.reviewer.to_public_dict() if self.reviewer else None,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'project_type': self.project_type,
            'service_package_id': self.service_package_id,
            'business_idea_id': self.business_idea_id,
            'communication_rating': self.communication_rating,
            'quality_rating': self.quality_rating,
            'delivery_rating': self.delivery_rating,
            'value_rating': self.value_rating,
            'is_verified': self.is_verified,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

