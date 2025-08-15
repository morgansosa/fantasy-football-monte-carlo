from sim.config import LeagueConfig, TeamConfig
from sim.simulator import simulate_many

def test_runs():
    cfg = LeagueConfig(teams=[TeamConfig('A',120,15),TeamConfig('B',110,15)], weeks=6)
    df = simulate_many(cfg, iterations=100, seed=1)
    assert 'champ_rate' in df.columns
