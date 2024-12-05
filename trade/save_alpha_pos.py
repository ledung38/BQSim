# import pickle
import BUtils
import numpy as np
import math

def get_data_version(filename):
    try:
        header = np.fromfile(filename, dtype=np.int32, count=1, sep="")
        if (len(header) < 1): return -1
        return header[0]
    except:
        return -1

def write_daily_alpha(di, alpha, fo):
    header = np.zeros((2), dtype=np.int32)
    header[0] = di
    n = len(alpha)
    while (n > 0):
        v = alpha[n-1]
        if math.isnan(v) or (abs(v) < 1e-6):
            n = n-1
        else: break
    if (n == 0): return
    header[1] = n
    header.tofile(fo, "")
    alpha[0:n].tofile(fo, "")
        

class Trade:
    def create(self, global_data, xml_node):
        self.output_dir = xml_node.get("output_dir", "./pos")
        self.file_format = int(xml_node.get("file_format", 0))
        mode = int(xml_node.get("mode", 0))
        self.dates = global_data["dates"]
        BUtils.create_dir(self.output_dir)
        filename = self.output_dir + "/" + self.alpha_id

        append_mode = False
        data_version = global_data["data_version"]
        if (mode == 1):
            file_version = get_data_version(filename)
            if (file_version == data_version): append_mode = True
        
        if (append_mode):
            self.out_file = open(filename, "ab")
        else:
            self.out_file = open(filename, "wb")
            header = np.zeros((1), dtype=np.int32)
            header[0] = data_version
            header.tofile(self.out_file, "")
        
    def calculate(self, di, alp):
        write_daily_alpha(di, alp.alpha, self.out_file)
        return None
    
    def finish(self):
        self.out_file.close()
        print("Saved " + self.output_dir + "/" + self.alpha_id)
