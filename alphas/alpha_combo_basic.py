import BComboUtils
import math

def calc_daily_pnl(d, pos, valid, ret):
    size = len(pos)
    total_w = 0
    total_pnl = 0
    for ii in range(size):
        if (not valid[d-1][ii]): continue
        x = pos[ii]
        if (math.isnan(x)): continue
        total_w += abs(x)
        y = x * ret[d][ii]
        if (math.isnan(y)): continue
        total_pnl += y
    if (total_w < 1e-6): return 0
    return total_pnl * 1e+6 / total_w

def update_pnl_history(di, alpha_set, valid, ret, days, hist_pnls, is_first_day):
    if (is_first_day):
        di_start = di - days
    else:
        di_start = di - 1
    hi_start = di_start % days
    for ai in range(len(alpha_set)):
        __id, start_di, pos_data = alpha_set[ai]
        hi = hi_start
        for d in range(di_start, di):
            p = d - start_di - 1
            if (p >= 0) and (p < len(pos_data)): 
                hist_pnls[ai][hi] = calc_daily_pnl(d, pos_data[p], valid, ret)
            else:
                hist_pnls[ai][hi] = 0
            hi += 1
            if (hi == days): hi = 0
    

def combo_alpha_mean_variance(mode, di, alpha, alpha_set, valid, ret, days, hist_pnls, is_first_day):
    size = len(alpha)
    for ii in range(size):
        if (valid[di][ii]): alpha[ii] = 0.0

    # hist_pnls = calc_pnl_history(di, alpha_set, valid, ret, days)
    update_pnl_history(di, alpha_set, valid, ret, days, hist_pnls, is_first_day)
    if (mode == 1):
        weights = BComboUtils.optimize_invert_volatility(hist_pnls)
    elif (mode == 2):
        weights = BComboUtils.optimize_ir_weighted(hist_pnls)
    elif (mode == 3):
        weights = BComboUtils.optimize_ret_weighted(hist_pnls)
    else:
        weights = [1] * len(alpha_set)
    BComboUtils.normalize_weights(weights)
    return weights

class Alpha:
    def create(self, global_data, xml_node):
        valid_univ = xml_node.get("valid", "ALL")
        self.valid = global_data[valid_univ]
        self.ret1 = global_data["return"]
        self.days = int(xml_node.get("days", 100))

        self.dates = global_data["dates"]
        self.mode = int(xml_node.get("mode", 0))
        self.alpha_set, self.weights = BComboUtils.load_component_alpha_info(global_data, xml_node)
        self.dc = 0
        
    def generate(self, di):
        if (self.mode > 0):
            if (self.dc == 0): self.hist_pnls = BComboUtils.create_float_matrix(len(self.alpha_set), self.days)
            self.weights = combo_alpha_mean_variance(self.mode, di, self.alpha, self.alpha_set, self.valid, self.ret1, self.days, self.hist_pnls, (self.dc == 0))
        BComboUtils.generate_combo_alpha(di, self.alpha, self.alpha_set, self.valid, self.weights)
        self.dc += 1
    
    