import BUtils
import BDataUtils
import numpy as np

def build_data(xml_node, global_data):
    id, data_dir = BUtils.get_basic_attrs(xml_node, global_data)
    days = int(xml_node.get("days", 20))
    size = int(xml_node.get("size", 10000))
    min_adv = float((xml_node.get("min_adv", 1e+6)))
    
    meta_info = str([global_data["data_version"], days, min_adv])
    old_shape = BDataUtils.get_reusable_data_shape(data_dir, meta_info)

    dates = global_data["dates"]
    tickers = global_data["tickers"]
    num_days = len(dates)
    num_tickers = len(tickers)
    data_infos = []
    valid = BDataUtils.register_data(global_data, data_infos, data_dir, id, bool, old_shape, (num_days, num_tickers), False)
    
    di_start = old_shape[0]
    if (di_start == num_days): return 
    
    close = global_data["close"]
    volume = global_data["volume"]
    
    target_vol = min_adv * days
    vol = np.zeros((num_tickers), dtype=np.float32)
    list_v = np.zeros((num_tickers), dtype=np.float32)
    for di in range(di_start, num_days):
        if (di <= days):
            for ii in range(num_tickers): valid[di][ii] = False
            continue
        cc = 0
        for ii in range(num_tickers):
            sum = 0
            for d in range(di-days, di-1): sum += close[d][ii] * volume[d][ii]
            vol[ii] = sum
            if (sum > target_vol):
                list_v[cc] = sum
                cc += 1
        threshold = target_vol
        if (cc > size): threshold = BUtils.find_k_element(list_v, cc, size)
        cc = 0
        for ii in range(num_tickers):
            valid[di][ii] = (vol[ii] > threshold)
            if (valid[di][ii]): cc += 1
        print("[" + id + "]:", dates[di], "No of valids", cc, "threshold %0.3f" % (threshold/days*1e-6))
    
    BUtils.create_dir(data_dir)
    meta_lines = [meta_info, num_days, num_tickers]
    BDataUtils.save_meta_file(data_dir, meta_lines)
    if (num_tickers > old_shape[1]):
        BDataUtils.save_all_register_data(data_dir, data_infos)
    else:
        BDataUtils.append_all_register_data(data_dir, data_infos, di_start)

    
    
    
def test_data(global_data, id):
    valid = global_data[id]
    dates = global_data["dates"]
    tickers = global_data["tickers"]
    num_days = len(dates)
    num_tickers = len(tickers)
    for di in range(num_days):
        print(dates[di], valid[di][:])


