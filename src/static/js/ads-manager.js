// ========== مدير الإعلانات المتجاوب ==========

class AdsManager {
    constructor() {
        this.adsLoaded = false;
        this.adPositions = {
            header: null,
            sidebar: null,
            content: null,
            footer: null
        };
        this.init();
    }

    init() {
        this.detectDevice();
        this.loadAds();
        this.setupAdTracking();
        this.setupResponsiveAds();
    }

    detectDevice() {
        this.isMobile = window.innerWidth <= 768;
        this.isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
        this.isDesktop = window.innerWidth > 1024;
    }

    async loadAds() {
        try {
            // تحميل إعلانات مختلفة حسب نوع الجهاز
            const positions = this.getAdPositionsForDevice();
            
            for (const position of positions) {
                await this.loadAdForPosition(position);
            }
            
            this.adsLoaded = true;
            console.log('تم تحميل الإعلانات بنجاح');
        } catch (error) {
            console.error('خطأ في تحميل الإعلانات:', error);
        }
    }

    getAdPositionsForDevice() {
        if (this.isMobile) {
            return ['header', 'content']; // إعلانات أقل على الجوال
        } else if (this.isTablet) {
            return ['header', 'content', 'sidebar'];
        } else {
            return ['header', 'sidebar', 'content', 'footer'];
        }
    }

    async loadAdForPosition(position) {
        try {
            const response = await fetch(`/api/ads/${position}`);
            const data = await response.json();
            
            if (data.success && data.ad) {
                this.displayAd(data.ad, position);
                this.trackAdImpression(data.ad.id, position);
            }
        } catch (error) {
            console.error(`خطأ في تحميل إعلان ${position}:`, error);
        }
    }

    displayAd(ad, position) {
        const container = document.getElementById(`ad-${position}`);
        if (!container) return;

        const adElement = this.createAdElement(ad, position);
        container.innerHTML = '';
        container.appendChild(adElement);
        
        this.adPositions[position] = ad;
    }

    createAdElement(ad, position) {
        const adDiv = document.createElement('div');
        adDiv.className = `ad-container ad-${position}`;
        adDiv.setAttribute('data-ad-id', ad.id);
        
        // تحديد حجم الإعلان حسب الجهاز والموضع
        const adSize = this.getAdSize(position);
        
        if (ad.sponsored) {
            adDiv.innerHTML = `
                <div class="ad-native" style="max-width: ${adSize.width}px;">
                    <div class="ad-label">إعلان</div>
                    <div class="ad-content">
                        <img src="${ad.image}" alt="${ad.title}" class="ad-image" 
                             style="width: 100%; height: ${adSize.height}px; object-fit: cover; border-radius: 8px;">
                        <div class="ad-text">
                            <h3 class="ad-title">${ad.title}</h3>
                            <p class="ad-description">${ad.description}</p>
                        </div>
                    </div>
                </div>
            `;
        } else {
            adDiv.innerHTML = `
                <div class="ad-banner" style="max-width: ${adSize.width}px; height: ${adSize.height}px;">
                    <img src="${ad.image}" alt="${ad.title}" 
                         style="width: 100%; height: 100%; object-fit: cover; border-radius: 8px;">
                </div>
            `;
        }

        // إضافة مستمع النقر
        adDiv.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleAdClick(ad, position);
        });

        return adDiv;
    }

    getAdSize(position) {
        const sizes = {
            mobile: {
                header: { width: 320, height: 50 },
                sidebar: { width: 300, height: 250 },
                content: { width: 320, height: 100 },
                footer: { width: 320, height: 50 }
            },
            tablet: {
                header: { width: 728, height: 90 },
                sidebar: { width: 300, height: 250 },
                content: { width: 468, height: 60 },
                footer: { width: 728, height: 90 }
            },
            desktop: {
                header: { width: 728, height: 90 },
                sidebar: { width: 300, height: 250 },
                content: { width: 728, height: 90 },
                footer: { width: 728, height: 90 }
            }
        };

        let deviceType = 'desktop';
        if (this.isMobile) deviceType = 'mobile';
        else if (this.isTablet) deviceType = 'tablet';

        return sizes[deviceType][position] || { width: 300, height: 250 };
    }

    async handleAdClick(ad, position) {
        try {
            // تتبع النقرة
            await this.trackAdClick(ad.id, position);
            
            // فتح الرابط
            if (ad.url && ad.url !== '#') {
                window.open(ad.url, '_blank');
            }
        } catch (error) {
            console.error('خطأ في معالجة نقرة الإعلان:', error);
        }
    }

    async trackAdClick(adId, position) {
        try {
            await fetch('/api/ads/click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ad_id: adId,
                    position: position,
                    page: window.location.pathname
                })
            });
        } catch (error) {
            console.error('خطأ في تتبع النقرة:', error);
        }
    }

    async trackAdImpression(adId, position) {
        try {
            await fetch('/api/ads/impression', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    ad_id: adId,
                    position: position,
                    page: window.location.pathname
                })
            });
        } catch (error) {
            console.error('خطأ في تتبع الظهور:', error);
        }
    }

    setupAdTracking() {
        // تتبع الوقت المقضي في الصفحة
        this.pageStartTime = Date.now();
        
        window.addEventListener('beforeunload', () => {
            const timeSpent = Date.now() - this.pageStartTime;
            // يمكن إرسال هذه البيانات للتحليل
            console.log(`وقت قضاه المستخدم في الصفحة: ${timeSpent}ms`);
        });
    }

    setupResponsiveAds() {
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                this.detectDevice();
                this.refreshAds();
            }, 250);
        });
    }

    refreshAds() {
        // إعادة تحميل الإعلانات عند تغيير حجم الشاشة
        const newPositions = this.getAdPositionsForDevice();
        
        // إخفاء الإعلانات غير المناسبة للجهاز الحالي
        Object.keys(this.adPositions).forEach(position => {
            const container = document.getElementById(`ad-${position}`);
            if (container) {
                if (newPositions.includes(position)) {
                    container.style.display = 'block';
                } else {
                    container.style.display = 'none';
                }
            }
        });
    }

    // إعلانات Google AdSense
    loadGoogleAdSense() {
        if (window.adsbygoogle) return; // تجنب التحميل المتكرر

        const script = document.createElement('script');
        script.async = true;
        script.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXX';
        script.crossOrigin = 'anonymous';
        document.head.appendChild(script);

        script.onload = () => {
            console.log('تم تحميل Google AdSense');
            this.initializeAdSenseAds();
        };
    }

    initializeAdSenseAds() {
        // تهيئة إعلانات AdSense
        const adSenseContainers = document.querySelectorAll('.adsbygoogle');
        adSenseContainers.forEach(container => {
            try {
                (window.adsbygoogle = window.adsbygoogle || []).push({});
            } catch (error) {
                console.error('خطأ في تهيئة إعلان AdSense:', error);
            }
        });
    }

    // إعلانات الأفلييت
    async loadAffiliateLinks() {
        try {
            const response = await fetch('/api/ads/affiliate-links');
            const data = await response.json();
            
            if (data.success) {
                this.displayAffiliateLinks(data.affiliate_links);
            }
        } catch (error) {
            console.error('خطأ في تحميل روابط الأفلييت:', error);
        }
    }

    displayAffiliateLinks(links) {
        const container = document.getElementById('affiliate-links');
        if (!container) return;

        const linksHTML = links.map(link => `
            <div class="affiliate-link" onclick="window.open('${link.link}', '_blank')">
                <img src="${link.image}" alt="${link.title}" class="affiliate-image">
                <div class="affiliate-content">
                    <h4>${link.title}</h4>
                    <p>${link.description}</p>
                    <div class="affiliate-price">${link.price}</div>
                    <div class="affiliate-commission">عمولة: ${link.commission}</div>
                </div>
            </div>
        `).join('');

        container.innerHTML = `
            <div class="affiliate-container">
                <h3>منتجات مقترحة</h3>
                <div class="affiliate-grid">
                    ${linksHTML}
                </div>
            </div>
        `;
    }

    // إحصائيات الإعلانات
    async getAdStats() {
        try {
            const response = await fetch('/api/ads/stats');
            const data = await response.json();
            
            if (data.success) {
                console.log('إحصائيات الإعلانات:', data.stats);
                return data.stats;
            }
        } catch (error) {
            console.error('خطأ في جلب إحصائيات الإعلانات:', error);
        }
    }
}

// تهيئة مدير الإعلانات عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    window.adsManager = new AdsManager();
    
    // تحميل Google AdSense إذا كان متاحاً
    // window.adsManager.loadGoogleAdSense();
    
    // تحميل روابط الأفلييت
    window.adsManager.loadAffiliateLinks();
});

// إضافة CSS للإعلانات
const adStyles = `
<style>
.ad-container {
    margin: 16px auto;
    text-align: center;
    position: relative;
}

.ad-native {
    background: var(--panel);
    border: 1px solid var(--muted);
    border-radius: 8px;
    padding: 12px;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
}

.ad-native:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.ad-label {
    position: absolute;
    top: 4px;
    right: 8px;
    font-size: 10px;
    color: var(--muted-text);
    background: var(--muted);
    padding: 2px 6px;
    border-radius: 4px;
}

.ad-content {
    display: flex;
    gap: 12px;
    align-items: center;
}

.ad-image {
    flex-shrink: 0;
}

.ad-text {
    flex: 1;
    text-align: right;
}

.ad-title {
    margin: 0 0 8px 0;
    font-size: 16px;
    color: var(--text);
}

.ad-description {
    margin: 0;
    font-size: 14px;
    color: var(--muted-text);
    line-height: 1.4;
}

.ad-banner {
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 8px;
    overflow: hidden;
}

.ad-banner:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.affiliate-container {
    margin: 24px 0;
    padding: 16px;
    background: var(--panel);
    border-radius: 12px;
    border: 1px solid var(--muted);
}

.affiliate-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin-top: 16px;
}

.affiliate-link {
    background: var(--bg);
    border: 1px solid var(--muted);
    border-radius: 8px;
    padding: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.affiliate-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-color: var(--accent);
}

.affiliate-image {
    width: 100%;
    height: 120px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 8px;
}

.affiliate-content h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    color: var(--text);
}

.affiliate-content p {
    margin: 0 0 8px 0;
    font-size: 12px;
    color: var(--muted-text);
    line-height: 1.3;
}

.affiliate-price {
    font-weight: bold;
    color: var(--accent);
    font-size: 14px;
}

.affiliate-commission {
    font-size: 11px;
    color: var(--muted-text);
    margin-top: 4px;
}

/* تحسينات للجوال */
@media (max-width: 768px) {
    .ad-content {
        flex-direction: column;
        text-align: center;
    }
    
    .ad-text {
        text-align: center;
    }
    
    .affiliate-grid {
        grid-template-columns: 1fr;
    }
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', adStyles);
