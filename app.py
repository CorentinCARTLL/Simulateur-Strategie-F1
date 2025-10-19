# ============================================================
#  SIMULATEUR STRATÉGIE DE COURSE F1
#  Auteur : Corentin Cartallier
# ============================================================

# PARAMÈTRES GLOBAUX MODIFIABLES

RACE_LAPS = 64
BASE_LAP_TIME = 90.0
PIT_STOP_TIME = 25.0

TYRES = {
    "soft":         {"delta": -1.5, "degradation": 0.12, "max_laps": 12, "wear_per_lap": 8, "allowed_weather": ["dry"]},
    "medium":       {"delta": -0.7, "degradation": 0.07, "max_laps": 20, "wear_per_lap": 5, "allowed_weather": ["dry"]},
    "hard":         {"delta":  0.0, "degradation": 0.03, "max_laps": 35, "wear_per_lap": 3, "allowed_weather": ["dry"]},
    "intermediate": {"delta": +1.0, "degradation": 0.08, "max_laps": 20, "wear_per_lap": 5, "allowed_weather": ["light_rain"]},
    "wet":          {"delta": +0.5, "degradation": 0.05, "max_laps": 25, "wear_per_lap": 4, "allowed_weather": ["heavy_rain"]},
}

MAX_FUEL_CAPACITY = 150.0
FUEL_CONSUMPTION_PER_LAP = 5
FUEL_CONSUMPTION_RAIN_REDUCTION = {"light_rain": 2, "heavy_rain": 3}
FUEL_EFFECT_PER_LITRE = 0.03

LIFT_TIME_PENALTY = 1.0
LIFT_FUEL_SAVED = 3

RANDOMNESS = 0.05

# (tour_de_début, tour_de_fin, condition_météo)
WEATHER_SCHEDULE = [
    (1, 25, "dry"),
    (26, 35, "light_rain"),
    (36, 64, "dry")
]

# Imports nécessaires

import numpy as np
import pandas as pd
import itertools
import random
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# FONCTIONS DU SIMULATEUR
def get_weather_for_lap(lap):
    for start, end, w in WEATHER_SCHEDULE:
        if start <= lap <= end:
            return w
    return "dry"

def lap_time(lap_in_stint, tyre, fuel_litres, lift=False):
    tdata = TYRES[tyre]
    time = BASE_LAP_TIME + tdata["delta"]
    time += fuel_litres * FUEL_EFFECT_PER_LITRE
    time += tdata["degradation"] * lap_in_stint
    if lift:
        time += LIFT_TIME_PENALTY
    time += random.uniform(-RANDOMNESS, RANDOMNESS)
    return time

def simulate_strategy(stints, pit_stop_time=PIT_STOP_TIME):
    lap_times_cum, tyres_per_lap, fuel_per_lap, lift_per_lap, stints_with_lc = [], [], [], [], []
    total_time = 0.0

    fuel_needed = RACE_LAPS * FUEL_CONSUMPTION_PER_LAP
    fuel = min(fuel_needed, MAX_FUEL_CAPACITY)
    lift_laps_required = max(0, int(np.ceil((fuel_needed - fuel) / LIFT_FUEL_SAVED)))
    lc_counter = 0

    for stint_i, (tyre, laps) in enumerate(stints):
        if laps > TYRES[tyre]["max_laps"]:
            return np.inf, [], [], [], [], []

        lc_in_stint = 0
        for lap in range(1, laps + 1):
            lap_number = sum(s[1] for s in stints[:stint_i]) + lap
            weather = get_weather_for_lap(lap_number)

            if weather not in TYRES[tyre]["allowed_weather"]:
                return np.inf, [], [], [], [], []

            lift = lc_counter < lift_laps_required
            if lift:
                lc_in_stint += 1

            lap_fuel_for_time = fuel
            if weather in FUEL_CONSUMPTION_RAIN_REDUCTION:
                lap_fuel_for_time -= FUEL_CONSUMPTION_RAIN_REDUCTION[weather]

            t = lap_time(lap, tyre, lap_fuel_for_time, lift)
            total_time += t
            lap_times_cum.append(total_time)
            tyres_per_lap.append(tyre)
            fuel_per_lap.append(fuel)
            lift_per_lap.append(lift)

            fuel -= max(FUEL_CONSUMPTION_PER_LAP - LIFT_FUEL_SAVED, 0) if lift else FUEL_CONSUMPTION_PER_LAP
            if lift:
                lc_counter += 1

        stints_with_lc.append((tyre, laps, lc_in_stint))
        if stint_i < len(stints) - 1:
            total_time += pit_stop_time

    return total_time, lap_times_cum, tyres_per_lap, fuel_per_lap, lift_per_lap, stints_with_lc

# Génération de stratégies optimisée
def generate_strategies(total_laps=RACE_LAPS, max_stops=4):
    """
    Génère des stratégies en respectant la météo, mais avec limites pour éviter les boucles infinies.
    """
    segments = []
    for start, end, w in WEATHER_SCHEDULE:
        seg_len = end - start + 1
        allowed = [t for t, v in TYRES.items() if w in v["allowed_weather"]]
        if not allowed:
            return []
        max_laps_allowed = max(TYRES[t]["max_laps"] for t in allowed)
        min_stints = int(np.ceil(seg_len / max_laps_allowed))
        segments.append({"weather": w, "length": seg_len, "allowed": allowed, "min_stints": min_stints})

    min_total_stints = sum(seg["min_stints"] for seg in segments)
    if min_total_stints - 1 > max_stops:
        return []

    strategies = []
    MAX_PARTITIONS = 5   # limite du nombre de découpages par segment
    MAX_STRATEGIES = 200 # limite globale pour éviter de surcharger

    def split_lengths(seg_len, n_stints, max_len, min_len=5):
        results = []
        def backtrack(i, current, remaining):
            if len(results) >= MAX_PARTITIONS:
                return
            if i == n_stints - 1:
                if min_len <= remaining <= max_len:
                    results.append(current + [remaining])
                return
            max_here = min(max_len, remaining - min_len * (n_stints - 1 - i))
            for x in range(min_len, max_here + 1):
                backtrack(i + 1, current + [x], remaining - x)
        backtrack(0, [], seg_len)
        return results

    def build(seg_idx, built_stints, built_stops):
        if len(strategies) >= MAX_STRATEGIES:
            return
        if seg_idx == len(segments):
            strategies.append(built_stints[:])
            return

        seg = segments[seg_idx]
        seg_len = seg["length"]
        allowed = seg["allowed"]
        max_laps_allowed = max(TYRES[t]["max_laps"] for t in allowed)
        min_st = seg["min_stints"]
        max_st = min(min_st + 1, max_stops - built_stops + 1)

        for n_stints in range(min_st, max_st + 1):
            new_stops = built_stops + (n_stints - 1)
            if new_stops > max_stops:
                continue
            lengths = split_lengths(seg_len, n_stints, max_laps_allowed)
            for Ls in lengths:
                for combo in itertools.product(allowed, repeat=n_stints):
                    if len(strategies) >= MAX_STRATEGIES:
                        return
                    local_stints = [(combo[i], Ls[i]) for i in range(n_stints)]
                    build(seg_idx + 1, built_stints + local_stints, new_stops)

    build(0, [], 0)
    return strategies

# Évaluation des stratégies
def evaluate_strategies(total_laps=RACE_LAPS, max_stops=4):
    strategies = generate_strategies(total_laps, max_stops=max_stops)
    if not strategies:
        return pd.DataFrame()

    results = []
    for stints in strategies:
        total_time, laps, tyres, fuel, lift, stints_with_lc = simulate_strategy(stints)
        if np.isfinite(total_time):
            results.append({
                "strategy": stints_with_lc,
                "total_time": total_time,
                "laps": laps,
                "tyres_per_lap": tyres,
                "fuel_per_lap": fuel,
                "lift_per_lap": lift
            })

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    df.sort_values("total_time", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

# EXÉCUTION MAIN
if __name__ == "__main__":
    print("Simulation en cours...")

    # météo par tour
    weather_per_lap = []
    for start, end, condition in WEATHER_SCHEDULE:
        weather_per_lap.extend([condition] * (end - start + 1))

    df = evaluate_strategies(RACE_LAPS, max_stops=4)

    if df.empty:
        print("❌ Aucune stratégie valide trouvée (vérifie les paramètres).")
        exit(0)

    best = df.iloc[0]

    print("\n=== MEILLEURE STRATÉGIE ===")
    print("Stints :", best["strategy"])
    print(f"Temps total : {best['total_time']:.2f} s\n")

    #Visualisation
    laps = list(range(1, len(best["laps"]) + 1))
    lap_times = np.diff([0] + best["laps"])

    tyre_colors = {"soft":"red", "medium":"gold", "hard":"gray", "intermediate":"orange", "wet":"blue"}
    weather_colors = {"dry":"yellow", "light_rain":"orange", "heavy_rain":"blue"}

    fig, axes = plt.subplots(4, 1, figsize=(10, 12), sharex=True)

    #Temps au tour
    axes[0].scatter(laps, lap_times, c=[tyre_colors[t] for t in best["tyres_per_lap"]])
    axes[0].set_ylabel("Temps (s)")
    axes[0].set_title("Évolution du temps au tour")

    #Légende des pneus
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="red", label="Soft"),
        Patch(facecolor="gold", label="Medium"),
        Patch(facecolor="gray", label="Hard"),
        Patch(facecolor="orange", label="Intermediate"),
        Patch(facecolor="blue", label="Wet")
    ]
    axes[0].legend(handles=legend_elements, title="Type de pneu", loc="upper right")
    #Carburant
    axes[1].plot(laps, best["fuel_per_lap"], color="green")
    axes[1].set_ylabel("Carburant (L)")
    axes[1].set_title("Évolution du carburant")

    #Usure pneus (avec reset à chaque changement)
    wear = []
    current_tyre = best["tyres_per_lap"][0]
    laps_since_change = 0
    for i, tyre in enumerate(best["tyres_per_lap"]):
        if tyre != current_tyre:
            current_tyre = tyre
            laps_since_change = 0
        deg = max(100 - TYRES[tyre]["wear_per_lap"] * laps_since_change, 0)
        wear.append(deg)
        laps_since_change += 1
    axes[2].plot(laps, wear, color="purple")
    axes[2].set_ylabel("État des pneus (%)")
    axes[2].set_title("Usure des pneus")

    #Météo
    weather_map = {"dry":0, "light_rain":1, "heavy_rain":2}
    w_y = [weather_map[w] for w in weather_per_lap[:len(laps)]]
    axes[3].scatter(laps, w_y, c=[weather_colors[w] for w in weather_per_lap[:len(laps)]])
    axes[3].set_yticks([0,1,2])
    axes[3].set_yticklabels(["dry","light_rain","heavy_rain"])
    axes[3].set_xlabel("Tour")
    axes[3].set_title("Conditions météo")

    plt.tight_layout()
    plt.show()
