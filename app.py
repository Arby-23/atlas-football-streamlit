# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pipeline import get_daily_picks

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Atlas Football",
    layout="wide"
)

st.title("⚽ Atlas Football — Panel Operativo")
st.markdown("Sistema de decisión probabilística · Perfil balanceado")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Configuración")

bankroll = st.sidebar.number_input(
    "Banca actual",
    min_value=100.0,
    value=1000.0,
    step=100.0
)

leagues_allowed = st.sidebar.multiselect(
    "Ligas activas",
    [
        "Premier League",
        "La Liga",
        "Serie A",
        "Bundesliga",
        "Ligue 1"
    ],
    default=["Premier League", "La Liga", "Serie A"]
)

run = st.sidebar.button("▶️ Generar Picks")

# -----------------------------
# EJECUCIÓN
# -----------------------------
if run:
    picks = get_daily_picks(bankroll)

    # Filtro por ligas
    picks = [p for p in picks if p.league in leagues_allowed]

    if not picks:
        st.warning("No hay picks con edge suficiente hoy.")
    else:
        df = pd.DataFrame([p.__dict__ for p in picks])

        st.subheader("📊 Picks del día")
        st.dataframe(df, use_container_width=True)

        # -----------------------------
        # MÉTRICAS
        # -----------------------------
        st.subheader("📈 Métricas")
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Picks", len(df))
        col2.metric("Edge Promedio", f"{df.edge.mean():.2%}")
        col3.metric("Exposición Total", f"{df.stake.sum():.2f}")

        # -----------------------------
        # GRÁFICA BANCA
        # -----------------------------
        st.subheader("📉 Evolución simulada de banca")

        bankroll_series = [bankroll]
        for _, row in df.iterrows():
            bankroll_series.append(
                bankroll_series[-1] + row.stake * row.edge
            )

        fig, ax = plt.subplots()
        ax.plot(bankroll_series)
        ax.set_xlabel("Picks")
        ax.set_ylabel("Banca")
        st.pyplot(fig)

else:
    st.info("Configura la banca, elige ligas y genera los picks.")
