from flask import Blueprint, request, jsonify, render_template_string
from src.models.item import AdClick, db
from datetime import datetime, timedelta
import random

ads_bp = Blueprint('ads', __name__)

# قاعدة بيانات الإعلانات (يمكن نقلها لقاعدة البيانات لاحقاً)
ADS_DATABASE = {
    'banner_ads': [
        {
            'id': 'banner_1',
            'title': 'خدمات التصميم الاحترافي',
            'description': 'احصل على تصميمات احترافية لموقعك أو تطبيقك',
            'image': 'https://via.placeholder.com/728x90/4CAF50/white?text=خدمات+التصميم+الاحترافي',
            'url': '#',
            'cpc': 0.50,  # Cost Per Click
            'cpm': 2.00,  # Cost Per 1000 impressions
            'active': True,
            'position': 'header'
        },
        {
            'id': 'banner_2',
            'title': 'كورسات البرمجة المجانية',
            'description': 'تعلم البرمجة من الصفر مع أفضل الكورسات',
            'image': 'https://via.placeholder.com/728x90/2196F3/white?text=كورسات+البرمجة+المجانية',
            'url': '#',
            'cpc': 0.75,
            'cpm': 3.00,
            'active': True,
            'position': 'header'
        }
    ],
    'sidebar_ads': [
        {
            'id': 'sidebar_1',
            'title': 'استضافة مواقع موثوقة',
            'description': 'استضافة سريعة وآمنة لموقعك',
            'image': 'https://via.placeholder.com/300x250/FF9800/white?text=استضافة+مواقع',
            'url': '#',
            'cpc': 0.60,
            'cpm': 2.50,
            'active': True,
            'position': 'sidebar'
        },
        {
            'id': 'sidebar_2',
            'title': 'أدوات التسويق الرقمي',
            'description': 'زد من مبيعاتك مع أفضل الأدوات',
            'image': 'https://via.placeholder.com/300x250/9C27B0/white?text=التسويق+الرقمي',
            'url': '#',
            'cpc': 0.80,
            'cpm': 3.50,
            'active': True,
            'position': 'sidebar'
        }
    ],
    'native_ads': [
        {
            'id': 'native_1',
            'title': 'أفضل 10 تطبيقات للإنتاجية في 2025',
            'description': 'اكتشف التطبيقات التي ستغير طريقة عملك',
            'image': 'https://via.placeholder.com/400x200/607D8B/white?text=تطبيقات+الإنتاجية',
            'url': '#',
            'cpc': 1.00,
            'cpm': 4.00,
            'active': True,
            'position': 'content',
            'sponsored': True
        }
    ],
    'popup_ads': [
        {
            'id': 'popup_1',
            'title': 'عرض خاص - خصم 50%',
            'description': 'احصل على خصم 50% على جميع الخدمات',
            'image': 'https://via.placeholder.com/400x300/F44336/white?text=عرض+خاص+50%25',
            'url': '#',
            'cpc': 1.20,
            'cpm': 5.00,
            'active': True,
            'position': 'popup',
            'delay': 30  # ثانية قبل الظهور
        }
    ]
}

@ads_bp.route('/ads/<position>', methods=['GET'])
def get_ads(position):
    """الحصول على الإعلانات حسب الموضع"""
    try:
        ads = []
        
        if position == 'header' or position == 'banner':
            ads = [ad for ad in ADS_DATABASE['banner_ads'] if ad['active']]
        elif position == 'sidebar':
            ads = [ad for ad in ADS_DATABASE['sidebar_ads'] if ad['active']]
        elif position == 'native' or position == 'content':
            ads = [ad for ad in ADS_DATABASE['native_ads'] if ad['active']]
        elif position == 'popup':
            ads = [ad for ad in ADS_DATABASE['popup_ads'] if ad['active']]
        elif position == 'all':
            # جمع جميع الإعلانات النشطة
            for ad_type in ADS_DATABASE.values():
                ads.extend([ad for ad in ad_type if ad['active']])
        
        # اختيار إعلان عشوائي إذا كان هناك أكثر من واحد
        if ads:
            selected_ad = random.choice(ads)
            return jsonify({
                'success': True,
                'ad': selected_ad
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No active ads found for this position'
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ads_bp.route('/ads/click', methods=['POST'])
def track_ad_click():
    """تتبع النقرات على الإعلانات وحساب الأرباح"""
    try:
        data = request.get_json()
        ad_id = data.get('ad_id')
        position = data.get('position', 'unknown')
        page = data.get('page', 'unknown')
        
        # البحث عن الإعلان لحساب الربح
        revenue = 0.0
        ad_found = False
        
        for ad_type in ADS_DATABASE.values():
            for ad in ad_type:
                if ad['id'] == ad_id:
                    revenue = ad.get('cpc', 0.0)
                    ad_found = True
                    break
            if ad_found:
                break
        
        # تسجيل النقرة في قاعدة البيانات
        ad_click = AdClick(
            ad_position=position,
            page=page,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            revenue=revenue
        )
        
        db.session.add(ad_click)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ad click tracked successfully',
            'revenue': revenue
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@ads_bp.route('/ads/impression', methods=['POST'])
def track_ad_impression():
    """تتبع ظهور الإعلانات (للـ CPM)"""
    try:
        data = request.get_json()
        ad_id = data.get('ad_id')
        position = data.get('position', 'unknown')
        page = data.get('page', 'unknown')
        
        # يمكن إضافة جدول منفصل لتتبع الظهور
        # هنا نسجل كنقرة بقيمة 0 للتتبع
        impression_log = AdClick(
            ad_position=position,
            page=page,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            revenue=0.0  # لا يوجد ربح من الظهور فقط
        )
        
        db.session.add(impression_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Ad impression tracked successfully'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@ads_bp.route('/ads/stats', methods=['GET'])
def get_ad_stats():
    """إحصائيات الإعلانات والأرباح"""
    try:
        # إحصائيات اليوم
        today = datetime.utcnow().date()
        today_clicks = AdClick.query.filter(
            db.func.date(AdClick.clicked_at) == today,
            AdClick.revenue > 0
        ).count()
        
        today_revenue = db.session.query(
            db.func.sum(AdClick.revenue)
        ).filter(
            db.func.date(AdClick.clicked_at) == today
        ).scalar() or 0.0
        
        # إحصائيات الأسبوع
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_clicks = AdClick.query.filter(
            AdClick.clicked_at >= week_ago,
            AdClick.revenue > 0
        ).count()
        
        week_revenue = db.session.query(
            db.func.sum(AdClick.revenue)
        ).filter(
            AdClick.clicked_at >= week_ago
        ).scalar() or 0.0
        
        # إحصائيات الشهر
        month_ago = datetime.utcnow() - timedelta(days=30)
        month_clicks = AdClick.query.filter(
            AdClick.clicked_at >= month_ago,
            AdClick.revenue > 0
        ).count()
        
        month_revenue = db.session.query(
            db.func.sum(AdClick.revenue)
        ).filter(
            AdClick.clicked_at >= month_ago
        ).scalar() or 0.0
        
        # إحصائيات حسب الموضع
        position_stats = db.session.query(
            AdClick.ad_position,
            db.func.count(AdClick.id).label('clicks'),
            db.func.sum(AdClick.revenue).label('revenue')
        ).filter(
            AdClick.revenue > 0
        ).group_by(AdClick.ad_position).all()
        
        return jsonify({
            'success': True,
            'stats': {
                'today': {
                    'clicks': today_clicks,
                    'revenue': round(today_revenue, 2)
                },
                'week': {
                    'clicks': week_clicks,
                    'revenue': round(week_revenue, 2)
                },
                'month': {
                    'clicks': month_clicks,
                    'revenue': round(month_revenue, 2)
                },
                'by_position': [
                    {
                        'position': stat.ad_position,
                        'clicks': stat.clicks,
                        'revenue': round(stat.revenue or 0, 2)
                    }
                    for stat in position_stats
                ]
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ads_bp.route('/ads/adsense-code', methods=['GET'])
def get_adsense_code():
    """إرجاع كود Google AdSense للتضمين"""
    adsense_code = '''
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXX"
         crossorigin="anonymous"></script>
    
    <!-- إعلان البانر العلوي -->
    <ins class="adsbygoogle"
         style="display:block"
         data-ad-client="ca-pub-XXXXXXXXXX"
         data-ad-slot="XXXXXXXXXX"
         data-ad-format="auto"
         data-full-width-responsive="true"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
    '''
    
    return jsonify({
        'success': True,
        'adsense_code': adsense_code,
        'note': 'استبدل ca-pub-XXXXXXXXXX برقم الناشر الخاص بك من Google AdSense'
    })

@ads_bp.route('/ads/affiliate-links', methods=['GET'])
def get_affiliate_links():
    """روابط الأفلييت للمنتجات ذات الصلة"""
    affiliate_links = [
        {
            'title': 'كورس تطوير التطبيقات',
            'description': 'تعلم تطوير التطبيقات من الصفر',
            'price': '$49.99',
            'commission': '30%',
            'link': 'https://example.com/affiliate/course1?ref=emperor_store',
            'image': 'https://via.placeholder.com/200x150/4CAF50/white?text=كورس+التطبيقات'
        },
        {
            'title': 'استضافة مواقع احترافية',
            'description': 'استضافة سريعة وموثوقة',
            'price': '$9.99/شهر',
            'commission': '25%',
            'link': 'https://example.com/affiliate/hosting?ref=emperor_store',
            'image': 'https://via.placeholder.com/200x150/2196F3/white?text=استضافة+مواقع'
        }
    ]
    
    return jsonify({
        'success': True,
        'affiliate_links': affiliate_links
    })
