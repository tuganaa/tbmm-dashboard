"""
TBMM Yazili Soru Onergeleri - Streamlit Dashboard v2
=====================================================
Kurulum:
    pip install streamlit plotly pandas

Calistirma:
    streamlit run dashboard_onerge.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="TBMM Önerge Analizi",
    page_icon="🏛️",
    layout="wide"
)

# CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1B3A5C, #2d6a9f);
        border-radius: 12px;
        padding: 18px 22px;
        color: white;
        text-align: center;
    }
    .metric-card h2 { font-size: 2rem; margin: 0; }
    .metric-card p  { font-size: 0.9rem; margin: 0; opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ── Veri yükle ────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(__file__)
    mv  = pd.read_csv(os.path.join(base, "mv_analiz.csv"))
    il  = pd.read_csv(os.path.join(base, "il_analiz.csv"))
    yil = pd.read_csv(os.path.join(base, "yil_analiz.csv"))
    kel = pd.read_csv(os.path.join(base, "kelime_analiz.csv"))
    return mv, il, yil, kel

mv_pd, il_pd, yil_pd, kelime_pd = load_data()

# Türkiye il koordinatları
IL_KOORDINAT = {
    "ADANA": (37.00, 35.32), "ADIYAMAN": (37.76, 38.28), "AFYONKARAHİSAR": (38.75, 30.54),
    "AĞRI": (39.72, 43.05), "AKSARAY": (38.37, 34.03), "AMASYA": (40.65, 35.83),
    "ANKARA": (39.92, 32.85), "ANTALYA": (36.90, 30.70), "ARDAHAN": (41.11, 42.70),
    "ARTVİN": (41.18, 41.82), "AYDIN": (37.84, 27.84), "BALIKESİR": (39.65, 27.89),
    "BARTIN": (41.63, 32.34), "BATMAN": (37.88, 41.13), "BAYBURT": (40.26, 40.22),
    "BİLECİK": (40.14, 29.98), "BİNGÖL": (38.88, 40.50), "BİTLİS": (38.40, 42.12),
    "BOLU": (40.74, 31.61), "BURDUR": (37.72, 30.29), "BURSA": (40.18, 29.06),
    "ÇANAKKALE": (40.15, 26.41), "ÇANKIRI": (40.60, 33.62), "ÇORUM": (40.55, 34.96),
    "DENİZLİ": (37.77, 29.09), "DİYARBAKIR": (37.91, 40.23), "DÜZCE": (40.84, 31.16),
    "EDİRNE": (41.68, 26.56), "ELAZIĞ": (38.67, 39.22), "ERZİNCAN": (39.75, 39.49),
    "ERZURUM": (39.90, 41.27), "ESKİŞEHİR": (39.78, 30.52), "GAZİANTEP": (37.07, 37.38),
    "GİRESUN": (40.91, 38.39), "GÜMÜŞHANE": (40.46, 39.48), "HAKKARİ": (37.57, 43.74),
    "HATAY": (36.40, 36.35), "IĞDIR": (39.92, 44.05), "ISPARTA": (37.76, 30.56),
    "İSTANBUL": (41.01, 28.96), "İZMİR": (38.42, 27.14), "KAHRAMANMARAŞ": (37.57, 36.92),
    "KARABÜK": (41.20, 32.63), "KARAMAN": (37.18, 33.22), "KARS": (40.61, 43.10),
    "KASTAMONU": (41.38, 33.78), "KAYSERİ": (38.73, 35.49), "KIRIKKALE": (39.84, 33.51),
    "KIRKLARELİ": (41.73, 27.22), "KIRŞEHİR": (39.14, 34.16), "KİLİS": (36.72, 37.12),
    "KOCAELİ": (40.85, 29.88), "KONYA": (37.87, 32.49), "KÜTAHYA": (39.42, 29.98),
    "MALATYA": (38.35, 38.31), "MANİSA": (38.61, 27.43), "MARDİN": (37.31, 40.74),
    "MERSİN": (36.81, 34.64), "MUĞLA": (37.22, 28.36), "MUŞ": (38.73, 41.49),
    "NEVŞEHİR": (38.62, 34.71), "NİĞDE": (37.97, 34.68), "ORDU": (40.98, 37.88),
    "OSMANİYE": (37.07, 36.25), "RİZE": (41.02, 40.52), "SAKARYA": (40.69, 30.44),
    "SAMSUN": (41.29, 36.33), "ŞANLIURFA": (37.16, 38.80), "SİİRT": (37.93, 41.94),
    "SİNOP": (42.03, 35.15), "ŞIRNAK": (37.52, 42.46), "SİVAS": (39.75, 37.01),
    "TEKİRDAĞ": (41.00, 27.50), "TOKAT": (40.31, 36.55), "TRABZON": (41.00, 39.72),
    "TUNCELİ": (39.31, 39.44), "UŞAK": (38.68, 29.41), "VAN": (38.49, 43.38),
    "YALOVA": (40.65, 29.27), "YOZGAT": (39.82, 34.80), "ZONGULDAK": (41.46, 31.80),
}

# ── Başlık ────────────────────────────────────────────────────
st.title("🏛️ TBMM 28. Dönem Yazılı Soru Önergeleri Analizi")
st.caption("Kaynak: tbmm.gov.tr | BIG DATA 401 Final Projesi | 21.525 önerge")

# ── Metrik kartlar ────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class='metric-card'><h2>{mv_pd['count'].sum():,}</h2><p>Toplam Önerge</p></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='metric-card'><h2>{len(mv_pd):,}</h2><p>Aktif Milletvekili</p></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='metric-card'><h2>{len(il_pd):,}</h2><p>İl</p></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class='metric-card'><h2>{len(yil_pd):,}</h2><p>Yasama Yılı</p></div>""", unsafe_allow_html=True)

st.markdown("---")

# ── TABS ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Genel Analiz", "🗺️ Harita", "🔍 Arama", "📋 Veri Tablosu"])

# ── TAB 1: Genel Analiz ───────────────────────────────────────
with tab1:
    st.sidebar.title("🔍 Filtreler")
    top_n_mv  = st.sidebar.slider("Kaç milletvekili göster?", 5, 50, 15)
    top_n_il  = st.sidebar.slider("Kaç il göster?", 5, 50, 15)
    top_n_kel = st.sidebar.slider("Kaç kelime göster?", 10, 50, 20)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("En Çok Önerge Veren Milletvekilleri")
        fig_mv = px.bar(
            mv_pd.head(top_n_mv),
            x="count", y="onerge_sahibi",
            orientation="h",
            color="count",
            color_continuous_scale="Reds",
            labels={"count": "Önerge Sayısı", "onerge_sahibi": ""},
            text="count",
            hover_data=["il"]
        )
        fig_mv.update_traces(textposition="outside")
        fig_mv.update_layout(height=500, showlegend=False,
                             coloraxis_showscale=False,
                             yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_mv, use_container_width=True)

    with col2:
        st.subheader("İl Bazında Önerge Dağılımı")
        fig_il = px.bar(
            il_pd.head(top_n_il),
            x="count", y="il",
            orientation="h",
            color="count",
            color_continuous_scale="Blues",
            labels={"count": "Önerge Sayısı", "il": ""},
            text="count"
        )
        fig_il.update_traces(textposition="outside")
        fig_il.update_layout(height=500, showlegend=False,
                             coloraxis_showscale=False,
                             yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_il, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Yasama Yılına Göre Önerge Trendi")
        yil_pd["yil_kisa"] = yil_pd["yasama_yili_text"].str.extract(r"(28\.DÖNEM \d+\.Yasama|Son Dönem)")
        yil_pd["yil_kisa"] = yil_pd["yil_kisa"].fillna(yil_pd["yasama_yili_text"].str[:20])
        fig_yil = px.bar(
            yil_pd,
            x="yil_kisa", y="count",
            color="count",
            color_continuous_scale="Teal",
            labels={"count": "Önerge Sayısı", "yil_kisa": "Dönem"},
            text="count"
        )
        fig_yil.update_traces(textposition="outside")
        fig_yil.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_yil, use_container_width=True)

    with col4:
        st.subheader("En Sık Geçen Kelimeler")
        fig_kel = px.bar(
            kelime_pd.head(top_n_kel),
            x="count", y="kelime",
            orientation="h",
            color="count",
            color_continuous_scale="Oranges",
            labels={"count": "Frekans", "kelime": ""},
            text="count"
        )
        fig_kel.update_traces(textposition="outside")
        fig_kel.update_layout(height=400, showlegend=False,
                              coloraxis_showscale=False,
                              yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_kel, use_container_width=True)

    # Treemap
    st.subheader("İl Bazında Önerge Yoğunluğu (Treemap)")
    fig_tree = px.treemap(
        il_pd.head(30),
        path=["il"],
        values="count",
        color="count",
        color_continuous_scale="RdBu",
    )
    fig_tree.update_layout(height=400)
    st.plotly_chart(fig_tree, use_container_width=True)


# ── TAB 2: Harita ─────────────────────────────────────────────
with tab2:
    st.subheader("🗺️ Türkiye İl Bazında Önerge Haritası")

    st.markdown("---")
    st.subheader("İl Seç — Milletvekillerini Gör")
    secili_il = st.selectbox(
        "Bir il seç:", 
        [""] + sorted(il_map["il"].tolist()),
        key="harita_il"
    )
    if secili_il:
        mv_il = mv_pd[mv_pd["il"] == secili_il].sort_values("count", ascending=False)
        st.success(f"{secili_il} — {len(mv_il)} milletvekili, toplam {mv_il['count'].sum():,} önerge")
        st.dataframe(
            mv_il.rename(columns={"onerge_sahibi": "Milletvekili", 
                                   "il": "İl", "count": "Önerge Sayısı"}),
            use_container_width=True
        )

    # Koordinat eşleştir
    il_map = il_pd.copy()
    il_map["lat"] = il_map["il"].map(lambda x: IL_KOORDINAT.get(x, (None, None))[0])
    il_map["lon"] = il_map["il"].map(lambda x: IL_KOORDINAT.get(x, (None, None))[1])
    il_map = il_map.dropna(subset=["lat", "lon"])

    fig_map = px.scatter_geo(
        il_map,
        lat="lat",
        lon="lon",
        size="count",
        color="count",
        hover_name="il",
        hover_data={"count": True, "lat": False, "lon": False},
        color_continuous_scale="Reds",
        size_max=60,
        labels={"count": "Önerge Sayısı"},
        title="İl Bazında Yazılı Soru Önergesi Dağılımı"
    )
    fig_map.update_geos(
        scope="europe",
        center={"lat": 39, "lon": 35},
        projection_scale=4,
        showland=True,
        landcolor="lightgray",
        showocean=True,
        oceancolor="lightblue",
        showcountries=True,
        countrycolor="white",
    )
    fig_map.update_layout(height=600, coloraxis_colorbar_title="Önerge")
    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("İl Sıralaması")
    col_a, col_b = st.columns(2)
    with col_a:
        st.dataframe(
            il_map.head(20)[["il", "count"]].rename(
                columns={"il": "İl", "count": "Önerge Sayısı"}
            ).reset_index(drop=True),
            use_container_width=True,
            height=400
        )
    with col_b:
        fig_pie = px.pie(
            il_pd.head(10),
            names="il",
            values="count",
            title="Top 10 İl Dağılımı",
            hole=0.4
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)


# ── TAB 3: Arama ─────────────────────────────────────────────
with tab3:
    st.subheader("🔍 Milletvekili veya İl Arama")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        mv_arama = st.text_input("Milletvekili adı ara:", placeholder="örn. TANAL")
        if mv_arama:
            sonuc = mv_pd[mv_pd["onerge_sahibi"].str.contains(mv_arama.upper(), na=False)]
            if len(sonuc) > 0:
                st.success(f"{len(sonuc)} milletvekili bulundu")
                st.dataframe(
                    sonuc.rename(columns={"onerge_sahibi": "Milletvekili",
                                         "il": "İl", "count": "Önerge Sayısı"}),
                    use_container_width=True
                )
                fig_s = px.bar(
                    sonuc.head(10),
                    x="onerge_sahibi", y="count",
                    color="count",
                    color_continuous_scale="Reds",
                    labels={"onerge_sahibi": "Milletvekili", "count": "Önerge Sayısı"},
                    text="count"
                )
                fig_s.update_layout(showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_s, use_container_width=True)
            else:
                st.warning("Sonuç bulunamadı.")

    with col_s2:
        il_arama = st.text_input("İl ara:", placeholder="örn. İSTANBUL")
        if il_arama:
            sonuc_il = mv_pd[mv_pd["il"].str.contains(il_arama.upper(), na=False)]
            if len(sonuc_il) > 0:
                toplam = sonuc_il["count"].sum()
                st.success(f"{il_arama.upper()} — {len(sonuc_il)} milletvekili, toplam {toplam:,} önerge")
                st.dataframe(
                    sonuc_il.rename(columns={"onerge_sahibi": "Milletvekili",
                                             "il": "İl", "count": "Önerge Sayısı"})
                    .sort_values("Önerge Sayısı", ascending=False),
                    use_container_width=True
                )
            else:
                st.warning("Sonuç bulunamadı.")

    st.markdown("---")
    st.subheader("Kelime Arama")
    kel_arama = st.text_input("Kelime ara:", placeholder="örn. cezaevi")
    if kel_arama:
        sonuc_kel = kelime_pd[kelime_pd["kelime"].str.contains(kel_arama.lower(), na=False)]
        if len(sonuc_kel) > 0:
            st.dataframe(
                sonuc_kel.rename(columns={"kelime": "Kelime", "count": "Frekans"}),
                use_container_width=True
            )
        else:
            st.warning("Bu kelime bulunamadı.")


# ── TAB 4: Veri Tablosu ───────────────────────────────────────
with tab4:
    st.subheader("📋 Milletvekili Detay Tablosu")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        il_filtre = st.selectbox("İle göre filtrele:", ["Tümü"] + sorted(mv_pd["il"].dropna().unique().tolist()))
    with col_f2:
        min_onerge = st.slider("Minimum önerge sayısı:", 0, 500, 0)

    filtered = mv_pd.copy()
    if il_filtre != "Tümü":
        filtered = filtered[filtered["il"] == il_filtre]
    filtered = filtered[filtered["count"] >= min_onerge]
    filtered = filtered.sort_values("count", ascending=False).reset_index(drop=True)

    st.info(f"{len(filtered)} milletvekili gösteriliyor, toplam {filtered['count'].sum():,} önerge")

    st.dataframe(
        filtered.rename(columns={"onerge_sahibi": "Milletvekili",
                                  "il": "İl", "count": "Önerge Sayısı"}),
        use_container_width=True,
        height=500
    )

    # CSV indir
    csv = filtered.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        "⬇️ Filtrelenmiş veriyi indir (CSV)",
        data=csv,
        file_name="tbmm_mv_filtered.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("BIG DATA 401 Final Projesi | ODTÜ İstatistik Bölümü | 2024-2025")
