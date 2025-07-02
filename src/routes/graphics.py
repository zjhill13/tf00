from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import db
import json

graphics_bp = Blueprint('graphics', __name__)

# Sample graphics data
GRAPHICS_DATA = [
    {
        "id": 1,
        "title": "AI-Powered Dashboard UI Kit",
        "description": "Complete UI kit for AI and machine learning dashboards with 50+ components",
        "detailed_description": "A comprehensive UI kit designed specifically for AI and machine learning applications. Includes data visualization components, neural network diagrams, analytics charts, and futuristic interface elements. Perfect for creating professional AI dashboards, analytics platforms, and tech startups.",
        "category": "UI/UX Design",
        "subcategory": "Dashboard",
        "tags": ["UI Kit", "AI", "Dashboard", "Analytics", "Figma", "Sketch"],
        "creator": "DesignTech Studio",
        "creator_id": 1,
        "price": 89,
        "original_price": 149,
        "discount": 40,
        "status": "Available",
        "preview_image": "/images/graphics/ai-dashboard-preview.jpg",
        "gallery_images": [
            "/images/graphics/ai-dashboard-1.jpg",
            "/images/graphics/ai-dashboard-2.jpg",
            "/images/graphics/ai-dashboard-3.jpg"
        ],
        "file_formats": ["Figma", "Sketch", "Adobe XD", "PNG", "SVG"],
        "file_size": "45 MB",
        "downloads": 1247,
        "rating": 4.8,
        "reviews_count": 89,
        "created_date": "2024-01-15",
        "updated_date": "2024-01-20",
        "features": [
            "50+ UI components",
            "Dark and light themes",
            "Responsive design",
            "Vector graphics",
            "Easy customization",
            "Documentation included"
        ],
        "what_included": [
            "Figma source file",
            "Sketch source file",
            "Adobe XD file",
            "PNG exports (2x, 3x)",
            "SVG icons pack",
            "Color palette guide",
            "Typography guide",
            "Usage documentation"
        ],
        "license": "Commercial use allowed",
        "software_compatibility": ["Figma", "Sketch", "Adobe XD", "Photoshop", "Illustrator"]
    },
    {
        "id": 2,
        "title": "Sustainable Brand Identity Pack",
        "description": "Complete branding package for eco-friendly and sustainable businesses",
        "detailed_description": "A comprehensive brand identity package designed for sustainable and eco-friendly businesses. Includes logo variations, color palettes inspired by nature, typography selections, and brand guidelines. Perfect for green startups, environmental organizations, and conscious brands.",
        "category": "Branding",
        "subcategory": "Logo Design",
        "tags": ["Branding", "Logo", "Eco-friendly", "Sustainable", "Green", "Identity"],
        "creator": "EcoDesign Co.",
        "creator_id": 2,
        "price": 129,
        "original_price": 199,
        "discount": 35,
        "status": "Available",
        "preview_image": "/images/graphics/sustainable-brand-preview.jpg",
        "gallery_images": [
            "/images/graphics/sustainable-brand-1.jpg",
            "/images/graphics/sustainable-brand-2.jpg",
            "/images/graphics/sustainable-brand-3.jpg"
        ],
        "file_formats": ["AI", "EPS", "PNG", "SVG", "PDF"],
        "file_size": "78 MB",
        "downloads": 892,
        "rating": 4.9,
        "reviews_count": 67,
        "created_date": "2024-01-10",
        "updated_date": "2024-01-18",
        "features": [
            "5 logo variations",
            "Nature-inspired color palettes",
            "Typography recommendations",
            "Brand guidelines",
            "Business card templates",
            "Letterhead designs"
        ],
        "what_included": [
            "Adobe Illustrator files",
            "EPS vector files",
            "PNG files (transparent)",
            "SVG files",
            "Brand guidelines PDF",
            "Color palette swatches",
            "Font recommendations",
            "Usage examples"
        ],
        "license": "Extended commercial license",
        "software_compatibility": ["Adobe Illustrator", "Adobe Photoshop", "Canva", "Figma"]
    },
    {
        "id": 3,
        "title": "Futuristic Mobile App Icons",
        "description": "Set of 100 futuristic and tech-inspired mobile app icons",
        "detailed_description": "A collection of 100 professionally designed mobile app icons with a futuristic and technology theme. Each icon is crafted with attention to detail, featuring modern gradients, sleek designs, and perfect pixel alignment. Ideal for tech apps, AI applications, and innovative mobile products.",
        "category": "Icons",
        "subcategory": "Mobile Apps",
        "tags": ["Icons", "Mobile", "Futuristic", "Tech", "App Icons", "iOS", "Android"],
        "creator": "IconCraft Studio",
        "creator_id": 3,
        "price": 49,
        "original_price": 79,
        "discount": 38,
        "status": "Available",
        "preview_image": "/images/graphics/futuristic-icons-preview.jpg",
        "gallery_images": [
            "/images/graphics/futuristic-icons-1.jpg",
            "/images/graphics/futuristic-icons-2.jpg",
            "/images/graphics/futuristic-icons-3.jpg"
        ],
        "file_formats": ["PNG", "SVG", "ICO", "ICNS"],
        "file_size": "32 MB",
        "downloads": 2156,
        "rating": 4.7,
        "reviews_count": 143,
        "created_date": "2024-01-05",
        "updated_date": "2024-01-12",
        "features": [
            "100 unique icons",
            "Multiple sizes (16px to 512px)",
            "Retina ready",
            "iOS and Android compatible",
            "Consistent design style",
            "Easy to customize"
        ],
        "what_included": [
            "PNG files (multiple sizes)",
            "SVG vector files",
            "ICO files for Windows",
            "ICNS files for macOS",
            "Icon preview sheet",
            "Installation guide",
            "Color variations",
            "Naming convention guide"
        ],
        "license": "Royalty-free commercial use",
        "software_compatibility": ["Any image editor", "Xcode", "Android Studio", "Figma", "Sketch"]
    },
    {
        "id": 4,
        "title": "Social Media Graphics Bundle",
        "description": "Complete social media graphics package with templates for all platforms",
        "detailed_description": "A comprehensive social media graphics bundle containing over 200 templates for Instagram, Facebook, Twitter, LinkedIn, and TikTok. Includes post templates, story templates, cover designs, and promotional graphics. All templates are fully customizable and designed to increase engagement.",
        "category": "Social Media",
        "subcategory": "Templates",
        "tags": ["Social Media", "Instagram", "Facebook", "Templates", "Marketing", "Graphics"],
        "creator": "SocialDesign Pro",
        "creator_id": 4,
        "price": 79,
        "original_price": 129,
        "discount": 39,
        "status": "Available",
        "preview_image": "/images/graphics/social-media-preview.jpg",
        "gallery_images": [
            "/images/graphics/social-media-1.jpg",
            "/images/graphics/social-media-2.jpg",
            "/images/graphics/social-media-3.jpg"
        ],
        "file_formats": ["PSD", "AI", "PNG", "JPG"],
        "file_size": "156 MB",
        "downloads": 1789,
        "rating": 4.6,
        "reviews_count": 234,
        "created_date": "2024-01-08",
        "updated_date": "2024-01-22",
        "features": [
            "200+ templates",
            "All major platforms covered",
            "Easy text editing",
            "High-resolution graphics",
            "Trendy designs",
            "Color variations included"
        ],
        "what_included": [
            "Photoshop PSD files",
            "Illustrator AI files",
            "PNG exports",
            "JPG exports",
            "Font list",
            "Color palette guide",
            "Size specifications",
            "Usage instructions"
        ],
        "license": "Commercial use with attribution",
        "software_compatibility": ["Adobe Photoshop", "Adobe Illustrator", "Canva", "GIMP"]
    },
    {
        "id": 5,
        "title": "Minimalist Website Illustrations",
        "description": "Set of 50 minimalist illustrations perfect for modern websites",
        "detailed_description": "A curated collection of 50 minimalist illustrations designed for modern websites and applications. Each illustration follows a consistent style with clean lines, subtle colors, and contemporary aesthetics. Perfect for landing pages, about sections, and feature explanations.",
        "category": "Illustrations",
        "subcategory": "Website",
        "tags": ["Illustrations", "Minimalist", "Website", "Modern", "Clean", "Vector"],
        "creator": "MinimalArt Studio",
        "creator_id": 5,
        "price": 69,
        "original_price": 99,
        "discount": 30,
        "status": "Available",
        "preview_image": "/images/graphics/minimalist-illustrations-preview.jpg",
        "gallery_images": [
            "/images/graphics/minimalist-illustrations-1.jpg",
            "/images/graphics/minimalist-illustrations-2.jpg",
            "/images/graphics/minimalist-illustrations-3.jpg"
        ],
        "file_formats": ["AI", "SVG", "PNG", "EPS"],
        "file_size": "89 MB",
        "downloads": 1456,
        "rating": 4.8,
        "reviews_count": 98,
        "created_date": "2024-01-12",
        "updated_date": "2024-01-19",
        "features": [
            "50 unique illustrations",
            "Consistent style",
            "Scalable vectors",
            "Web-optimized",
            "Easy to customize",
            "Multiple formats"
        ],
        "what_included": [
            "Adobe Illustrator files",
            "SVG vector files",
            "PNG files (transparent)",
            "EPS files",
            "Color guide",
            "Style guide",
            "Usage examples",
            "Web optimization tips"
        ],
        "license": "Extended commercial license",
        "software_compatibility": ["Adobe Illustrator", "Figma", "Sketch", "Inkscape"]
    }
]

@graphics_bp.route('/api/graphics', methods=['GET'])
@jwt_required()
def get_graphics():
    """Get all graphics (member-only access)"""
    try:
        current_user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category', None)
        sort_by = request.args.get('sort_by', 'newest')  # newest, popular, price_low, price_high
        
        # Filter by category if provided
        graphics = GRAPHICS_DATA
        if category:
            graphics = [graphic for graphic in graphics if graphic['category'].lower() == category.lower()]
        
        # Sort graphics
        if sort_by == 'popular':
            graphics = sorted(graphics, key=lambda x: x['downloads'], reverse=True)
        elif sort_by == 'price_low':
            graphics = sorted(graphics, key=lambda x: x['price'])
        elif sort_by == 'price_high':
            graphics = sorted(graphics, key=lambda x: x['price'], reverse=True)
        elif sort_by == 'rating':
            graphics = sorted(graphics, key=lambda x: x['rating'], reverse=True)
        else:  # newest
            graphics = sorted(graphics, key=lambda x: x['created_date'], reverse=True)
        
        # Implement pagination
        start = (page - 1) * per_page
        end = start + per_page
        paginated_graphics = graphics[start:end]
        
        return jsonify({
            'success': True,
            'data': paginated_graphics,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': len(graphics),
                'pages': (len(graphics) + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching graphics: {str(e)}'
        }), 500

@graphics_bp.route('/api/graphics/<int:graphic_id>', methods=['GET'])
@jwt_required()
def get_graphic_detail(graphic_id):
    """Get detailed information about a specific graphic"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find the graphic by ID
        graphic = next((graphic for graphic in GRAPHICS_DATA if graphic['id'] == graphic_id), None)
        
        if not graphic:
            return jsonify({
                'success': False,
                'message': 'Graphic not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': graphic
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching graphic: {str(e)}'
        }), 500

@graphics_bp.route('/api/graphics/categories', methods=['GET'])
def get_graphic_categories():
    """Get all available graphic categories (public endpoint)"""
    try:
        categories = list(set([graphic['category'] for graphic in GRAPHICS_DATA]))
        return jsonify({
            'success': True,
            'data': categories
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching categories: {str(e)}'
        }), 500

@graphics_bp.route('/api/graphics/<int:graphic_id>/purchase', methods=['POST'])
@jwt_required()
def purchase_graphic(graphic_id):
    """Purchase a graphic"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find the graphic by ID
        graphic = next((graphic for graphic in GRAPHICS_DATA if graphic['id'] == graphic_id), None)
        
        if not graphic:
            return jsonify({
                'success': False,
                'message': 'Graphic not found'
            }), 404
        
        # In a real implementation, this would:
        # 1. Process payment through Stripe/PayPal
        # 2. Create a purchase record in the database
        # 3. Grant access to download files
        # 4. Send confirmation email with download links
        
        return jsonify({
            'success': True,
            'message': f'Successfully purchased "{graphic["title"]}" for ${graphic["price"]}',
            'data': {
                'graphic_id': graphic_id,
                'title': graphic['title'],
                'price': graphic['price'],
                'purchase_date': '2024-01-01T00:00:00Z',
                'download_links': [
                    f'/api/graphics/{graphic_id}/download/source',
                    f'/api/graphics/{graphic_id}/download/preview',
                    f'/api/graphics/{graphic_id}/download/documentation'
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing purchase: {str(e)}'
        }), 500

@graphics_bp.route('/api/graphics/<int:graphic_id>/download/<file_type>', methods=['GET'])
@jwt_required()
def download_graphic_file(graphic_id, file_type):
    """Download graphic files after purchase"""
    try:
        current_user_id = get_jwt_identity()
        
        # Find the graphic by ID
        graphic = next((graphic for graphic in GRAPHICS_DATA if graphic['id'] == graphic_id), None)
        
        if not graphic:
            return jsonify({
                'success': False,
                'message': 'Graphic not found'
            }), 404
        
        # In a real implementation, this would:
        # 1. Verify user has purchased this graphic
        # 2. Generate secure download link
        # 3. Track download analytics
        # 4. Return actual file or redirect to file URL
        
        download_info = {
            'source': {
                'filename': f'{graphic["title"].replace(" ", "_")}_Source_Files.zip',
                'description': 'Complete source files in all available formats',
                'size': graphic['file_size']
            },
            'preview': {
                'filename': f'{graphic["title"].replace(" ", "_")}_Preview.pdf',
                'description': 'High-resolution preview of all graphics',
                'size': '5 MB'
            },
            'documentation': {
                'filename': f'{graphic["title"].replace(" ", "_")}_Documentation.pdf',
                'description': 'Usage guide and license information',
                'size': '2 MB'
            }
        }
        
        if file_type not in download_info:
            return jsonify({
                'success': False,
                'message': 'Invalid file type'
            }), 400
        
        return jsonify({
            'success': True,
            'message': 'Download ready',
            'data': {
                'download_url': f'/downloads/{graphic_id}/{file_type}',
                'filename': download_info[file_type]['filename'],
                'description': download_info[file_type]['description'],
                'size': download_info[file_type]['size'],
                'expires_at': '2024-01-08T00:00:00Z'  # 7 days from now
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error processing download: {str(e)}'
        }), 500

@graphics_bp.route('/api/graphics/creator/<int:creator_id>', methods=['GET'])
@jwt_required()
def get_creator_graphics(creator_id):
    """Get all graphics by a specific creator"""
    try:
        current_user_id = get_jwt_identity()
        
        creator_graphics = [graphic for graphic in GRAPHICS_DATA if graphic['creator_id'] == creator_id]
        
        return jsonify({
            'success': True,
            'data': creator_graphics,
            'total': len(creator_graphics)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching creator graphics: {str(e)}'
        }), 500

