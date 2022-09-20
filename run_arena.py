import time
import os
import argparse
import csv

from dakon.agents.random import AgentRandom
from dakon.agents.mcts import AgentMonteCarlo
from dakon.agents.max import AgentMax
from dakon.agents.exact import AgentExact
from dakon.arena import Arena



PARSER = argparse.ArgumentParser(
    description='Run the arena with availabe agents')

PARSER.add_argument('--output', type=str, default='arena.results.csv',
                    help='Path to write arena results')

ARGS = PARSER.parse_args()

start = time.time()
print('Starting arena at',time.ctime())

agents = [
    # Place agents in this list as created
    # first in the tuple is the readable name
    # second is a lambda that ONLY takes a random seed. This can be discarded
    # if the the Agent does not require a seed
    ("Random", lambda seed: AgentRandom(seed)),
    # ('Max', lambda seed: AgentMax(seed)),
    # ('Exact', lambda seed: AgentExact(seed)),
    ('MonteCarlo', lambda seed: AgentMonteCarlo(seed, depth=6))
]


ARENA = Arena(agents)


print('Run the arena for: ', ARENA.csv_header())

with open(ARGS.output, 'w') as f:
    WRITER = csv.writer(f)
    WRITER.writerow(ARENA.csv_header())
    WRITER.writerows(ARENA.csv_results_lists())


print('Complete at', time.ctime())
print('Execution time:', "%s seconds" % (time.time() - start))
# print(AgentRandom().move(4))

# Agent().move()
