from Model.Building import Building


class Granary(Building):

    def __init__(self, tile):
        super().__init__(3, 3, tile, job_offered=6)
        self.capacity = 12
        self.current_stock = 0

    def __repr__(self):
        return "Granary"

    def __str__(self):
        string = super().__str__()
        string += f"\n\tCapacity: {self.current_stock}/{self.capacity}"
        return string

    def is_full(self):
        return self.current_stock >= self.capacity

    def is_empty(self):
        return self.current_stock <= 0

    # return True if a cartload was stocked, else False
    def stock(self):
        if self.is_active() and not self.is_full():
            self.current_stock += 1
            print("stocking in granary")
            return True
        else:
            return False

    # return True if a cartload was unstocked, else False
    def unstock(self):
        if self.is_active() and not self.is_empty():
            self.current_stock -= 1
            print("unstocking in granary")
            return True
        else:
            return False
