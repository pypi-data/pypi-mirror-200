class Answer:
    def __init__(self, type, content):
        self.type = type
        self.content = content

    def to_dict(self):
        dict_obj = {
            "type": self.type,
            "content": self.content.to_dict()
        }

        return dict_obj


class AnswerType:
    CHOICE = "CHOICE"
    TEXT = "TEXT"
    MATCHING = "MATCHING"
