# app.py
import streamlit as st
import pandas as pd
from atlas_engine import generate_picks

st.set_page_config(
    page_title="Atlas Football",
    layout="wide"
)

st.title("⚽ Atlas Football — Panel Operativo")

st.markdown("Sistema de decisión probabilística (perfil balanceado)")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙️ Configuración")
bankroll = st.sidebar.number_input(
    "Banca actual",
    min_value=100.0,
    value=1000.0,
    step=100.0
)

if st.sidebar.button("▶️ Generar Picks"):
    picks = generate_picks(bankroll)

    if not picks:
        st.warning("No hay picks con edge suficiente hoy.")
    else:
        df = pd.DataFrame([p.__dict__ for p in picks])

        st.subheader("📊 Picks del día")
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Métricas")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Picks", len(df))
        col2.metric("Edge Promedio", f"{df.edge.mean():.2%}")
        col3.metric("Exposición Total", f"{df.stake.sum():.2f}")

else:
    st.info("Configura la banca y genera los picks.")
