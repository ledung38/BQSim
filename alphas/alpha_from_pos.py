import numpy as np
import BUtils

def load_alpha_pos_data(filename):
    fi = open(filename, "rb")
    header = np.fromfile(fi, dtype=np.int32, count=1, sep="")
    data_version = header[0]
    output = []
    prev_di = -1
    while True:
        try:
            header = np.fromfile(fi, dtype=np.int32, count=2, sep="")
            if (len(header) < 2): break
            di = header[0]
            size = header[1]
            alpha = np.fromfile(fi, dtype=np.float32, count=size, sep="")
            if (prev_di < 0):
                start_di = di
            elif (prev_di + 1 < di):
                for i in range(prev_di+1, di): output.append([])
            output.append(alpha)
            prev_di = di
        except EOFError:
            break
    fi.close()
    return data_version, start_di, output

class Alpha:
    def create(self, global_data, xml_node):
        self.dates = global_data["dates"]
        pos_file = BUtils.get_compulsory_attr(xml_node, "alpha_pos", "Alpha")
        data_version, self.start_di, self.pos_data = load_alpha_pos_data(pos_file)
        if (global_data["data_version"] != data_version): raise Exception("File position " + pos_file + " has different data version with the base data")
        
    def generate(self, di):
        pi = di - self.start_di
        if (pi < 0): return
        if (pi >= len(self.pos_data)): return

        pos = self.pos_data[pi]
        for ii in range(len(self.alpha)):
            if (ii == len(pos)): break
            self.alpha[ii] = pos[ii]
    