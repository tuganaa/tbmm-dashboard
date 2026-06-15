"""
TBMM Yazili Soru Onergeleri - Streamlit Dashboard
===================================================
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

st.title("🏛️ TBMM 28. Dönem Yazılı Soru Önergeleri Analizi")
st.caption("Kaynak: tbmm.gov.tr | BIG DATA 401 Final Projesi")

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

# ── Metrik kartlar ────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("Toplam Önerge", f"{mv_pd['count'].sum():,}")
c2.metric("Aktif Milletvekili", f"{len(mv_pd):,}")
c3.metric("İl", f"{len(il_pd):,}")
c4.metric("Yasama Yılı", f"{len(yil_pd):,}")

st.markdown("---")

# ── Sidebar filtreler ─────────────────────────────────────────
st.sidebar.title("🔍 Filtreler")
top_n_mv = st.sidebar.slider("Kaç milletvekili göster?", 5, 50, 15)
top_n_il = st.sidebar.slider("Kaç il göster?", 5, 50, 15)
top_n_kel = st.sidebar.slider("Kaç kelime göster?", 10, 50, 20)

# ── Grafik 1 & 2 ──────────────────────────────────────────────
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
        text="count"
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

# ── Grafik 3 & 4 ──────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Yasama Yılına Göre Önerge Trendi")
    # Yasama yili metnini kisalt
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
    fig_yil.update_layout(height=400, showlegend=False,
                          coloraxis_showscale=False)
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

# ── Treemap: İl dağılımı ──────────────────────────────────────
st.subheader("🗺️ İl Bazında Önerge Haritası")
fig_tree = px.treemap(
    il_pd.head(30),
    path=["il"],
    values="count",
    color="count",
    color_continuous_scale="RdBu",
    title="İllere Göre Önerge Yoğunluğu (Top 30)"
)
fig_tree.update_layout(height=400)
st.plotly_chart(fig_tree, use_container_width=True)

# ── Veri tablosu ──────────────────────────────────────────────
st.subheader("📋 Milletvekili Detay Tablosu")
st.dataframe(
    mv_pd.rename(columns={"onerge_sahibi": "Milletvekili", 
                           "il": "İl", "count": "Önerge Sayısı"}),
    use_container_width=True,
    height=400
)

st.markdown("---")
st.caption("BIG DATA 401 Final Projesi | ODTÜ | 2025-2026")
