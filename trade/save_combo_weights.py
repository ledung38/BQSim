# import pickle
import BUtils
import numpy as np
import math

class Trade:
    def create(self, global_data, xml_node):
        self.output_dir = xml_node.get("output_dir", "./weights")
        # self.file_format = int(xml_node.get("file_format", 0))
        mode = int(xml_node.get("mode", 0))
        self.dates = global_data["dates"]
        BUtils.create_dir(self.output_dir)
        filename = self.output_dir + "/" + self.alpha_id

        if (mode == 1):
            self.out_file = open(filename, "a")
        else:
            self.out_file = open(filename, "w")
            
    def calculate(self, di, alp):
        self.out_file.write(str(self.dates[di]))
        n = len(alp.alpha_set)
        for i in range(n):
            id = alp.alpha_set[i][0]
            w = alp.weights[i]
            self.out_file.write("," + id + "=" + str(w))
        self.out_file.write("\n")
        return None
    
    def finish(self):
        self.out_file.close()
        print("Saved " + self.output_dir + "/" + self.alpha_id)
