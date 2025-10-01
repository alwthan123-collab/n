from flask import Blueprint, request, jsonify
from src.models.item import Item, Category, DownloadLog, AdClick, db
from sqlalchemy import desc, func
import datetime

items_bp = Blueprint('items', __name__)

@items_bp.route('/items', methods=['GET'])
def get_items():
    """الحصول على قائمة العناصر مع إمكانية التصفية والبحث"""
    try:
        # معاملات البحث والتصفية
        item_type = request.args.get('type', 'all')  # 'app', 'book', or 'all'
        category = request.args.get('category', 'all')
        search_query = request.args.get('q', '').strip()
        sort_by = request.args.get('sort', 'new')  # 'new', 'popular', 'az'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # بناء الاستعلام
        query = Item.query
        
        # تصفية حسب النوع
        if item_type != 'all':
            query = query.filter(Item.type == item_type)
        
        # تصفية حسب الفئة
        if category != 'all':
            query = query.filter(Item.category == category)
        
        # البحث النصي
        if search_query:
            search_filter = f"%{search_query}%"
            query = query.filter(
                db.or_(
                    Item.title.like(search_filter),
                    Item.description.like(search_filter),
                    Item.category.like(search_filter)
                )
            )
        
        # الترتيب
        if sort_by == 'new':
            query = query.order_by(desc(Item.date_added))
        elif sort_by == 'popular':
            query = query.order_by(desc(Item.download_count))
        elif sort_by == 'az':
            query = query.order_by(Item.title)
        
        # التصفح بالصفحات
        items = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'items': [item.to_dict() for item in items.items],
            'pagination': {
                'page': page,
                'pages': items.pages,
                'per_page': per_page,
                'total': items.total,
                'has_next': items.has_next,
                'has_prev': items.has_prev
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    """الحصول على تفاصيل عنصر محدد"""
    try:
        item = Item.query.get_or_404(item_id)
        return jsonify({
            'success': True,
            'item': item.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/items', methods=['POST'])
def add_item():
    """إضافة عنصر جديد (للإدارة)"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['id', 'type', 'title', 'category', 'size', 'version', 'description', 'thumbnail', 'download_url']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        # التحقق من عدم وجود العنصر مسبقاً
        if Item.query.get(data['id']):
            return jsonify({'success': False, 'error': 'Item with this ID already exists'}), 400
        
        # إنشاء العنصر الجديد
        item = Item(
            id=data['id'],
            type=data['type'],
            title=data['title'],
            category=data['category'],
            size=data['size'],
            version=data['version'],
            description=data['description'],
            thumbnail=data['thumbnail'],
            download_url=data['download_url'],
            is_featured=data.get('is_featured', False)
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Item added successfully',
            'item': item.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/items/<item_id>/download', methods=['POST'])
def track_download(item_id):
    """تتبع التحميل وزيادة العداد"""
    try:
        item = Item.query.get_or_404(item_id)
        
        # زيادة عداد التحميل
        item.download_count += 1
        
        # تسجيل التحميل في السجل
        download_log = DownloadLog(
            item_id=item_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        
        db.session.add(download_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Download tracked successfully',
            'download_count': item.download_count
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/categories', methods=['GET'])
def get_categories():
    """الحصول على قائمة الفئات"""
    try:
        item_type = request.args.get('type', 'all')
        
        query = Category.query
        if item_type != 'all':
            query = query.filter(Category.type == item_type)
        
        categories = query.all()
        
        return jsonify({
            'success': True,
            'categories': [cat.to_dict() for cat in categories]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/featured', methods=['GET'])
def get_featured_items():
    """الحصول على العناصر المميزة"""
    try:
        limit = int(request.args.get('limit', 6))
        
        items = Item.query.filter(Item.is_featured == True).order_by(desc(Item.date_added)).limit(limit).all()
        
        return jsonify({
            'success': True,
            'items': [item.to_dict() for item in items]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/stats', methods=['GET'])
def get_stats():
    """إحصائيات الموقع"""
    try:
        total_apps = Item.query.filter(Item.type == 'app').count()
        total_books = Item.query.filter(Item.type == 'book').count()
        total_downloads = db.session.query(func.sum(Item.download_count)).scalar() or 0
        
        # أكثر العناصر تحميلاً
        popular_items = Item.query.order_by(desc(Item.download_count)).limit(5).all()
        
        # إحصائيات التحميل الأسبوعية
        week_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        weekly_downloads = DownloadLog.query.filter(DownloadLog.downloaded_at >= week_ago).count()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_apps': total_apps,
                'total_books': total_books,
                'total_items': total_apps + total_books,
                'total_downloads': total_downloads,
                'weekly_downloads': weekly_downloads,
                'popular_items': [item.to_dict() for item in popular_items]
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@items_bp.route('/ads/click', methods=['POST'])
def track_ad_click():
    """تتبع النقرات على الإعلانات"""
    try:
        data = request.get_json()
        
        ad_click = AdClick(
            ad_position=data.get('position', 'unknown'),
            page=data.get('page', 'unknown'),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            revenue=data.get('revenue', 0.0)
        )
        
        db.session.add(ad_click)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ad click tracked successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
