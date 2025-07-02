from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.models.user import User, db
from src.models.business_idea import BusinessIdea
from src.models.service import Service
from src.models.transaction import Transaction
import json

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/business-ideas', methods=['GET'])
def get_business_ideas():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')
        
        # Build query
        query = BusinessIdea.query.filter_by(is_published=True)
        
        if category and category != 'all':
            query = query.filter(BusinessIdea.category == category)
        
        if search:
            query = query.filter(
                BusinessIdea.title.contains(search) | 
                BusinessIdea.description.contains(search)
            )
        
        # Apply sorting
        if sort_by == 'price':
            if order == 'asc':
                query = query.order_by(BusinessIdea.price.asc())
            else:
                query = query.order_by(BusinessIdea.price.desc())
        elif sort_by == 'rating':
            query = query.order_by(BusinessIdea.rating.desc())
        elif sort_by == 'sales':
            query = query.order_by(BusinessIdea.sales_count.desc())
        else:  # created_at
            if order == 'asc':
                query = query.order_by(BusinessIdea.created_at.asc())
            else:
                query = query.order_by(BusinessIdea.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        ideas = pagination.items
        
        return jsonify({
            'business_ideas': [idea.to_summary_dict() for idea in ideas],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/business-ideas/<int:idea_id>', methods=['GET'])
def get_business_idea(idea_id):
    try:
        idea = BusinessIdea.query.get(idea_id)
        
        if not idea or not idea.is_published:
            return jsonify({'error': 'Business idea not found'}), 404
        
        return jsonify({'business_idea': idea.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/business-ideas', methods=['POST'])
@jwt_required()
def create_business_idea():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.user_type != 'creator':
            return jsonify({'error': 'Only creators can create business ideas'}), 403
        
        # Check subscription tier
        if user.subscription_tier == 'basic':
            return jsonify({'error': 'Upgrade to Inventor or Guru plan to create business ideas'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'price']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create business idea
        idea = BusinessIdea(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            price=float(data['price']),
            creator_id=user_id,
            tags=json.dumps(data.get('tags', [])),
            image_url=data.get('image_url', ''),
            executive_summary=data.get('executive_summary', ''),
            market_analysis=data.get('market_analysis', ''),
            business_model=data.get('business_model', ''),
            financial_projections=data.get('financial_projections', ''),
            marketing_strategy=data.get('marketing_strategy', ''),
            is_published=data.get('is_published', False)
        )
        
        db.session.add(idea)
        db.session.commit()
        
        return jsonify({
            'message': 'Business idea created successfully',
            'business_idea': idea.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/services', methods=['GET'])
def get_services():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'desc')
        
        # Build query
        query = Service.query.filter_by(is_published=True)
        
        if category and category != 'all':
            query = query.filter(Service.category == category)
        
        if search:
            query = query.filter(
                Service.title.contains(search) | 
                Service.description.contains(search)
            )
        
        # Apply sorting
        if sort_by == 'price':
            if order == 'asc':
                query = query.order_by(Service.starting_price.asc())
            else:
                query = query.order_by(Service.starting_price.desc())
        elif sort_by == 'rating':
            query = query.order_by(Service.rating.desc())
        elif sort_by == 'orders':
            query = query.order_by(Service.orders_count.desc())
        else:  # created_at
            if order == 'asc':
                query = query.order_by(Service.created_at.asc())
            else:
                query = query.order_by(Service.created_at.desc())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        services = pagination.items
        
        return jsonify({
            'services': [service.to_summary_dict() for service in services],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    try:
        service = Service.query.get(service_id)
        
        if not service or not service.is_published:
            return jsonify({'error': 'Service not found'}), 404
        
        return jsonify({'service': service.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/services', methods=['POST'])
@jwt_required()
def create_service():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.user_type != 'creator':
            return jsonify({'error': 'Only creators can create services'}), 403
        
        # Check subscription tier
        if user.subscription_tier == 'basic':
            return jsonify({'error': 'Upgrade to Inventor or Guru plan to create services'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'starting_price', 'delivery_time']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create service
        service = Service(
            title=data['title'],
            description=data['description'],
            category=data['category'],
            starting_price=float(data['starting_price']),
            delivery_time=data['delivery_time'],
            creator_id=user_id,
            image_url=data.get('image_url', ''),
            packages=json.dumps(data.get('packages', [])),
            is_published=data.get('is_published', False)
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'message': 'Service created successfully',
            'service': service.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/purchase', methods=['POST'])
@jwt_required()
def purchase_item():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['item_type', 'item_id', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        item_type = data['item_type']
        item_id = data['item_id']
        amount = float(data['amount'])
        
        # Get the item and seller
        seller_id = None
        if item_type == 'business_idea':
            item = BusinessIdea.query.get(item_id)
            if not item or not item.is_published:
                return jsonify({'error': 'Business idea not found'}), 404
            seller_id = item.creator_id
        elif item_type == 'service':
            item = Service.query.get(item_id)
            if not item or not item.is_published:
                return jsonify({'error': 'Service not found'}), 404
            seller_id = item.creator_id
        else:
            return jsonify({'error': 'Invalid item type'}), 400
        
        # Calculate commission
        commission_rate = 0.1  # 10%
        commission_amount = amount * commission_rate
        seller_amount = amount - commission_amount
        
        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            transaction_type='purchase',
            item_type=item_type,
            item_id=item_id,
            amount=amount,
            status='completed',  # In real app, this would be 'pending' until payment is processed
            payment_method=data.get('payment_method', 'credit_card'),
            seller_id=seller_id,
            commission_rate=commission_rate,
            commission_amount=commission_amount,
            seller_amount=seller_amount
        )
        
        db.session.add(transaction)
        
        # Update item sales count
        if item_type == 'business_idea':
            item.sales_count += 1
        elif item_type == 'service':
            item.orders_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Purchase completed successfully',
            'transaction': transaction.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available categories for business ideas and services"""
    categories = [
        'Technology',
        'E-commerce',
        'Healthcare',
        'Education',
        'Finance',
        'Entertainment',
        'Food & Beverage',
        'Real Estate',
        'Sustainability',
        'Marketing',
        'Consulting',
        'Design'
    ]
    
    return jsonify({'categories': categories}), 200

@marketplace_bp.route('/my-creations', methods=['GET'])
@jwt_required()
def get_my_creations():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.user_type != 'creator':
            return jsonify({'error': 'Only creators can view their creations'}), 403
        
        # Get user's business ideas
        business_ideas = BusinessIdea.query.filter_by(creator_id=user_id).all()
        
        # Get user's services
        services = Service.query.filter_by(creator_id=user_id).all()
        
        return jsonify({
            'business_ideas': [idea.to_summary_dict() for idea in business_ideas],
            'services': [service.to_summary_dict() for service in services]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/my-purchases', methods=['GET'])
@jwt_required()
def get_my_purchases():
    try:
        user_id = get_jwt_identity()
        
        # Get user's purchase transactions
        transactions = Transaction.query.filter_by(
            user_id=user_id, 
            transaction_type='purchase'
        ).order_by(Transaction.created_at.desc()).all()
        
        return jsonify({
            'purchases': [transaction.to_dict() for transaction in transactions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

