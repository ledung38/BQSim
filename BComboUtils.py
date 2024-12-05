import numpy as np
import math

def create_float_matrix(rsize, csize):
    return np.zeros((rsize, csize), dtype=np.float32)

def scale_weights(weights):
    m = len(weights)
    total = 0
    for i in range(m): total += abs(weights[i])
    if (total < 1e-6): return
    scale = 1.0 / total
    for i in range(m): weights[i] *= scale
    
def optimize_invert_volatility(pnls):
    (m, n) = pnls.shape
    weights = np.std(pnls, axis=1)
    for i in range(m):
        if (weights[i] < 1e-6):
            weights[i] = 0.0
        else:
            weights[i] = 1/weights[i]
    scale_weights(weights)
    return weights

def optimize_ir_weighted(pnls):
    (m, n) = pnls.shape
    weights = np.std(pnls, axis=1)
    for i in range(m):
        sdev = weights[i]
        if (sdev < 1e-6):
            weights[i] = 0
            continue
        total = 0
        for j in range(n): total += pnls[i][j]
        mean = total / n
        ir = mean / sdev
        if (ir < 0): ir = 0.0
        weights[i] = ir
    scale_weights(weights)
    return weights

def optimize_ret_weighted(pnls):
    (m, n) = pnls.shape
    weights = np.std(pnls, axis=1)
    for i in range(m):
        total = 0
        for j in range(n): total += pnls[i][j]
        mean = total / n
        if (mean < 1e-6): mean = 0.0
        weights[i] = mean
    scale_weights(weights)
    return weights

def generate_combo_alpha(di, alpha, alpha_set, valid, weights):
    size = len(alpha)
    for ii in range(size):
        if (valid[di][ii]): alpha[ii] = 0.0
    for ai in range(len(alpha_set)):
        __id, start_di, pos_data = alpha_set[ai]
        pi = di - start_di
        if (pi < 0) or (pi >= len(pos_data)): continue
        pos = pos_data[pi]
        size2 = size
        if (size2 > len(pos)): size2 = len(pos)
        total = 0
        for ii in range(size2):
            if (not valid[di][ii]): continue
            x = pos[ii]
            if (math.isnan(x)): continue
            total += abs(x)
        if (total < 1e-6): continue
        scale = weights[ai] * 1e+6 / total
        for ii in range(size2):
            if (not valid[di][ii]): continue
            x = pos[ii]
            if (math.isnan(x)): continue
            alpha[ii] += x * scale

def normalize_weights(weights):
    total = 0
    n = len(weights)
    for i in range(n): total += weights[i]
    if (total < 1e-6): return
    scale = 1.0 / total
    for i in range(n): weights[i] *= scale
    
def load_component_alpha_info(global_data, xml_node):
    alpha_ids = xml_node.get("alpha_ids", "").split(" ")
    database = global_data["AlphaDatabase"]
    alpha_set = []
    weights = []
    for item in alpha_ids:
        p = item.split("=")
        if (len(p) == 1):
            id = item
            weight = 1.0
        else:
            id = p[0]
            weight = float(p[1])
        start_di, pos_data = database[id]
        alpha_set.append((id, start_di, pos_data))
        weights.append(weight)
    normalize_weights(weights)
    return alpha_set, weights

    