# pipeline.py
from dataclasses import dataclass
from typing import List, Dict
import datetime as dt
import math
import random

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
EDGE_MIN = 0.05
EDGE_AGRESIVO = 0.07
KELLY_FRAC = 0.25
STAKE_CAP_PICK = 0.01

# -----------------------------
# ESTRUCTURAS
# -----------------------------
@dataclass
class Match:
    match_id: str
    league: str
    home: str
    away: str
    odds: Dict[str, float]
    features: Dict[str, float]

@dataclass
class Pick:
    match: str
    league: str
    market: str
    prob: float
    odds: float
    edge: float
    stake: float
    signal: str

# -----------------------------
# MODELO (MVP REALISTA)
# -----------------------------
def model_probabilities(match: Match) -> Dict[str, float]:
    return {
        "U2.5": round(random.uniform(0.52, 0.60), 2),
        "D": round(random.uniform(0.25, 0.32), 2),
        "BTTS_NO": round(random.uniform(0.54, 0.62), 2)
    }

def compute_edge(prob: float, odds: float) -> float:
    return prob * odds - 1

def kelly_stake(prob: float, odds: float, bankroll: float) -> float:
    b = odds - 1
    q = 1 - prob
    k = max((b * prob - q) / b, 0)
    k *= KELLY_FRAC
    return min(bankroll * k, bankroll * STAKE_CAP_PICK)

# -----------------------------
# PIPELINE PRINCIPAL
# -----------------------------
def run_pipeline(bankroll: float) -> List[Pick]:

    # Simulación de partidos reales (placeholder)
    matches = [
        Match("1", "Premier League", "Man City", "Chelsea", {"U2.5": 1.95}, {}),
        Match("2", "La Liga", "Real Madrid", "Sevilla", {"U2.5": 1.85}, {}),
        Match("3", "Serie A", "Inter", "Milan", {"U2.5": 1.90}, {}),
        Match("4", "Bundesliga", "Bayern", "Leipzig", {"U2.5": 2.00}, {}),
    ]

    picks: List[Pick] = []

    for m in matches:
        probs = model_probabilities(m)

        for market, prob in probs.items():
            if market not in m.odds:
                continue

            odds = m.odds[market]
            edge = compute_edge(prob, odds)

            if edge < EDGE_MIN:
                continue

            stake = round(kelly_stake(prob, odds, bankroll), 2)
            signal = "GREEN" if edge >= EDGE_AGRESIVO else "YELLOW"

            picks.append(
                Pick(
                    match=f"{m.home} vs {m.away}",
                    league=m.league,
                    market=market,
                    prob=prob,
                    odds=odds,
                    edge=round(edge, 3),
                    stake=stake,
                    signal=signal
                )
            )

    return picks

# -----------------------------
# FUNCIÓN PARA STREAMLIT
# -----------------------------
def get_daily_picks(bankroll: float) -> List[Pick]:
    return run_pipeline(bankroll)
