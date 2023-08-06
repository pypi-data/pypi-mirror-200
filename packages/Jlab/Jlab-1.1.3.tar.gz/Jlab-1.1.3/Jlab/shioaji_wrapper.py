import datetime


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

    def get_near_month_txf_contract(self):
        contract = min(
            [
                x
                for x in self.api.Contracts.Futures.TXF
                if x.code[-2:] not in ["R1", "R2"]
            ],
            key=lambda x: x.delivery_date,
        )
        return contract

    def is_market_open(self):
        now = datetime.datetime.now()
        contract = self.get_near_month_txf_contract()
        update_date_str = contract.update_date
        update_date = datetime.datetime.strptime(update_date_str, "%Y/%m/%d").date()
        return update_date == now.date()
