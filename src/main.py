import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp
from src.routes.items import items_bp
from src.routes.ads import ads_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# تسجيل البلوبرينتس
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(items_bp, url_prefix='/api')
app.register_blueprint(ads_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# إنشاء الجداول وإضافة البيانات الأولية
with app.app_context():
    db.create_all()
    
    # إضافة البيانات الأولية إذا لم تكن موجودة
    from src.models.item import Item, Category
    
    # إضافة الفئات الأساسية
    categories_data = [
        {'name': 'تعليمي', 'type': 'app'},
        {'name': 'أدوات', 'type': 'app'},
        {'name': 'إنتاجية', 'type': 'app'},
        {'name': 'ترفيه', 'type': 'app'},
        {'name': 'برمجة', 'type': 'book'},
        {'name': 'تصميم', 'type': 'book'},
        {'name': 'تنمية بشرية', 'type': 'book'},
        {'name': 'شبكات', 'type': 'book'},
        {'name': 'ذكاء اصطناعي', 'type': 'book'},
        {'name': 'روايات', 'type': 'book'}
    ]
    
    for cat_data in categories_data:
        if not Category.query.filter_by(name=cat_data['name'], type=cat_data['type']).first():
            category = Category(**cat_data)
            db.session.add(category)
    
    # إضافة العناصر الأولية
    items_data = [
        # التطبيقات
        {
            'id': 'app1', 'type': 'app', 'title': 'تعلم الإنجليزية', 'category': 'تعليمي',
            'size': '32 MB', 'version': '1.4.2', 'description': 'تطبيق تفاعلي لتعليم الإنجليزية مع ألعاب وتمارين صوتية.',
            'thumbnail': 'images/apps/app1.png', 'download_url': '#', 'is_featured': True
        },
        {
            'id': 'app2', 'type': 'app', 'title': 'منظف الجهاز', 'category': 'أدوات',
            'size': '18 MB', 'version': '2.0.1', 'description': 'تنظيف الملفات المؤقتة وتسريع الهاتف بضغطة.',
            'thumbnail': 'images/apps/app2.png', 'download_url': '#', 'is_featured': False
        },
        {
            'id': 'app3', 'type': 'app', 'title': 'قاموس عربي-إنجليزي', 'category': 'تعليمي',
            'size': '25 MB', 'version': '3.1.0', 'description': 'قاموس شامل يعمل بدون إنترنت.',
            'thumbnail': 'images/apps/app3.png', 'download_url': '#', 'is_featured': True
        },
        {
            'id': 'app4', 'type': 'app', 'title': 'مراقب الصحة', 'category': 'إنتاجية',
            'size': '28 MB', 'version': '1.2.5', 'description': 'مراقبة النشاط والتمارين وحساب السعرات.',
            'thumbnail': 'images/apps/app4.png', 'download_url': '#', 'is_featured': False
        },
        {
            'id': 'app5', 'type': 'app', 'title': 'مترجم فوري', 'category': 'أدوات',
            'size': '22 MB', 'version': '4.0.0', 'description': 'ترجمة نصوص ومحادثات فورية بدعم صوتي.',
            'thumbnail': 'images/apps/app5.png', 'download_url': '#', 'is_featured': True
        },
        # الكتب
        {
            'id': 'book1', 'type': 'book', 'title': 'مدخل إلى بايثون', 'category': 'برمجة',
            'size': '7.2 MB', 'version': 'PDF', 'description': 'كتاب مبسط للمبتدئين في بايثون مع أمثلة عملية.',
            'thumbnail': 'images/books/book1.png', 'download_url': '#', 'is_featured': True
        },
        {
            'id': 'book2', 'type': 'book', 'title': 'تصميم واجهات المستخدم', 'category': 'تصميم',
            'size': '5.8 MB', 'version': 'PDF', 'description': 'مبادئ تصميم واجهات حديثة وتجربة المستخدم.',
            'thumbnail': 'images/books/book2.png', 'download_url': '#', 'is_featured': False
        },
        {
            'id': 'book3', 'type': 'book', 'title': 'أساسيات قواعد البيانات', 'category': 'برمجة',
            'size': '6.9 MB', 'version': 'PDF', 'description': 'مدخل لقواعد البيانات SQL وتصميم ERD.',
            'thumbnail': 'images/books/book3.png', 'download_url': '#', 'is_featured': True
        }
    ]
    
    for item_data in items_data:
        if not Item.query.get(item_data['id']):
            item = Item(**item_data)
            db.session.add(item)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing data: {e}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
