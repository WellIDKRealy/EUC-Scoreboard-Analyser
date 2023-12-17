class Error:
    def __init__(self, error):
        self.error = error

    def __repr__(self):
        return f'Error({self.error})'

    def to_dict(self):
        return {'error': self.error}

class Ok:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Ok({self.value})'

    def to_dict(self):
        return self.value

def is_error(val):
    return isinstance(val, Error)
