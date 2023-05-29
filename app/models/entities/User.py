class User:
    def __init__(self, username: str, password: str, _id: str):
        self.username = username
        self.password = password
        self._id = _id
    def __str__(self):
        return f"{self.username}: {self.password}"