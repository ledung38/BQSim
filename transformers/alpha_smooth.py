import math
import numpy as np

def generate_coefficients(mode, n, factor):
    coeffs = np.zeros((n), dtype=np.float32)
    if (mode == 0):
        for i in range(n): coeffs[i] = 1.0
    elif (mode == 1):
        for i in range(n): coeffs[i] = math.pow(i+1, factor)
    elif (mode == 2):
        coeffs[0] = 1.0
        for i in range(1, n): coeffs[i] = coeffs[i-1] * factor
    return coeffs

def run_operation(alpha, history, di, n, coeffs):
    for ii in range(len(alpha)):
        a = alpha[ii]
        if (math.isnan(a)):
            history[di][ii] = 0.0
            continue
        history[di][ii] = a
        total = a * coeffs[0]
        d = di
        for i in range(1, n):
            if (d == 0): d = n
            d -= 1
            total += history[d][ii] * coeffs[i]
        alpha[ii] = total
    

class Transform:
    def create(self, global_data, xml_node):
        # self.__global_data = global_data
        mode = int(xml_node.get("mode", 0))
        self.days = int(xml_node.get("days", 5))
        factor = float(xml_node.get("factor", 1.0))
        self.coeffs = generate_coefficients(mode, self.days, factor)
        alpha_size = len(global_data["tickers"])
        self.history = np.zeros((self.days, alpha_size), dtype=np.float32)
        self.dc = 0
        

    def transform(self, alpha):
        run_operation(alpha, self.history, self.dc, self.days, self.coeffs)
        self.dc += 1
        if (self.dc == self.days): self.dc = 0
