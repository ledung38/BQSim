import math
import BUtils
import pickle

class Trade:
    def create(self, global_data, xml_node):
        # self.__global_data = global_data
        self.output_dir = xml_node.get("output_dir", "./pnl")
        BUtils.create_dir(self.output_dir)
        self.mode = int(xml_node.get("mode", 0))
        # self.close = global_data["close"]
        self.dates = global_data["dates"]
        self.ret1 = global_data["return"]
        self.num_days = 0
        self.total_pnl = 0
        self.total_pnl_2 = 0
        self.total_trade = 0
        self.total_booksize = 0
        self.total_long = 0
        self.total_short = 0
        self.stats = []
        # print(global_data["tickers"])

    def calculate(self, di, alp):
        alpha = alp.alpha
        prev_alpha = alp.prev_alpha
        size = len(alpha)
        booksize = 0
        pnl = 0
        long_book = 0
        short_book = 0
        trade = 0
        num_long = 0
        num_short = 0
        # pnls = []
        for ii in range(size):
            booksize += abs(alpha[ii])
            if (alpha[ii] > 0):
                long_book += alpha[ii]
                num_long += 1
            elif (alpha[ii] < 0):
                short_book -= alpha[ii]
                num_short += 1
            trade += abs(alpha[ii] - prev_alpha[ii])
            rt = self.ret1[di][ii]
            if (abs(rt) > 10): rt = 0
            if (math.isnan(rt)): rt = 0
            x = prev_alpha[ii] * rt
            pnl += x
            # pnls.append(x)
        # print(pnls)
        
        self.stats.append([self.dates[di], long_book, short_book, num_long, num_short, trade, pnl])
        self.total_pnl += pnl
        self.total_pnl_2 += pnl*pnl
        self.num_days += 1
        self.total_booksize += booksize
        self.total_long += long_book
        self.total_short += short_book
        self.total_trade += trade

        n = self.num_days
        ret = self.total_pnl / self.total_booksize * 365
        tvr = self.total_trade / self.total_booksize
        ir = 0
        if (n > 1):
            avg_pnl = self.total_pnl / n
            var = (self.total_pnl_2 - n * avg_pnl * avg_pnl) / (n-1)
            std = math.sqrt(var)
            ir = avg_pnl / std
        print_output = str(self.dates[di]) + " %15s   LONG x SHORT  %6.1f x %6.1f  %3d x %3d" % (alp.id, long_book * 1e-3, short_book*1e-3, num_long, num_short)
        print_output += "     TVR %5.1f   PNL %8.1f   Total PNL  %8.1f   RET %7.1f   IR %8.3f" % (tvr*100, pnl * 1e-3, self.total_pnl * 1e-3, ret * 100, ir)
        
        return print_output
    
    def finish(self):
        if (self.mode == 1):
            f = open(self.output_dir + "/" + self.alpha_id, "a")
        else:
            f = open(self.output_dir + "/" + self.alpha_id, "w")
        
        for stat in self.stats:
            first = True
            for item in stat:
                if (not first): f.write(",")
                f.write(str(item))
                first = False
            f.write("\n")
        f.close()

    def save_object_state(self, fo):
        pickle.dump((self.num_days, self.total_pnl, self.total_pnl_2, self.total_trade, self.total_booksize, self.total_long, self.total_short), fo)
    
    def load_object_state(self, fi):
        self.num_days, self.total_pnl, self.total_pnl_2, self.total_trade, self.total_booksize, self.total_long, self.total_short = pickle.load(fi)









        
        


