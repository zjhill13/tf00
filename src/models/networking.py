from src.models.user import db
from datetime import datetime

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, accepted, declined, blocked
    message = db.Column(db.Text, nullable=True)  # Connection request message
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    requester = db.relationship('User', foreign_keys=[requester_id], backref='sent_connections')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_connections')
    
    # Unique constraint to prevent duplicate connections
    __table_args__ = (db.UniqueConstraint('requester_id', 'recipient_id', name='unique_connection'),)
    
    def __repr__(self):
        return f'<Connection {self.requester_id} -> {self.recipient_id} ({self.status})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'recipient_id': self.recipient_id,
            'requester': self.requester.to_public_dict() if self.requester else None,
            'recipient': self.recipient.to_public_dict() if self.recipient else None,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50), nullable=False, default='text')  # text, image, video, article, project_showcase, idea_share
    
    # Media attachments
    media_urls = db.Column(db.Text, nullable=True)  # JSON array of media URLs
    
    # Post metadata
    tags = db.Column(db.Text, nullable=True)  # JSON array of hashtags
    mentions = db.Column(db.Text, nullable=True)  # JSON array of mentioned user IDs
    
    # Visibility and engagement
    visibility = db.Column(db.String(20), nullable=False, default='public')  # public, connections, private
    is_featured = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # Linked content
    business_idea_id = db.Column(db.Integer, db.ForeignKey('business_idea.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)
    portfolio_item_id = db.Column(db.Integer, db.ForeignKey('portfolio_item.id'), nullable=True)
    
    # Engagement metrics
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', foreign_keys=[author_id], backref='posts')
    business_idea = db.relationship('BusinessIdea', foreign_keys=[business_idea_id])
    service = db.relationship('Service', foreign_keys=[service_id])
    portfolio_item = db.relationship('PortfolioItem', foreign_keys=[portfolio_item_id])
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('PostComment', backref='post', lazy=True, cascade='all, delete-orphan')
    shares = db.relationship('PostShare', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.id} by {self.author_id}>'
    
    def to_dict(self, current_user_id=None):
        # Check if current user has liked this post
        user_liked = False
        if current_user_id:
            user_liked = any(like.user_id == current_user_id for like in self.likes)
        
        return {
            'id': self.id,
            'author_id': self.author_id,
            'author': self.author.to_public_dict() if self.author else None,
            'content': self.content,
            'post_type': self.post_type,
            'media_urls': self.media_urls,
            'tags': self.tags,
            'mentions': self.mentions,
            'visibility': self.visibility,
            'is_featured': self.is_featured,
            'is_pinned': self.is_pinned,
            'business_idea_id': self.business_idea_id,
            'service_id': self.service_id,
            'portfolio_item_id': self.portfolio_item_id,
            'business_idea': self.business_idea.to_summary_dict() if self.business_idea else None,
            'service': self.service.to_summary_dict() if self.service else None,
            'portfolio_item': self.portfolio_item.to_dict() if self.portfolio_item else None,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'shares_count': self.shares_count,
            'views_count': self.views_count,
            'user_liked': user_liked,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('post_id', 'user_id', name='unique_post_like'),)
    
    def __repr__(self):
        return f'<PostLike {self.user_id} on Post {self.post_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'), nullable=True)  # For replies
    content = db.Column(db.Text, nullable=False)
    mentions = db.Column(db.Text, nullable=True)  # JSON array of mentioned user IDs
    
    # Engagement
    likes_count = db.Column(db.Integer, default=0)
    replies_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    parent_comment = db.relationship('PostComment', remote_side=[id], backref='replies')
    comment_likes = db.relationship('CommentLike', backref='comment', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PostComment {self.id} by {self.user_id}>'
    
    def to_dict(self, current_user_id=None):
        # Check if current user has liked this comment
        user_liked = False
        if current_user_id:
            user_liked = any(like.user_id == current_user_id for like in self.comment_likes)
        
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'parent_comment_id': self.parent_comment_id,
            'content': self.content,
            'mentions': self.mentions,
            'likes_count': self.likes_count,
            'replies_count': self.replies_count,
            'user_liked': user_liked,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'replies': [reply.to_dict(current_user_id) for reply in self.replies] if self.replies else []
        }

class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('comment_id', 'user_id', name='unique_comment_like'),)

class PostShare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    share_message = db.Column(db.Text, nullable=True)  # Optional message when sharing
    share_type = db.Column(db.String(20), nullable=False, default='repost')  # repost, quote, external
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<PostShare {self.user_id} shared Post {self.post_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'share_message': self.share_message,
            'share_type': self.share_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), nullable=False, default='text')  # text, image, file, voice
    
    # File attachments
    attachment_url = db.Column(db.String(500), nullable=True)
    attachment_name = db.Column(db.String(200), nullable=True)
    attachment_size = db.Column(db.Integer, nullable=True)
    
    # Message status
    is_read = db.Column(db.Boolean, default=False)
    is_edited = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id])
    conversation = db.relationship('Conversation', backref='messages')
    
    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'sender_id': self.sender_id,
            'sender': self.sender.to_public_dict() if self.sender else None,
            'content': self.content,
            'message_type': self.message_type,
            'attachment_url': self.attachment_url,
            'attachment_name': self.attachment_name,
            'attachment_size': self.attachment_size,
            'is_read': self.is_read,
            'is_edited': self.is_edited,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_type = db.Column(db.String(20), nullable=False, default='direct')  # direct, group
    title = db.Column(db.String(200), nullable=True)  # For group conversations
    description = db.Column(db.Text, nullable=True)
    
    # Conversation settings
    is_archived = db.Column(db.Boolean, default=False)
    is_muted = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    participants = db.relationship('ConversationParticipant', backref='conversation', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Conversation {self.id} ({self.conversation_type})>'
    
    def to_dict(self, current_user_id=None):
        # Get unread message count for current user
        unread_count = 0
        if current_user_id:
            participant = next((p for p in self.participants if p.user_id == current_user_id), None)
            if participant:
                unread_count = len([m for m in self.messages if not m.is_read and m.sender_id != current_user_id])
        
        # Get last message
        last_message = None
        if self.messages:
            last_message = sorted(self.messages, key=lambda x: x.created_at, reverse=True)[0].to_dict()
        
        return {
            'id': self.id,
            'conversation_type': self.conversation_type,
            'title': self.title,
            'description': self.description,
            'is_archived': self.is_archived,
            'is_muted': self.is_muted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'participants': [p.to_dict() for p in self.participants],
            'unread_count': unread_count,
            'last_message': last_message
        }

class ConversationParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')  # admin, member
    status = db.Column(db.String(20), nullable=False, default='active')  # active, left, removed
    
    # Participant settings
    is_muted = db.Column(db.Boolean, default=False)
    last_read_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('conversation_id', 'user_id', name='unique_conversation_participant'),)
    
    def __repr__(self):
        return f'<ConversationParticipant {self.user_id} in {self.conversation_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'role': self.role,
            'status': self.status,
            'is_muted': self.is_muted,
            'last_read_at': self.last_read_at.isoformat() if self.last_read_at else None,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'left_at': self.left_at.isoformat() if self.left_at else None
        }

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    follower = db.relationship('User', foreign_keys=[follower_id], backref='following_relationships')
    following = db.relationship('User', foreign_keys=[following_id], backref='follower_relationships')
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('follower_id', 'following_id', name='unique_follow'),)
    
    def __repr__(self):
        return f'<Follow {self.follower_id} -> {self.following_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'following_id': self.following_id,
            'follower': self.follower.to_public_dict() if self.follower else None,
            'following': self.following.to_public_dict() if self.following else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # connection_request, post_like, comment, message, etc.
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Related entities
    related_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    related_post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    related_comment_id = db.Column(db.Integer, db.ForeignKey('post_comment.id'), nullable=True)
    
    # Action URL
    action_url = db.Column(db.String(500), nullable=True)
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    is_archived = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='notifications')
    related_user = db.relationship('User', foreign_keys=[related_user_id])
    related_post = db.relationship('Post', foreign_keys=[related_post_id])
    related_comment = db.relationship('PostComment', foreign_keys=[related_comment_id])
    
    def __repr__(self):
        return f'<Notification {self.notification_type} for {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'related_user_id': self.related_user_id,
            'related_user': self.related_user.to_public_dict() if self.related_user else None,
            'related_post_id': self.related_post_id,
            'related_comment_id': self.related_comment_id,
            'action_url': self.action_url,
            'is_read': self.is_read,
            'is_archived': self.is_archived,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

