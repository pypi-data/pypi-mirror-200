from Answer import Answer

DEFAULT_QUESTION_TEXT = "--question--"
DEFAULT_MAX_GRADE = 1.0
DEFAULT_GRADE = 0.0
DEFAULT_ANSWER = "--answer--"


class Question:
    def __init__(self,
                 text=DEFAULT_QUESTION_TEXT,
                 max_grade=DEFAULT_MAX_GRADE,
                 grade=DEFAULT_GRADE,
                 answer=DEFAULT_ANSWER):
        self.text = text
        self.max_grade = max_grade
        self.grade = grade
        self.answer = answer

    def to_dict(self):
        dict_obj = {
            "question": self.text,
            "max_grade": self.max_grade,
            "grade": self.grade,
            "answer": self.answer if self.answer == DEFAULT_ANSWER else self.answer.to_dict()
        }

        return dict_obj
