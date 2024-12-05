def parse_portfolio_info(info, global_data):
    output = []
    ticker_map = global_data["ticker_map"]
    for s in info.split(" "):
        pair = s.split("=")
        ii = ticker_map[pair[0]]
        weight = float(pair[1])
        output.append((ii, weight))
    return output
    

class Alpha:
    def create(self, global_data, xml_node):
        # self.__global_data = global_data
        self.delay = int(xml_node.get("delay", 1))
        self.portfolio_info = parse_portfolio_info(xml_node.get("portfolio", "BTCUSDT=1"), global_data)
        
        valid_univ = xml_node.get("valid", "ALL")
        self.valid = global_data[valid_univ]
        # self.close.setflags(write=True)
        self.dc = 0
        
    
    def generate(self, di):
        for (ii, weight) in self.portfolio_info:
            if (not self.valid[di][ii]): continue
            self.alpha[ii] = weight
        # print(self.alpha)
        

