class Twit:
    def __init__(self, body, author):
        self.body = body
        self.author = author

    def to_dict(self):
        return {"body": self.body, "author": self.author}
