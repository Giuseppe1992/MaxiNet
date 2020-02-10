import json
import sys
import tempfile

from distriopt import VirtualNetwork
from distriopt.constants import *
from distriopt.embedding import PhysicalNetwork
from distriopt.embedding.algorithms import (
    EmbedBalanced,
    EmbedILP,
    EmbedPartition,
    EmbedGreedy,
)

MAPPERS={"EmbedBalanced":EmbedBalanced, "EmbedILP":EmbedILP, "EmbedPartition":EmbedPartition, "EmbedGreedy":EmbedGreedy}

def main():
    virtual_topo_file = sys.argv[1]
    physical_topo_file = sys.argv[2]
    mapper = sys.argv[3]

    virtual = VirtualNetwork.from_file(virtual_topo_file)
    physical = PhysicalNetwork.from_files(physical_topo_file)
    if mapper not in MAPPERS:
        raise ValueError(f"{mapper} not in {MAPPERS}")
    algo= MAPPERS[mapper]
    prob = algo(virtual, physical)
    time_solution, status = prob.solve()
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
        if status==1:
            # problem solved
            with open(temp.name,"w") as f:
                json.dump({"mapping":prob.solution.node_mapping},f)
        else:
            with open(temp.name, "w") as f:
                json.dump({"Infeasible": None}, f)


        print(temp.name, end="")
    except:
        raise RuntimeError( "problem in distrinet_runner.py")



if __name__ == '__main__':
    main()