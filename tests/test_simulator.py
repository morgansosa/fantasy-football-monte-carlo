from sim.config import LeagueConfig, TeamConfig, load_config
from sim.simulator import simulate_many, simulate_matchup
import yaml, textwrap

def make_cfg():
    teams = [
        TeamConfig(name="A", mean=120.0, std=15.0),
        TeamConfig(name="B", mean=110.0, std=15.0),
        TeamConfig(name="C", mean=105.0, std=15.0),
        TeamConfig(name="D", mean=100.0, std=15.0),
    ]
    return LeagueConfig(teams=teams, weeks=8)

def test_runs_and_shapes():
    cfg = make_cfg()
    df = simulate_many(cfg, iterations=200, seed=42)
    assert set(df.columns) == {"team","avg_wins","win_std","champ_rate"}
    assert len(df) == 4

def test_matchup_tiebreak_coinflip():
    scores = {"A": 100.0, "B": 100.0}
    import numpy as np
    rng = np.random.default_rng(0)
    w = simulate_matchup("A", "B", scores, rng)
    assert w in ("A","B")

def test_load_config_reads_scoring(tmp_path):
    league = textwrap.dedent("""\
    weeks: 14
    scoring_rules: scoring.yaml
    teams:
      - {name: "A", mean: 120.0, std: 15.0}
      - {name: "B", mean: 110.0, std: 15.0}
    """)
    scoring_dict = {"pass_td": 4, "rush_td": 6}
    (tmp_path / "league.yaml").write_text(league)
    (tmp_path / "scoring.yaml").write_text(yaml.safe_dump(scoring_dict))
    cfg = load_config(str(tmp_path / "league.yaml"))
    assert cfg.scoring_rules is not None
    assert cfg.scoring_rules["pass_td"] == 4
