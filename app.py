import os
from flask import Flask, send_from_directory
from src.models.user import db
from src.routes.user import user_bp
from src.routes.items import items_bp
from src.routes.ads import ads_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# تسجيل البلوبرينتس
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(items_bp, url_prefix='/api')
app.register_blueprint(ads_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# إنشاء الجداول وإضافة البيانات الأولية
with app.app_context():
    db.create_all()
    
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
        {
            'id': 'app1', 'type': 'app', 'title': 'تعلم الإنجليزية', 'category': 'تعليمي',
            'size': '32 MB', 'version': '1.4.2', 'description': 'تطبيق تفاعلي لتعليم الإنجليزية مع ألعاب وتمارين صوتية.',
            'thumbnail': 'images/apps/app1.png', 'download_url': '#', 'is_featured': True
        },
        # يمكنك إضافة باقي العناصر هنا بنفس الطريقة...
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
