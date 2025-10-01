from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Item(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.String(50), primary_key=True)
    type = db.Column(db.String(20), nullable=False)  # 'app' or 'book'
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(200), nullable=False)
    download_url = db.Column(db.String(500), nullable=False)
    download_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'category': self.category,
            'size': self.size,
            'version': self.version,
            'date': self.date_added.strftime('%Y-%m-%d'),
            'desc': self.description,
            'thumb': self.thumbnail,
            'downloads': [{'label': 'تحميل مباشر', 'url': self.download_url}],
            'download_count': self.download_count,
            'is_featured': self.is_featured
        }

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(20), nullable=False)  # 'app' or 'book'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        }

class DownloadLog(db.Model):
    __tablename__ = 'download_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.String(50), db.ForeignKey('items.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(500))
    downloaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    item = db.relationship('Item', backref=db.backref('download_logs', lazy=True))

class AdClick(db.Model):
    __tablename__ = 'ad_clicks'
    
    id = db.Column(db.Integer, primary_key=True)
    ad_position = db.Column(db.String(50), nullable=False)  # 'header', 'sidebar', 'footer', etc.
    page = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(500))
    clicked_at = db.Column(db.DateTime, default=datetime.utcnow)
    revenue = db.Column(db.Float, default=0.0)  # للتتبع المحتمل للإيرادات
