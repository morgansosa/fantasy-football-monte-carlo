from dataclasses import dataclass
from typing import List
import yaml

@dataclass
class TeamConfig:
    name: str
    mean: float
    std: float

@dataclass
class LeagueConfig:
    teams: List[TeamConfig]
    weeks: int

def load_config(path: str) -> 'LeagueConfig':
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    teams = [TeamConfig(**t) for t in data['teams']]
    return LeagueConfig(teams=teams, weeks=int(data.get('weeks',14)))
