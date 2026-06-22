import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io
import zipfile

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="حذف پس‌زمینه | BgRemover",
    page_icon="✂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap');

* { font-family: 'Vazirmatn', sans-serif !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0f0f13;
    color: #e8e8f0;
    direction: rtl;
}

[data-testid="stHeader"] { background: transparent; }

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero p {
    color: #8888aa;
    font-size: 1.1rem;
}

/* Upload zone */
[data-testid="stFileUploader"] {
    background: #1a1a24;
    border: 2px dashed #2e2e45;
    border-radius: 16px;
    padding: 1.5rem;
    transition: border-color .2s;
}
[data-testid="stFileUploader"]:hover { border-color: #a78bfa; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb);
    color: white;
    border: none;
    border-radius: 10px;
    padding: .65rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    transition: opacity .2s, transform .1s;
    cursor: pointer;
}
.stButton > button:hover { opacity: .9; transform: translateY(-1px); }

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: #1a1a24 !important;
    border: 1.5px solid #a78bfa !important;
    color: #a78bfa !important;
    border-radius: 10px;
    width: 100%;
    font-weight: 600;
}

/* Cards */
.card {
    background: #1a1a24;
    border: 1px solid #2e2e45;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Stats bar */
.stat-bar {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1.5rem 0;
}
.stat {
    background: #1a1a24;
    border: 1px solid #2e2e45;
    border-radius: 12px;
    padding: .75rem 1.5rem;
    text-align: center;
}
.stat-num { font-size: 1.5rem; font-weight: 700; color: #a78bfa; }
.stat-lbl { font-size: .8rem; color: #666680; }

/* Model selector */
.stSelectbox > div > div {
    background: #1a1a24 !important;
    border-color: #2e2e45 !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
}

/* Color picker label */
label { color: #8888aa !important; font-size: .9rem; }

/* Image containers */
[data-testid="stImage"] img {
    border-radius: 12px;
    border: 1px solid #2e2e45;
}

/* Divider */
hr { border-color: #2e2e45; }

/* Section title */
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #8888aa;
    margin-bottom: .75rem;
    text-align: right;
}

/* Badge */
.badge {
    display: inline-block;
    background: #7c3aed22;
    color: #a78bfa;
    border: 1px solid #7c3aed44;
    border-radius: 20px;
    padding: .2rem .75rem;
    font-size: .8rem;
    margin-bottom: 1rem;
}

/* Success */
.success-box {
    background: #0d2b1e;
    border: 1px solid #166534;
    border-radius: 10px;
    padding: .75rem 1rem;
    color: #4ade80;
    text-align: center;
    font-size: .9rem;
}

/* Steps */
.steps {
    display: flex;
    gap: .75rem;
    justify-content: center;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.step {
    display: flex;
    align-items: center;
    gap: .4rem;
    color: #8888aa;
    font-size: .9rem;
}
.step-num {
    background: #7c3aed33;
    color: #a78bfa;
    border-radius: 50%;
    width: 24px; height: 24px;
    display: flex; align-items: center; justify-content: center;
    font-size: .75rem; font-weight: 700;
}
.step-arrow { color: #2e2e45; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">✂️ هوش مصنوعی</div>
    <h1>حذف پس‌زمینه</h1>
    <p>تصویرت رو آپلود کن — در چند ثانیه پس‌زمینه حذف می‌شه</p>
</div>
""", unsafe_allow_html=True)

# Steps
st.markdown("""
<div class="steps">
    <div class="step"><div class="step-num">۱</div> آپلود تصویر</div>
    <div class="step-arrow">←</div>
    <div class="step"><div class="step-num">۲</div> تنظیمات</div>
    <div class="step-arrow">←</div>
    <div class="step"><div class="step-num">۳</div> دریافت نتیجه</div>
</div>
""", unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stat-bar">
    <div class="stat"><div class="stat-num">۱۵+</div><div class="stat-lbl">مدل هوش مصنوعی</div></div>
    <div class="stat"><div class="stat-num">PNG</div><div class="stat-lbl">خروجی شفاف</div></div>
    <div class="stat"><div class="stat-num">۱۰۰٪</div><div class="stat-lbl">رایگان</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── Layout ────────────────────────────────────────────────────────────────────
col_upload, col_settings, col_result = st.columns([2, 1.2, 2], gap="large")

# ── Upload ────────────────────────────────────────────────────────────────────
with col_upload:
    st.markdown('<div class="section-title">📁 آپلود تصویر</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "تصویر یا تصاویر خود را انتخاب کنید",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help="فرمت‌های PNG، JPG و WebP پشتیبانی می‌شوند",
    )

    if uploaded_files:
        st.markdown(f'<div class="success-box">✅ {len(uploaded_files)} تصویر انتخاب شد</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        # Preview
        for f in uploaded_files[:3]:
            img = Image.open(f)
            st.image(img, caption=f.name, use_container_width=True)
        if len(uploaded_files) > 3:
            st.caption(f"و {len(uploaded_files)-3} تصویر دیگر...")

# ── Settings ──────────────────────────────────────────────────────────────────
with col_settings:
    st.markdown('<div class="section-title">⚙️ تنظیمات</div>', unsafe_allow_html=True)

    with st.container():
        model_options = {
            "عمومی (u2net)": "u2net",
            "سبک و سریع (u2netp)": "u2netp",
            "انسان و پرتره": "u2net_human_seg",
            "لباس": "u2net_cloth_seg",
            "BiRefNet (دقیق‌ترین)": "birefnet-general",
            "BiRefNet سبک": "birefnet-general-lite",
            "پرتره BiRefNet": "birefnet-portrait",
            "انیمه": "isnet-anime",
        }
        selected_model_label = st.selectbox(
            "مدل هوش مصنوعی",
            list(model_options.keys()),
            help="برای اکثر تصاویر، مدل عمومی یا BiRefNet توصیه می‌شود",
        )
        selected_model = model_options[selected_model_label]

        st.markdown("<br>", unsafe_allow_html=True)

        bg_option = st.radio(
            "پس‌زمینه خروجی",
            ["شفاف (PNG)", "سفید", "رنگ دلخواه"],
            index=0,
        )

        bg_color = None
        if bg_option == "رنگ دلخواه":
            bg_color = st.color_picker("انتخاب رنگ", "#ffffff")

        st.markdown("<br>", unsafe_allow_html=True)

        alpha_matting = st.toggle("Alpha Matting (لبه‌های نرم‌تر)", value=False,
                                   help="برای موهای ظریف و لبه‌های نامنظم مفیده")

        st.markdown("<br>", unsafe_allow_html=True)

        process_btn = st.button("✂️ حذف پس‌زمینه", type="primary", use_container_width=True)

# ── Result ────────────────────────────────────────────────────────────────────
with col_result:
    st.markdown('<div class="section-title">🖼️ نتیجه</div>', unsafe_allow_html=True)

    if process_btn and uploaded_files:
        session = new_session(selected_model)
        results = []
        progress = st.progress(0, text="در حال پردازش...")

        for i, uploaded_file in enumerate(uploaded_files):
            uploaded_file.seek(0)
            input_bytes = uploaded_file.read()

            try:
                output_bytes = remove(
                    input_bytes,
                    session=session,
                    alpha_matting=alpha_matting,
                )

                result_img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

                # Apply background
                if bg_option == "سفید":
                    bg = Image.new("RGBA", result_img.size, (255, 255, 255, 255))
                    bg.paste(result_img, mask=result_img.split()[3])
                    result_img = bg.convert("RGB")
                elif bg_option == "رنگ دلخواه" and bg_color:
                    r = int(bg_color[1:3], 16)
                    g = int(bg_color[3:5], 16)
                    b = int(bg_color[5:7], 16)
                    bg = Image.new("RGBA", result_img.size, (r, g, b, 255))
                    bg.paste(result_img, mask=result_img.split()[3])
                    result_img = bg.convert("RGB")

                # Save to bytes
                buf = io.BytesIO()
                fmt = "PNG" if bg_option == "شفاف (PNG)" else "JPEG"
                ext = "png" if bg_option == "شفاف (PNG)" else "jpg"
                result_img.save(buf, format=fmt, quality=95)
                buf.seek(0)

                results.append({
                    "name": uploaded_file.name.rsplit(".", 1)[0] + f"_nobg.{ext}",
                    "img": result_img,
                    "bytes": buf.getvalue(),
                    "ext": ext,
                })

            except Exception as e:
                st.error(f"خطا در پردازش {uploaded_file.name}: {e}")

            progress.progress((i + 1) / len(uploaded_files),
                              text=f"پردازش {i+1} از {len(uploaded_files)}...")

        progress.empty()

        if results:
            st.markdown(f'<div class="success-box">✅ {len(results)} تصویر با موفقیت پردازش شد</div>',
                        unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            for r in results:
                st.image(r["img"], caption=r["name"], use_container_width=True)
                st.download_button(
                    label=f"⬇️ دانلود {r['name']}",
                    data=r["bytes"],
                    file_name=r["name"],
                    mime=f"image/{'png' if r['ext']=='png' else 'jpeg'}",
                    use_container_width=True,
                )
                st.markdown("<br>", unsafe_allow_html=True)

            # Zip download for multiple
            if len(results) > 1:
                zip_buf = io.BytesIO()
                with zipfile.ZipFile(zip_buf, "w") as zf:
                    for r in results:
                        zf.writestr(r["name"], r["bytes"])
                zip_buf.seek(0)
                st.download_button(
                    label="📦 دانلود همه (ZIP)",
                    data=zip_buf.getvalue(),
                    file_name="nobg_results.zip",
                    mime="application/zip",
                    use_container_width=True,
                )

    elif process_btn and not uploaded_files:
        st.warning("ابتدا یک تصویر آپلود کنید.")
    else:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 3rem 1rem; color: #444466;">
            <div style="font-size:3rem">🖼️</div>
            <div style="margin-top:.5rem">نتیجه اینجا نمایش داده می‌شود</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#444466; font-size:.85rem; padding:1rem 0">
    ساخته‌شده با ❤️ در ایران &nbsp;|&nbsp; موتور: rembg &nbsp;|&nbsp; پشتیبانی: فارسی
</div>
""", unsafe_allow_html=True)
