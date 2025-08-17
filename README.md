## Project goals
- Monte Carlo simulation of fantasy football seasons
- Config-driven: teams, weeks, scoring rules
- Clean modules: simulate_matchup, simulate_week, simulate_season
- Output: CSV with win statistics: avg_wins, win_std, champ_rate

## How to Run
# initialize a sample league config
python -m src.sim.cli init --config league.yaml

# run a simulation with 2000 iterations
python -m src.sim.cli run --config league.yaml -n 2000 -o outputs/results.csv

## How to Run Tests
# install dev dependencies
pip install -r requirements.txt

# run the test suite
pytest -q