# ✂️ حذف پس‌زمینه | BgRemover

ابزار هوشمند حذف پس‌زمینه تصاویر با استفاده از هوش مصنوعی — ساخته‌شده برای بازار ایران

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

---

## ✨ ویژگی‌ها

- حذف پس‌زمینه با هوش مصنوعی
- پشتیبانی از ۸+ مدل مختلف
- پردازش چندتایی (Batch)
- خروجی شفاف، سفید، یا رنگ دلخواه
- دانلود ZIP برای چند تصویر
- رابط کاربری فارسی

## 🚀 اجرای محلی

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy روی Streamlit Cloud

1. این ریپو را Fork کنید
2. به [share.streamlit.io](https://share.streamlit.io) بروید
3. ریپو را انتخاب کنید و `app.py` را به عنوان فایل اصلی تنظیم کنید
4. Deploy کنید!

## 🤖 مدل‌های پشتیبانی‌شده

| مدل | کاربرد |
|-----|--------|
| u2net | عمومی |
| u2netp | سبک و سریع |
| u2net_human_seg | انسان و پرتره |
| u2net_cloth_seg | لباس |
| birefnet-general | دقیق‌ترین - عمومی |
| birefnet-portrait | پرتره |
| isnet-anime | انیمه |

## 📄 لایسنس

MIT
