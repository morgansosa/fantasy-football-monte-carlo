SAMPLE_CONFIG = """weeks: 14
teams:
  - {name: "Alpha", mean: 120.0, std: 15.0}
  - {name: "Bravo", mean: 115.0, std: 18.0}
  - {name: "Charlie", mean: 110.0, std: 20.0}
  - {name: "Delta", mean: 112.0, std: 17.0}
  - {name: "Echo", mean: 105.0, std: 22.0}
  - {name: "Foxtrot", mean: 118.0, std: 16.0}
  - {name: "Golf", mean: 109.0, std: 19.0}
  - {name: "Hotel", mean: 113.0, std: 17.0}
"""

def write_sample_config(path: str):
    with open(path, "w") as f:
        f.write(SAMPLE_CONFIG)
