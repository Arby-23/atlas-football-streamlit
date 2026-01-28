# atlas_engine.py
from dataclasses import dataclass
from typing import List
import random

@dataclass
class Pick:
    match: str
    market: str
    prob: float
    odds: float
    edge: float
    stake: float
    signal: str

def generate_picks(bankroll: float) -> List[Pick]:
    # Simulación MVP (luego conectas tu pipeline real)
    matches = [
        "Real Madrid vs Sevilla",
        "Man City vs Chelsea",
        "Inter vs Milan"
    ]

    picks = []

    for m in matches:
        prob = round(random.uniform(0.52, 0.60), 2)
        odds = round(random.uniform(1.80, 2.10), 2)
        edge = round(prob * odds - 1, 2)

        if edge < 0.05:
            continue

        stake = round(bankroll * 0.01, 2)
        signal = "GREEN" if edge >= 0.07 else "YELLOW"

        picks.append(
            Pick(m, "Under 2.5", prob, odds, edge, stake, signal)
        )

    return picks
