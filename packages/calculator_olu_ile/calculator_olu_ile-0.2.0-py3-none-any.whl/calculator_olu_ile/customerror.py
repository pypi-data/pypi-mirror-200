class NoneNumericValueError(Exception):
    def __init__(self, value):
        self.message = "A non-numeric value %s was used as input" % str(value)
        super().__init__(self.message)