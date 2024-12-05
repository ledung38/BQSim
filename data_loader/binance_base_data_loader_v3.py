import numpy as np
import BUtils
import BDataUtils
import os
import bisect
import math
import random

NAN = float('nan')

def check_meta_valid(meta_info, data_start_date, meta_lines):
    try:
        if (len(meta_lines) < 3): return False
        if (meta_info != meta_lines[0]): return False
        current_data_start = int(meta_lines[1])
        if (current_data_start > data_start_date): return False
    except:
        return False
    return True

def get_daily_data_dates_sorted(daily_data_path):
    data_dates = []
    for filename in os.listdir(path=daily_data_path):
        if filename.endswith(".csv"):
            d = int(filename[0:-4])
            data_dates.append(d)
    return sorted(data_dates)

def load_daily_data(data_path, date, output):
    lines = BUtils.load_text_file(data_path + "/" + str(date) + ".csv")
    first = True
    for line in lines:
        if (first):
            first = False
            continue
        read = line.split(",")
        read[1] = int(read[1])
        # read[7] = int(read[7])
        output.append(read)

def aggregate_open(a, b):
    return a

def aggregate_close(a, b):
    return b

def aggregate_low(a, b):
    if (a < b): return a
    return b

def aggregate_high(a, b):
    if (a < b): return b
    return a

def aggregate_sum(a, b):
    return a+b

def get_aggregate_method(name):
    if (name == "open"): return aggregate_open
    if (name == "close"): return aggregate_close
    if (name == "high"): return aggregate_high
    if (name == "low"): return aggregate_low
    return aggregate_sum

def parse_field_map(text):
    output = []
    for s in text.split(" "):
        pair = s.split("=")
        output.append([pair[0], int(pair[1]), get_aggregate_method(pair[0])])
    return output

def polling_instrument_set(data_path, dates, instruments, instrument_map, di_start = 0):
    n = len(dates)
    di = di_start
    while (di < n):
        lines = BUtils.load_text_file(data_path + "/" + str(dates[di]) + ".csv")
        first = True
        for s in lines:
            if (first):
                first = False
                continue # ignore the first header line
            p = s.find(",")
            if (p >= 0):
                ticker = s[0:p]
                if not (ticker in instrument_map):
                    instrument_map[ticker] = len(instruments)
                    instruments.append(ticker)
        di += 1
    

def add_data_value(ci, method, data, di, ii, read):
    value = float(read[ci])
    if (math.isnan(value)): return
    if (math.isnan(data[di][ii])): data[di][ii] = value
    data[di][ii] = method(data[di][ii], value)

class BaseLoaderWorkingData:
    pass

def load_and_process_daily_data(wd):
    num_days = len(wd.dates)
    num_insts = len(wd.instruments)
    reads = []
    for di in range(wd.di_start, num_days):
        start_time = BUtils.get_date_timestamp(wd.dates[di]) + wd.start_time_secs
        end_time = start_time + 86400

        start_time *= 1000
        end_time *= 1000

        if (wd.start_time_secs == 0) or (di == wd.di_start):
            load_daily_data(wd.data_path, wd.dates[di], reads)
        if (wd.start_time_secs > 0):
            if (di+1 < len(wd.dates)):
                load_daily_data(wd.data_path, wd.dates[di+1], reads)
            else:
                load_daily_data(wd.data_path, wd.data_dates[wd.end_date_index+1], reads)

        for f in wd.data_fields:
            data = f[3]
            for ii in range(num_insts): data[di][ii] = NAN

        ri = 0
        while (ri < len(reads)) and (reads[ri][1] < start_time): ri += 1

        while (ri < len(reads)) and (reads[ri][1] < end_time):
            read = reads[ri]
            ii = wd.instrument_map[read[0]]
            for f in wd.data_fields: add_data_value(f[1], f[2], f[3], di, ii, read)
            ri += 1
        print("Loaded data on", wd.dates[di], "no of records =", ri)
        reads = reads[ri:]
    
  
def build_from_scratch(wd):
    wd.dates = []
    num_days = wd.end_date_index - wd.start_date_index + 1
    for di in range(num_days): wd.dates.append(wd.data_dates[wd.start_date_index + di])
    wd.instruments = []
    wd.instrument_map = {}
    
    polling_instrument_set(wd.data_path, wd.dates, wd.instruments, wd.instrument_map)
    num_insts = len(wd.instruments)
    for f in wd.data_fields:
        data = np.zeros((num_days, num_insts), dtype=np.float32)
        f.append(data)

    wd.di_start = 0
    load_and_process_daily_data(wd)

    BUtils.create_dir(wd.data_dir)
    BUtils.save_text_file(wd.data_dir + "/dates", wd.dates)
    BUtils.save_text_file(wd.data_dir + "/tickers", wd.instruments)
    for f in wd.data_fields: BDataUtils.save_np_array_data(wd.data_dir, f[0], f[3])


def load_and_update_data(wd):
    wd.dates = BUtils.load_array_from_text_file(wd.data_dir + "/dates", int)
    wd.instruments = BUtils.load_text_file(wd.data_dir + "/tickers")
    wd.instrument_map = {}
    num_insts = len(wd.instruments)
    for ii in range(num_insts): wd.instrument_map[wd.instruments[ii]] = ii

    num_days = len(wd.dates)
    for f in wd.data_fields: f.append(BDataUtils.load_np_array_data(wd.data_dir, f[0], np.float32, (num_days, num_insts)))
    
    last_date = wd.dates[num_days-1]
    di = bisect.bisect_left(wd.data_dates, last_date)
    if (wd.data_dates[di] == last_date): di += 1
    for i in range(di, wd.end_date_index+1): wd.dates.append(wd.data_dates[i])
    
    if (len(wd.dates) == num_days): return
    
    wd.di_start = num_days
    num_days = len(wd.dates)
    old_num_insts = num_insts
    polling_instrument_set(wd.data_path, wd.dates, wd.instruments, wd.instrument_map, wd.di_start)
    num_insts = len(wd.instruments)
    for f in wd.data_fields:
        old = f[3]
        if (old_num_insts == num_insts):
            f[3] = np.resize(old, (num_days, num_insts))
        else:
            data = np.zeros((num_days, num_insts), dtype=np.float32)
            f[3] = data
            for d in range(wd.di_start):
                for ii in range(old_num_insts): data[d][ii] = old[d][ii]
                for ii in range(old_num_insts, num_insts): data[d][ii] = NAN
        
    load_and_process_daily_data(wd)
    
    BUtils.save_text_file(wd.data_dir + "/dates", wd.dates, wd.di_start)
    if (old_num_insts == num_insts):
        for f in wd.data_fields: BDataUtils.append_np_array_data(wd.data_dir, f[0], f[3], wd.di_start)
    else:
        BUtils.save_text_file(wd.data_dir + "/tickers", wd.instruments, old_num_insts)
        for f in wd.data_fields: BDataUtils.save_np_array_data(wd.data_dir, f[0], f[3])    
    

def build_data(xml_node, global_data):
    wd = BaseLoaderWorkingData()
    wd.id, wd.data_dir = BUtils.get_basic_attrs(xml_node, global_data)
    wd.data_path = BUtils.format_path(BUtils.get_compulsory_attr(xml_node, "data_path", id))
    # data_period = BUtils.get_compulsory_attr(xml_node, "data_period", id)
    field_map = BUtils.get_compulsory_attr(xml_node, "field_map", id)
    wd.data_fields = parse_field_map(field_map)

    sim_start_date = global_data["start_date"]
    sim_end_date = global_data["end_date"]
    back_days = global_data["back_days"]
    daily_start_time = global_data["daily_start_time"]
    wd.start_time_secs = BUtils.time_to_seconds(daily_start_time)


    meta_info = str([field_map, wd.data_path, daily_start_time])

    meta_lines = BDataUtils.load_meta_file(wd.data_dir)

    wd.data_dates = get_daily_data_dates_sorted(wd.data_path)
    data_dates_limit = len(wd.data_dates)-1
    if (daily_start_time > 0): data_dates_limit -= 1

    wd.start_date_index = bisect.bisect_left(wd.data_dates, sim_start_date)
    if (wd.start_date_index < back_days): raise Exception("On date " + str(sim_start_date) + ", there are not enough history data for back days " + str(back_days))
    
    if (wd.start_date_index > data_dates_limit): raise Exception("There is no base data on the start date " + str(sim_start_date))

    wd.start_date_index -= back_days

    wd.end_date_index = bisect.bisect_left(wd.data_dates, sim_end_date)
    if (wd.end_date_index > data_dates_limit): wd.end_date_index = data_dates_limit

    if not check_meta_valid(meta_info, wd.data_dates[wd.start_date_index], meta_lines):
        build_from_scratch(wd)
        random.seed()
        meta_lines = [meta_info, wd.dates[0], random.randrange(0, 2000000000)]
        BDataUtils.save_meta_file(wd.data_dir, meta_lines)
    else: 
        load_and_update_data(wd)
        
        
    global_data["dates"] = wd.dates
    global_data["tickers"] = wd.instruments
    global_data["ticker_map"] = wd.instrument_map
    for f in wd.data_fields:
        global_data[f[0]] = f[3]
    global_data["data_version"] = int(meta_lines[2])
    start_di = bisect.bisect_left(wd.dates, sim_start_date)
    end_di = bisect.bisect_left(wd.dates, sim_end_date)
    if (end_di == len(wd.dates)) or (wd.dates[end_di] != sim_end_date): end_di -= 1
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
    for di in range(len(dates)): print(dates[di], instruments[ii], close[di][ii], volume[di][ii])
