class Transaction:

    def __init__(
        self,
        date,
        trans_type,
        category,
        amount,
        description=""
    ):
        self.date = date
        self.trans_type = trans_type
        self.category = category
        self.amount = amount
        self.description = description