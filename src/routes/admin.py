from flask import Blueprint, request, jsonify, render_template_string
from src.models.item import Item, Category, DownloadLog, AdClick, db
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import os

admin_bp = Blueprint('admin', __name__)

# كلمة مرور بسيطة للإدارة (يجب تغييرها في الإنتاج)
ADMIN_PASSWORD = "emperor_admin_2025"

def verify_admin(password):
    return password == ADMIN_PASSWORD

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """تسجيل دخول الإدارة"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if verify_admin(password):
            return jsonify({
                'success': True,
                'message': 'تم تسجيل الدخول بنجاح',
                'token': 'admin_authenticated'  # في الإنتاج يجب استخدام JWT
            })
        else:
            return jsonify({
                'success': False,
                'message': 'كلمة مرور خاطئة'
            }), 401
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    """لوحة تحكم الإدارة"""
    try:
        # التحقق من صحة المصادقة (مبسط)
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        # إحصائيات عامة
        total_items = Item.query.count()
        total_apps = Item.query.filter(Item.type == 'app').count()
        total_books = Item.query.filter(Item.type == 'book').count()
        total_downloads = db.session.query(func.sum(Item.download_count)).scalar() or 0
        
        # إحصائيات الإعلانات
        today = datetime.utcnow().date()
        today_ad_clicks = AdClick.query.filter(
            db.func.date(AdClick.clicked_at) == today,
            AdClick.revenue > 0
        ).count()
        
        today_ad_revenue = db.session.query(
            func.sum(AdClick.revenue)
        ).filter(
            db.func.date(AdClick.clicked_at) == today
        ).scalar() or 0.0
        
        # أحدث التحميلات
        recent_downloads = db.session.query(
            DownloadLog, Item
        ).join(Item).order_by(desc(DownloadLog.downloaded_at)).limit(10).all()
        
        # أكثر العناصر تحميلاً
        popular_items = Item.query.order_by(desc(Item.download_count)).limit(10).all()
        
        return jsonify({
            'success': True,
            'dashboard': {
                'stats': {
                    'total_items': total_items,
                    'total_apps': total_apps,
                    'total_books': total_books,
                    'total_downloads': total_downloads,
                    'today_ad_clicks': today_ad_clicks,
                    'today_ad_revenue': round(today_ad_revenue, 2)
                },
                'recent_downloads': [
                    {
                        'item_title': download.Item.title,
                        'item_type': download.Item.type,
                        'downloaded_at': download.DownloadLog.downloaded_at.strftime('%Y-%m-%d %H:%M'),
                        'ip_address': download.DownloadLog.ip_address
                    }
                    for download in recent_downloads
                ],
                'popular_items': [
                    {
                        'id': item.id,
                        'title': item.title,
                        'type': item.type,
                        'download_count': item.download_count,
                        'is_featured': item.is_featured
                    }
                    for item in popular_items
                ]
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/items', methods=['GET'])
def admin_get_items():
    """إدارة العناصر - عرض القائمة"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        item_type = request.args.get('type', 'all')
        
        query = Item.query
        if item_type != 'all':
            query = query.filter(Item.type == item_type)
        
        items = query.order_by(desc(Item.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'items': [
                {
                    'id': item.id,
                    'title': item.title,
                    'type': item.type,
                    'category': item.category,
                    'download_count': item.download_count,
                    'is_featured': item.is_featured,
                    'created_at': item.created_at.strftime('%Y-%m-%d %H:%M')
                }
                for item in items.items
            ],
            'pagination': {
                'page': page,
                'pages': items.pages,
                'total': items.total,
                'has_next': items.has_next,
                'has_prev': items.has_prev
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/items/<item_id>/toggle-featured', methods=['POST'])
def admin_toggle_featured(item_id):
    """تبديل حالة العنصر المميز"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        item = Item.query.get_or_404(item_id)
        item.is_featured = not item.is_featured
        item.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'تم {"إضافة" if item.is_featured else "إزالة"} العنصر {"إلى" if item.is_featured else "من"} المميزة',
            'is_featured': item.is_featured
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/items/<item_id>', methods=['DELETE'])
def admin_delete_item(item_id):
    """حذف عنصر"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        item = Item.query.get_or_404(item_id)
        
        # حذف السجلات المرتبطة
        DownloadLog.query.filter_by(item_id=item_id).delete()
        
        # حذف العنصر
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف العنصر بنجاح'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/upload', methods=['POST'])
def admin_upload_file():
    """رفع ملف جديد"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'لم يتم اختيار ملف'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'لم يتم اختيار ملف'}), 400
        
        # إنشاء مجلد الرفع إذا لم يكن موجوداً
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # حفظ الملف
        filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        # إرجاع رابط الملف
        file_url = f"/uploads/{filename}"
        
        return jsonify({
            'success': True,
            'message': 'تم رفع الملف بنجاح',
            'file_url': file_url
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/analytics', methods=['GET'])
def admin_analytics():
    """تحليلات مفصلة"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        # تحليلات التحميل الأسبوعية
        week_ago = datetime.utcnow() - timedelta(days=7)
        daily_downloads = db.session.query(
            func.date(DownloadLog.downloaded_at).label('date'),
            func.count(DownloadLog.id).label('downloads')
        ).filter(
            DownloadLog.downloaded_at >= week_ago
        ).group_by(
            func.date(DownloadLog.downloaded_at)
        ).all()
        
        # تحليلات الإعلانات الأسبوعية
        daily_ad_revenue = db.session.query(
            func.date(AdClick.clicked_at).label('date'),
            func.sum(AdClick.revenue).label('revenue'),
            func.count(AdClick.id).label('clicks')
        ).filter(
            AdClick.clicked_at >= week_ago,
            AdClick.revenue > 0
        ).group_by(
            func.date(AdClick.clicked_at)
        ).all()
        
        # أكثر الفئات تحميلاً
        category_stats = db.session.query(
            Item.category,
            func.sum(Item.download_count).label('total_downloads'),
            func.count(Item.id).label('item_count')
        ).group_by(Item.category).order_by(desc('total_downloads')).all()
        
        return jsonify({
            'success': True,
            'analytics': {
                'daily_downloads': [
                    {
                        'date': str(stat.date),
                        'downloads': stat.downloads
                    }
                    for stat in daily_downloads
                ],
                'daily_ad_revenue': [
                    {
                        'date': str(stat.date),
                        'revenue': float(stat.revenue or 0),
                        'clicks': stat.clicks
                    }
                    for stat in daily_ad_revenue
                ],
                'category_stats': [
                    {
                        'category': stat.category,
                        'total_downloads': stat.total_downloads or 0,
                        'item_count': stat.item_count
                    }
                    for stat in category_stats
                ]
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@admin_bp.route('/admin/backup', methods=['POST'])
def admin_backup_database():
    """نسخ احتياطي من قاعدة البيانات"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.endswith('admin_authenticated'):
            return jsonify({'success': False, 'message': 'غير مصرح'}), 401
        
        # إنشاء مجلد النسخ الاحتياطية
        backup_dir = os.path.join(os.path.dirname(__file__), '..', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # نسخ ملف قاعدة البيانات
        db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'app.db')
        backup_filename = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        import shutil
        shutil.copy2(db_path, backup_path)
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء النسخة الاحتياطية بنجاح',
            'backup_file': backup_filename
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
