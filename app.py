import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="أداة MCDA للري الذكي — مصر",
    page_icon="🌊",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    * { font-family: 'Cairo', sans-serif; }
    .main { direction: rtl; }
</style>
""", unsafe_allow_html=True)

GOVS = [
    {"rank":1,  "name":"البحيرة",       "nameEn":"El Beheira",      "m":[4.5,4.5,4.0,4.5,5.0,4.0], "system":"أراضي مستصلحة حديثة — شركات كبرى",         "status":"selected"},
    {"rank":2,  "name":"القليوبية",     "nameEn":"El Qalyoubeya",   "m":[3.5,5.0,2.0,5.0,5.0,5.0], "system":"دلتا قديمة — حيازات صغيرة مجزأة",           "status":"selected"},
    {"rank":3,  "name":"الإسكندرية",   "nameEn":"Alexandria",      "m":[4.5,3.5,3.5,4.0,5.0,3.0], "system":"أراضي ساحلية متوسطية مستصلحة",              "status":"selected"},
    {"rank":4,  "name":"الدقهلية",     "nameEn":"El Dakahlia",     "m":[4.5,3.0,2.5,4.5,4.0,4.5], "system":"منطقة ملوحة ذيل قناة دلتا وسطى",            "status":"selected"},
    {"rank":5,  "name":"سوهاج",        "nameEn":"Sohag",           "m":[3.5,2.5,4.5,3.5,4.5,4.5], "system":"وادي صعيد ضيق — إجهاد حراري عالٍ",           "status":"selected"},
    {"rank":6,  "name":"الوادي الجديد","nameEn":"El Wadi El Gedid","m":[3.0,4.0,5.0,2.5,4.0,1.0], "system":"استصلاح خزان جوفي أحفوري — شبه جاف",        "status":"boundary"},
    {"rank":7,  "name":"مطروح",        "nameEn":"Matrouh",         "m":[3.5,3.5,4.5,2.5,2.5,1.5], "system":"ساحل شمال غرب — بدو / أمطار",               "status":"other"},
    {"rank":8,  "name":"الشرقية",      "nameEn":"El Sharqia",      "m":[3.0,2.5,2.5,4.0,2.0,4.5], "system":"دلتا شرقية — صغار مزارعين",                 "status":"other"},
    {"rank":9,  "name":"جنوب سيناء",   "nameEn":"South Sinai",     "m":[3.0,3.5,5.0,2.0,2.5,1.0], "system":"سيناء جبلية / ساحلية",                      "status":"other"},
    {"rank":10, "name":"شمال سيناء",   "nameEn":"North Sinai",     "m":[3.5,3.0,4.0,2.5,2.0,2.0], "system":"سيناء — منطقة القناة",                      "status":"other"},
    {"rank":11, "name":"المنيا",       "nameEn":"El Minia",        "m":[2.5,1.5,4.0,3.5,2.5,4.0], "system":"صعيد أوسط",                                 "status":"other"},
    {"rank":12, "name":"الفيوم",       "nameEn":"El Fayoum",       "m":[3.0,1.5,3.0,3.5,2.5,3.5], "system":"منخفض الفيوم",                              "status":"other"},
    {"rank":12, "name":"أسيوط",        "nameEn":"Asyut",           "m":[2.5,1.5,4.0,3.5,2.0,4.0], "system":"صعيد أوسط — أسيوط",                        "status":"other"},
    {"rank":14, "name":"كفر الشيخ",    "nameEn":"Kafr El Sheikh",  "m":[3.0,2.0,2.5,3.5,2.0,4.0], "system":"دلتا شمالية ساحلية",                        "status":"other"},
    {"rank":15, "name":"قنا",          "nameEn":"Qena",            "m":[2.5,1.5,4.5,3.0,2.0,3.5], "system":"صعيد — منطقة الأقصر",                       "status":"other"},
    {"rank":16, "name":"أسوان",        "nameEn":"Aswan",           "m":[2.5,2.0,5.0,3.0,1.5,2.0], "system":"أقصى صعيد",                                 "status":"other"},
    {"rank":17, "name":"الغربية",      "nameEn":"El Gharbia",      "m":[2.5,2.0,2.0,4.0,1.5,4.5], "system":"دلتا وسطى — صغار مزارعين",                  "status":"other"},
    {"rank":18, "name":"الإسماعيلية",  "nameEn":"Ismailia",        "m":[2.5,2.5,3.0,3.5,2.0,2.0], "system":"استصلاح منطقة القناة",                      "status":"other"},
    {"rank":19, "name":"بني سويف",     "nameEn":"Beni Suef",       "m":[2.5,1.5,3.5,3.0,2.0,3.5], "system":"صعيد — منطقة انتقالية",                     "status":"other"},
    {"rank":20, "name":"المنوفية",     "nameEn":"El Menoufia",     "m":[2.5,1.5,2.0,4.0,1.5,4.5], "system":"دلتا وسطى",                                 "status":"other"},
    {"rank":21, "name":"الأقصر",       "nameEn":"Luxor",           "m":[2.0,1.5,4.5,3.0,1.5,2.5], "system":"سياحة / صعيد علوي",                         "status":"other"},
    {"rank":22, "name":"الجيزة",       "nameEn":"Giza",            "m":[2.0,1.5,2.5,4.0,1.5,3.5], "system":"حضري — أراضي قديمة",                        "status":"other"},
    {"rank":23, "name":"البحر الأحمر", "nameEn":"Red Sea",         "m":[2.0,3.0,4.5,2.0,1.5,1.0], "system":"صحراء ساحلية متفرقة",                       "status":"other"},
    {"rank":24, "name":"دمياط",        "nameEn":"Damietta",        "m":[2.5,2.0,2.0,3.0,1.5,3.0], "system":"دلتا شمالية ساحلية",                        "status":"other"},
    {"rank":25, "name":"السويس",       "nameEn":"Suez",            "m":[1.5,2.0,3.5,2.5,1.0,1.5], "system":"صناعي / ساحلي",                             "status":"other"},
    {"rank":26, "name":"القاهرة",      "nameEn":"Cairo",           "m":[1.5,1.0,2.0,4.0,1.0,2.0], "system":"حضري — زراعة محيطية",                       "status":"other"},
    {"rank":27, "name":"بورسعيد",      "nameEn":"Port Said",       "m":[1.5,1.5,2.0,2.5,1.0,1.5], "system":"حضري — منطقة القناة",                       "status":"other"},
]

WEIGHTS_BASE = [0.22, 0.18, 0.15, 0.17, 0.18, 0.10]
M_NAMES = ["M₁ تنوع هيدرولوجي", "M₂ هيكل حيازات", "M₃ إجهاد مناخي", "M₄ جاهزية مؤسسية", "M₅ تمثيل النظام", "M₆ كثافة مزارعين"]
M_FULL  = [
    "M₁ — تنوع المصدر المائي",
    "M₂ — هيكل حيازة الأراضي",
    "M₃ — الإجهاد المناخي",
    "M₄ — الجاهزية المؤسسية",
    "M₅ — تمثيلية النظام الزراعي",
    "M₆ — كثافة المزارعين",
]

STATUS_MAP = {g["name"]: g["status"] for g in GOVS}

def calc_wlc(m, w):
    return round(sum(wi * mi for wi, mi in zip(w, m)), 3)

def build_df(weights=None):
    w = weights if weights else WEIGHTS_BASE
    rows = []
    for g in GOVS:
        score = calc_wlc(g["m"], w)
        rows.append({
            "المحافظة": g["name"],
            "Governorate": g["nameEn"],
            "M₁": g["m"][0], "M₂": g["m"][1], "M₃": g["m"][2],
            "M₄": g["m"][3], "M₅": g["m"][4], "M₆": g["m"][5],
            "WLC Score": score,
            "النظام الزراعي": g["system"],
            "الحالة": "مختارة ✓" if g["status"]=="selected" else "حالة حدودية" if g["status"]=="boundary" else "أخرى",
        })
    df = pd.DataFrame(rows).sort_values("WLC Score", ascending=False).reset_index(drop=True)
    df.index += 1
    return df

# Header
st.markdown("# 🌊 أداة MCDA للري الذكي — مصر")
st.markdown("نموذج **Weighted Linear Combination** مطبق على 27 محافظة مصرية | Stage 1 Six-Criterion WLC")
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(["📊 نتائج WLC", "🔬 Sensitivity Analysis", "✏️ تعديل الدرجات", "📥 تحميل البيانات"])

# TAB 1
with tab1:
    df = build_df()

    st.markdown("### 🏆 المحافظات الخمس المختارة")
    top5 = df[df["الحالة"] == "مختارة ✓"].head(5)
    cols = st.columns(5)
    for i, (_, row) in enumerate(top5.iterrows()):
        with cols[i]:
            st.metric(label=row["المحافظة"], value=row["WLC Score"])
            st.caption(row["النظام الزراعي"])

    st.markdown("---")
    st.markdown("### 📋 جدول كل المحافظات")

    display_df = df[["المحافظة", "M₁","M₂","M₃","M₄","M₅","M₆", "WLC Score", "الحالة", "النظام الزراعي"]].copy()

    def highlight_status(val):
        if val == "مختارة ✓":
            return "background-color: #fff8e1; font-weight: bold"
        elif val == "حالة حدودية":
            return "background-color: #fff3e0"
        return ""

    st.dataframe(
        display_df.style.map(highlight_status, subset=["الحالة"]),
        use_container_width=True,
        height=600
    )

    st.markdown("### 📊 مقارنة بصرية — أعلى 10 محافظات")
    fig = px.bar(
        df.head(10),
        x="WLC Score", y="المحافظة",
        orientation="h",
        color="الحالة",
        color_discrete_map={"مختارة ✓": "#c8a96e", "حالة حدودية": "#e65100", "أخرى": "#90a4ae"},
        text="WLC Score"
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# TAB 2
with tab2:
    st.markdown("### 🔬 اختبار الحساسية — غيّر الأوزان وشوف التأثير")
    st.info("غيّر أوزان المعايير — مجموعها لازم يساوي 1.00 بالظبط")

    cols2 = st.columns(3)
    new_weights = []
    for i, name in enumerate(M_NAMES):
        with cols2[i % 3]:
            w = st.slider(name, min_value=0.01, max_value=0.50,
                          value=WEIGHTS_BASE[i], step=0.01, key=f"w{i}")
            new_weights.append(w)

    total = round(sum(new_weights), 3)
    if abs(total - 1.0) > 0.005:
        st.error(f"⚠️ مجموع الأوزان = {total} — لازم يبقى 1.00 بالظبط")
    else:
        st.success(f"✓ مجموع الأوزان = {total}")
        df_new = build_df(new_weights)
        df_base = build_df()

        merged = df_new[["المحافظة","WLC Score","الحالة"]].copy()
        merged.columns = ["المحافظة","Score الجديد","الحالة"]
        base_scores = df_base.set_index("المحافظة")["WLC Score"]
        merged["Score الأصلي"] = merged["المحافظة"].map(base_scores)
        merged["Δ التغيير"] = (merged["Score الجديد"] - merged["Score الأصلي"]).round(3)
        merged = merged.sort_values("Score الجديد", ascending=False).reset_index(drop=True)
        merged.index += 1

        st.dataframe(
            merged[["المحافظة","Score الأصلي","Score الجديد","Δ التغيير","الحالة"]],
            use_container_width=True,
            height=500
        )

        fig2 = go.Figure()
        top10 = merged.head(10)
        fig2.add_trace(go.Bar(name="Score أصلي", x=top10["المحافظة"], y=top10["Score الأصلي"], marker_color="#90a4ae"))
        fig2.add_trace(go.Bar(name="Score جديد", x=top10["المحافظة"], y=top10["Score الجديد"], marker_color="#c8a96e"))
        fig2.update_layout(barmode="group", title="مقارنة: Score الأصلي vs الجديد", height=380)
        st.plotly_chart(fig2, use_container_width=True)

# TAB 3
with tab3:
    st.markdown("### ✏️ تعديل درجات أي محافظة")
    st.info("اختاري المحافظة وعدّلي درجاتها — الـ WLC Score بيتحدث فوراً")

    gov_names = [g["name"] for g in GOVS]
    selected_gov = st.selectbox("اختاري المحافظة", gov_names)
    gov_idx = gov_names.index(selected_gov)
    gov_data = GOVS[gov_idx]

    st.markdown(f"**{gov_data['name']}** — {gov_data['system']}")
    st.markdown("---")

    new_scores = []
    cols3 = st.columns(3)
    for i, full_name in enumerate(M_FULL):
        with cols3[i % 3]:
            score = st.slider(full_name, min_value=1.0, max_value=5.0,
                              value=float(gov_data["m"][i]), step=0.5, key=f"s{i}")
            new_scores.append(score)

    new_wlc = calc_wlc(new_scores, WEIGHTS_BASE)
    original_wlc = calc_wlc(gov_data["m"], WEIGHTS_BASE)
    delta = round(new_wlc - original_wlc, 3)

    c1, c2, c3 = st.columns(3)
    c1.metric("WLC Score الأصلي", original_wlc)
    c2.metric("WLC Score الجديد", new_wlc, delta=delta)
    c3.metric("التغيير", f"{'+' if delta>=0 else ''}{delta}")

# TAB 4
with tab4:
    st.markdown("### 📥 تحميل النتائج")
    df_dl = build_df()

    st.dataframe(
        df_dl[["المحافظة","Governorate","M₁","M₂","M₃","M₄","M₅","M₆","WLC Score","الحالة","النظام الزراعي"]],
        use_container_width=True
    )

    csv = df_dl.to_csv(index=True, encoding="utf-8-sig")
    st.download_button(
        label="⬇️ تحميل CSV",
        data=csv,
        file_name="egypt_irrigation_mcda.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.markdown("### 📐 صيغة الـ WLC")
    st.latex(r"S = (0.22 \times M_1) + (0.18 \times M_2) + (0.15 \times M_3) + (0.17 \times M_4) + (0.18 \times M_5) + (0.10 \times M_6)")

    weights_df = pd.DataFrame({
        "المعيار": M_FULL,
        "الوزن": WEIGHTS_BASE,
        "النسبة": [f"{w*100:.0f}%" for w in WEIGHTS_BASE]
    })
    st.dataframe(weights_df, use_container_width=True, hide_index=True)

st.divider()
st.caption("أداة MCDA للري الذكي في مصر · Stage 1 WLC Model · البيانات من MALR 2017 و WMRI 2018")
