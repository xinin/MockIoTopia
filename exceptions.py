class FieldSintaxError(Exception):
    """Exception raised for errors in the input field.

    Attributes:
        field -- input field which caused the error
        message -- explanation of the error
    """

    def __init__(self, field, message="FieldSintaxError"):
        self.field = field
        self.message = message
        super().__init__("\n"+str(self.field) +"\n"+ self.message)

class FieldNotSupportedError(Exception):

    def __init__(self, field, message="FieldNotSupportedError"):
        self.field = field
        self.message = message
        super().__init__("\n"+str(self.field) +"\n"+ self.message)