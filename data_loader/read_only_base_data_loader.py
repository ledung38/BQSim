import numpy as np
import BUtils
import BDataUtils
import bisect

def build_data(xml_node, global_data):
    id, data_dir = BUtils.get_basic_attrs(xml_node, global_data)
    data_fields = BUtils.get_compulsory_attr(xml_node, "fields", id).split(" ")
    
    sim_start_date = global_data["start_date"]
    sim_end_date = global_data["end_date"]
    
    meta_lines = BDataUtils.load_meta_file(data_dir)

    dates = BUtils.load_array_from_text_file(data_dir + "/dates", int)
    instruments = BUtils.load_text_file(data_dir + "/tickers")
    instrument_map = {}
    num_insts = len(instruments)
    for ii in range(num_insts): instrument_map[instruments[ii]] = ii

    num_days = len(dates)
    for fid in data_fields: global_data[fid] = BDataUtils.load_np_array_data(data_dir, fid, np.float32, (num_days, num_insts))
    global_data["dates"] = dates
    global_data["tickers"] = instruments
    global_data["ticker_map"] = instrument_map
    global_data["data_version"] = int(meta_lines[2])
    start_di = bisect.bisect_left(dates, sim_start_date)
    end_di = bisect.bisect_left(dates, sim_end_date)
    if (end_di == len(dates)) or (dates[end_di] != sim_end_date): end_di -= 1
    global_data["start_sim_di"] = start_di
    global_data["end_sim_di"] = end_di
    # test_data(global_data)


def test_data(global_data):
    dates = global_data["dates"]
    instruments = global_data["tickers"]
    instrument_map = global_data["ticker_map"]
    close = global_data["close"]
    volume = global_data["volume"]

    print("Test base data")
    ii = instrument_map["BTCUSDT"]
    num_days = len(dates)
    for di in range(num_days-100, num_days): print(dates[di], instruments[ii], close[di][ii], volume[di][ii])
