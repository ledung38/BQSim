import math
import time

def get_signal(close, days, mode, d, ii):
    if (mode == 0): return close[d][ii] / close[d-days][ii] - 1.0
    if (mode == 1):
        s = 0
        n = 0
        for i in range(days):
            x = close[d-i-1][ii]
            if (math.isnan(x)): continue
            s += x
            n += 1
        avg = s / n
        return close[d][ii] / avg - 1.0
    if (mode == 2):
        low = close[d][ii]
        high = low
        for i in range(days):
            x = close[d-i-1][ii]
            if (math.isnan(x)): continue
            if (high < x): high = x
            if (low > x): low = x
        mid = (low + high) / 2
        return (close[d][ii] - mid) / (high - low)


class Alpha:
    def create(self, global_data, xml_node):
        # self.__global_data = global_data
        self.delay = int(xml_node.get("delay", 1))
        self.days = int(xml_node.get("days", 7))
        self.mode = int(xml_node.get("mode", 0))
        self.close = global_data["close"]
        self.volume = global_data["volume"]
        self.dates = global_data["dates"]
        
        valid_univ = xml_node.get("universe", "ALL")
        self.valid = global_data[valid_univ]
        # self.close.setflags(write=True)
        self.dc = 0
        self.end_index = global_data["end_sim_di"]
        self.tickers = global_data["tickers"]
        
    
    def generate(self, di):
        d = di - self.delay
        # if (self.mode == 2): time.sleep(0.0000001*self.days)
        # date = self.dates[di]
        # if (date > 20240220) and (date < 20240310): print(self.close[di][:])

        for ii in range(len(self.alpha)):
            if (not self.valid[di][ii]): continue
            self.alpha[ii] = get_signal(self.close, self.days, self.mode, d, ii)
            # self.alpha[ii] = 1.0
        
        # if (di == self.end_index): self.print_data()

        # self.dc += 1
        # print(self.dc)

    def print_data(self):
        # print("data size ", len(self.dates), len(self.tickers))
        # print(self.close.shape)
        ii = 0
        for d in range(len(self.dates)-100, len(self.dates)):
            date = self.dates[d]
            print(date, self.tickers[ii], self.close[d][ii], self.volume[d][ii])

    
        
                
        

