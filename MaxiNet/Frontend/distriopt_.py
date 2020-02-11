import json
import os
from mininet.topo import Topo
import subprocess



class Mapper(object):
    def __init__(self, topo, physical_network_file, mapper):
        self.topo = topo
        self.physical_network_file = physical_network_file
        self.mapper = mapper
        self.topo_file = self.create_topo_file(topo)
        self.mapping_json_path = self._run_python3_distriopt(virtual_topo_file=self.topo_file,
                                                        physical_topo_file=physical_network_file,
                                                        mapper=mapper)

    @staticmethod
    def check_valid_path(physical_network_file):
        pass

    def create_topo_file(self,topo):
        assert isinstance(topo, Topo), "Invalid Network Format"
        filename = os.tempnam()
        json_topo={"nodes": {}, "links": {}}
        for node in topo.nodes():
            attrs = {"cores": topo.nodeInfo(node).get("cores", 1),
                     "memory": topo.nodeInfo(node).get("memory", 100)}
            json_topo["nodes"][node] = attrs

        for (u, v, attrs) in topo.iterLinks(withInfo=True):
            rate = attrs["bw"]
            edge_attrs = {"rate": rate}
            json_topo["links"][" ".join((u,v))]= edge_attrs

        with open(filename, "w") as f:
            json.dump(json_topo, f)

        return filename

    def create_mapping(self):
        with open(self.mapping_json_path, "r") as f:
            mapping = json.load(f)

        if "Infeasible" in mapping:
            print("MAPPING INFEASIBLE")
            exit(1)
        elif "mapping" in mapping:
            mapping = mapping["mapping"]
            return mapping
        else:
            raise ValueError("Returned value by the script not managed {}".format(mapping))


    def _run_python3_distriopt(self,virtual_topo_file, physical_topo_file, mapper, python3_script="/root/MaxiNet/MaxiNet/Frontend/distriopt_runner.py"):
        python3_command = "python3 {} {} {} {}".format(python3_script,virtual_topo_file,physical_topo_file,mapper)  # launch python3 script using bash

        process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        #return the temporary path for the mapping
        return output

