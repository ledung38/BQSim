import math
import time

class Alpha:
    def create(self, global_data, xml_node):
        # self.__global_data = global_data
        self.delay = int(xml_node.get("delay", 1))
        self.days = int(xml_node.get("days", 7))
        self.mode = int(xml_node.get("mode", 0))
        self.close = global_data["close"]
        self.volume = global_data["volume"]
        self.dates = global_data["dates"]
        
        valid_univ = xml_node.get("valid", "ALL")
        self.valid = global_data[valid_univ]
        # self.close.setflags(write=True)
        self.dc = 0
        self.end_index = global_data["end_sim_di"]
        self.tickers = global_data["tickers"]
        
    
    def generate(self, di):
        if (di == self.end_index): self.print_data()

    def print_data(self):
        ii = 0
        for d in range(len(self.dates)):
            date = self.dates[d]
            print(date, self.tickers[ii], self.close[d][ii], self.volume[d][ii])

    
        
                
        

