class VscoRequestException(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidProfileException(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg


class VscoImageAlreadyLoadedException(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg