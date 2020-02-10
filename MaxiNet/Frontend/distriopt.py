import json
import os
from mininet.topo import Topo
import subprocess



class Mapper(object):
    def __init__(self, topo, physical_network_file, mapper):
        self.topo = topo
        self.physical_network_file = physical_network_file
        self.mapper=mapper

    @staticmethod
    def check_valid_path(physical_network_file):
        pass

    def create_topo_file(self,topo):
        assert isinstance(topo, Topo), "Invalid Network Format"
        filename = os.tempnam()
        json_topo={"nodes": {}, "links": {}}
        for node in topo.nodes():
            attrs = {"cores": topo.nodeInfo(node).get("cores", 0),
                     "memory": topo.nodeInfo(node).get("memory", 0)}
            json_topo["nodes"][node] = attrs

        for (u, v, attrs) in topo.iterLinks(withInfo=True):
            u_port, v_port, rate = attrs["port1"], attrs["port2"], attrs["rate"]
            edge_attrs = {"devices":{u: u_port, v: v_port},"rate":rate}
            json_topo["links"][" ".join((u,v))]= edge_attrs

        with open(filename, "w") as f:
            json.dump(json_topo, f)

        return filename

    def create_mapping(self):
        pass

    def _run_python3_distriopt(self,virtual_topo_file, physical_topo_file, mapper, python3_script="distriopt_runner.py"):
        python3_command = "python3 {} {} {} {}".format(python3_script,virtual_topo_file,physical_topo_file,mapper)  # launch your python2 script using bash

        process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        output
        pass

