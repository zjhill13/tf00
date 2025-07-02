from src.models.user import db
from datetime import datetime

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    team_type = db.Column(db.String(50), default='standard')  # standard, enterprise, premium
    max_members = db.Column(db.Integer, default=10)
    settings = db.Column(db.Text, nullable=True)  # JSON string for team settings
    
    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id], backref='owned_teams')
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')
    projects = db.relationship('TeamProject', backref='team', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Team {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'owner': self.owner.to_public_dict() if self.owner else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'team_type': self.team_type,
            'max_members': self.max_members,
            'member_count': len(self.members),
            'settings': self.settings
        }
    
    def get_member_count(self):
        return len([m for m in self.members if m.status == 'active'])
    
    def can_add_member(self):
        return self.get_member_count() < self.max_members

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='member')  # owner, admin, member, viewer
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, active, inactive
    permissions = db.Column(db.Text, nullable=True)  # JSON string for custom permissions
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    invited_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='team_memberships')
    inviter = db.relationship('User', foreign_keys=[invited_by])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('team_id', 'user_id', name='unique_team_member'),)
    
    def __repr__(self):
        return f'<TeamMember {self.user_id} in Team {self.team_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'role': self.role,
            'status': self.status,
            'permissions': self.permissions,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'invited_by': self.invited_by,
            'inviter': self.inviter.to_public_dict() if self.inviter else None,
            'last_active': self.last_active.isoformat() if self.last_active else None
        }

class TeamProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    project_type = db.Column(db.String(50), nullable=False)  # business_idea, service, campaign
    status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, archived
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    tags = db.Column(db.Text, nullable=True)  # JSON string
    
    # Project data (JSON)
    project_data = db.Column(db.Text, nullable=True)  # JSON string containing project-specific data
    
    # Relationships
    creator = db.relationship('User', foreign_keys=[created_by])
    collaborations = db.relationship('ProjectCollaboration', backref='project', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('TeamActivity', backref='project', lazy=True)
    
    def __repr__(self):
        return f'<TeamProject {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'name': self.name,
            'description': self.description,
            'project_type': self.project_type,
            'status': self.status,
            'created_by': self.created_by,
            'creator': self.creator.to_public_dict() if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'tags': self.tags,
            'project_data': self.project_data,
            'collaboration_count': len(self.collaborations)
        }

class ProjectCollaboration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('team_project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='contributor')  # lead, contributor, reviewer
    contribution_type = db.Column(db.String(50), nullable=True)  # idea, design, development, review
    status = db.Column(db.String(20), nullable=False, default='active')  # active, completed, paused
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('project_id', 'user_id', name='unique_project_collaboration'),)
    
    def __repr__(self):
        return f'<ProjectCollaboration {self.user_id} on Project {self.project_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'role': self.role,
            'contribution_type': self.contribution_type,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes
        }

class TeamActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('team_project.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # created, updated, commented, completed, etc.
    activity_data = db.Column(db.Text, nullable=True)  # JSON string with activity details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<TeamActivity {self.activity_type} by {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'activity_type': self.activity_type,
            'activity_data': self.activity_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_public': self.is_public
        }

class TeamInvitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    invited_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='member')
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, accepted, declined, expired
    token = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    accepted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    team = db.relationship('Team', foreign_keys=[team_id])
    inviter = db.relationship('User', foreign_keys=[invited_by])
    
    def __repr__(self):
        return f'<TeamInvitation {self.email} to Team {self.team_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'team_id': self.team_id,
            'team': self.team.to_dict() if self.team else None,
            'email': self.email,
            'invited_by': self.invited_by,
            'inviter': self.inviter.to_public_dict() if self.inviter else None,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None
        }

