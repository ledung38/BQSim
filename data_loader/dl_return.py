import math
import BUtils
import BDataUtils
import numpy as np

def build_data(xml_node, global_data):
    id, data_dir = BUtils.get_basic_attrs(xml_node, global_data)
    days = int(xml_node.get("days", 1))
    meta_info = str([global_data["data_version"], days])
    old_shape = BDataUtils.get_reusable_data_shape(data_dir, meta_info)

    dates = global_data["dates"]
    tickers = global_data["tickers"]
    num_days = len(dates)
    num_tickers = len(tickers)
    data_infos = []

    NAN = float('nan')
    data_name = "return"
    if (days > 1): data_name += str(days)
    data = BDataUtils.register_data(global_data, data_infos, data_dir, data_name, np.float32, old_shape, (num_days, num_tickers), NAN)
    
    di_start = old_shape[0]
    if (di_start == num_days): return 
    
    close = global_data["close"]
    for di in range(di_start, num_days):
        if (di < days):
            for ii in range(num_tickers): data[di][ii] = NAN
            continue
        cc = 0
        for ii in range(num_tickers):
            rt = close[di][ii] / close[di-days][ii] - 1.0
            if (abs(rt) > 1.0): rt = 0.0
            if (not math.isnan(rt)): cc += 1
            data[di][ii] = rt
            
        print("[" + id + "]:", dates[di], "No of valids", cc)
    
    BUtils.create_dir(data_dir)
    meta_lines = [meta_info, num_days, num_tickers]
    BDataUtils.save_meta_file(data_dir, meta_lines)
    if (num_tickers > old_shape[1]):
        BDataUtils.save_all_register_data(data_dir, data_infos)
    else:
        BDataUtils.append_all_register_data(data_dir, data_infos, di_start)

    
