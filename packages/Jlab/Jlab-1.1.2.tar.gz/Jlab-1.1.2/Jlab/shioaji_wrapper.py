class ShioajiWrapper:
    def __init__(self, api):
        self.api = api

    def get_stock_list(self):
        stock_list = [
            s
            for stock in self.api.Contracts.Stocks
            for s in stock
            if len(s["code"]) == 4
        ]
        code_list = [stock.code for stock in stock_list]
        return code_list
