from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from .config import LeagueConfig, TeamConfig


@dataclass
class SeasonResult:
    wins: Dict[str, int]
    points_for: Dict[str, float]
    champion: str


def _simulate_week_scores(
    teams: List[TeamConfig], rng: np.random.Generator
) -> Dict[str, float]:
    return {t.name: float(rng.normal(t.mean, t.std)) for t in teams}


def simulate_matchup(a, b, scores, rng):
    sa, sb = scores[a], scores[b]
    if sa > sb:
        return a
    if sb > sa:
        return b
    return a if rng.random() < 0.5 else b


def simulate_week(teams, week_pairs, rng):
    scores = _simulate_week_scores(teams, rng)
    results = []
    for a, b in week_pairs:
        winner = simulate_matchup(a, b, scores, rng)
        results.append((a, b, winner, scores[a], scores[b]))
    return results


def _round_robin_schedule(
    team_names: List[str], weeks: int, rng: np.random.Generator
) -> List[List[Tuple[str, str]]]:
    pairings = []
    for _ in range(weeks):
        shuffled = team_names.copy()
        rng.shuffle(shuffled)
        pairings.append(
            [(shuffled[i], shuffled[i + 1]) for i in range(0, len(shuffled), 2)]
        )
    return pairings


def simulate_season(config: LeagueConfig, seed: int | None = None) -> SeasonResult:
    rng = np.random.default_rng(seed)
    team_names = [t.name for t in config.teams]
    schedule = _round_robin_schedule(team_names, config.weeks, rng)
    wins = {t: 0 for t in team_names}
    points_for = {t: 0.0 for t in team_names}
    for week_pairs in schedule:
        week_results = simulate_week(config.teams, week_pairs, rng)
        for a, b, winner, sa, sb in week_results:
            points_for[a] += sa
            points_for[b] += sb
            wins[winner] += 1
    max_wins = max(wins.values())
    cands = [t for t, w in wins.items() if w == max_wins]
    if len(cands) == 1:
        champ = cands[0]
    else:
        sub = {t: points_for[t] for t in cands}
        m = max(sub.values())
        pf = [t for t, v in sub.items() if v == m]
        champ = pf[int(rng.integers(0, len(pf)))]
    return SeasonResult(wins=wins, points_for=points_for, champion=champ)


def simulate_many(
    config: LeagueConfig, iterations: int, seed: int | None = None
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    team_names = [t.name for t in config.teams]
    wins_matrix = {t: [] for t in team_names}
    champs = {t: 0 for t in team_names}
    for _ in range(iterations):
        sr = simulate_season(config, seed=int(rng.integers(0, 1_000_000_000)))
        for t in team_names:
            wins_matrix[t].append(sr.wins[t])
        champs[sr.champion] += 1
    df = pd.DataFrame(wins_matrix)
    return pd.DataFrame(
        {
            "team": team_names,
            "avg_wins": [df[t].mean() for t in team_names],
            "win_std": [df[t].std(ddof=1) for t in team_names],
            "champ_rate": [champs[t] / iterations for t in team_names],
        }
    ).sort_values(["champ_rate", "avg_wins"], ascending=[False, False])
