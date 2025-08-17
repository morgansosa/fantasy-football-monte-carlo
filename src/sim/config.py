from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import yaml, os

@dataclass
class TeamConfig:
    name: str
    mean: float
    std: float

@dataclass
class LeagueConfig:
    teams: List[TeamConfig]
    weeks: int
    scoring_rules: Optional[Dict[str, Any]] = None

def load_config(path: str) -> LeagueConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    teams = [TeamConfig(**t) for t in data["teams"]]
    weeks = int(data.get("weeks", 14))
    scoring = None
    if "scoring_rules" in data:
        base = os.path.dirname(os.path.abspath(path))
        rules_path = os.path.join(base, data["scoring_rules"])
        with open(rules_path, "r") as rf:
            scoring = yaml.safe_load(rf)
    return LeagueConfig(teams=teams, weeks=weeks, scoring_rules=scoring)
