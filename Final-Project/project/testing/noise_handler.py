class NoiseEliminator:
    def __init__(self, total_vals, min_vals):
        self.total_vals = total_vals
        self.min_vals = min_vals
        self.values = [None] * total_vals
        self.index = 0

    def is_valid(self, v):
        return 5 < v < 125  # reject nonsense readings

    def add_value(self, value):
        if not self.is_valid(value):
            return

        self.values[self.index] = value
        self.index = (self.index + 1) % self.total_vals

    def get_median_value(self):
        valid_values = [v for v in self.values if v is not None]
        if len(valid_values) < self.min_vals:
            return None
        sorted_values = sorted(valid_values)
        mid = len(sorted_values) // 2
        return sorted_values[mid]

    def get_stable_distance(self):
        return self.get_median_value()