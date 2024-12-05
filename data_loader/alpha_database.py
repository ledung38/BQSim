import BUtils
import os
import numpy as np

def load_alpha_ids(list_input, alpha_pos_dir):
    if (list_input == "*"):
        output = []
        for filename in os.listdir(path=alpha_pos_dir):
            output.append(filename)
            # if (filename.startswith("alpha")):
            #     id = filename[5:]
            #     output.append(id)
        return output
    return list_input.split(" ")

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
                for __i in range(prev_di+1, di): output.append([])
            output.append(alpha)
            prev_di = di
        except EOFError:
            break
    fi.close()
    return data_version, start_di, output

def build_data(xml_node, global_data):
    id = BUtils.get_compulsory_attr(xml_node, "id", "AlphaDatabase")
    alpha_pos_dir = BUtils.format_path(BUtils.get_compulsory_attr(xml_node, "alpha_pos_dir", id))
    alpha_ids = load_alpha_ids(xml_node.get("alpha_ids", ""), alpha_pos_dir)

    base_data_version = global_data["data_version"]
    alpha_db = BUtils.BDict()
    for alpha_id in alpha_ids:
        data_version, start_di, pos_data = load_alpha_pos_data(alpha_pos_dir + "/" + alpha_id)
        if (data_version != base_data_version): raise Exception("alpha " + alpha_id + " has different data version with the base data")
        alpha_db[alpha_id] = (start_di, pos_data)

    global_data[id] = alpha_db

    test_data(global_data, id)
    
    
def test_data(global_data, id):
    database = global_data[id]
    for alpha_id in database:
        start_di, pos_data = database[alpha_id]
        print(id, "added alpha " + alpha_id, start_di, len(pos_data))
        


