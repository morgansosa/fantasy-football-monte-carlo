import os, click
from .config import load_config
from .simulator import simulate_many
from .data import write_sample_config

@click.group()
def cli(): pass

@cli.command()
@click.option('--config','config_path', default='league.yaml')
def init(config_path):
    write_sample_config(config_path)
    click.echo(f'Wrote sample config to {config_path}')

@cli.command()
@click.option('--config','config_path', required=True)
@click.option('--iterations','-n', default=2000)
@click.option('--seed', default=None)
@click.option('--output','-o', default='outputs/results.csv')
def run(config_path, iterations, seed, output):
    cfg = load_config(config_path)
    df = simulate_many(cfg, iterations=iterations, seed=seed)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    df.to_csv(output, index=False)
    click.echo(f'Wrote results to {output}')
    click.echo(df.to_string(index=False))

if __name__=='__main__': cli()
