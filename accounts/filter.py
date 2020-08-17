
class filterQuerySet:
    def __init__(self, product, status, order_set):
        self.product = product
        self.status = status
        self.order_set = order_set

    def querySearch(self):
        if self.product and self.status:
            return self.order_set.filter(product=self.product, status=self.status)
        elif self.product:
            return self.order_set.filter(product=self.product)
        elif self.status:
            return self.order_set.filter(status=self.status)
