DEFAULT_QUESTION_TEXT = "--question--"
DEFAULT_MAX_GRADE = 1.0
DEFAULT_GRADE = 0.0


class Question:
    def __init__(self,
                 answer,
                 text=DEFAULT_QUESTION_TEXT,
                 max_grade=DEFAULT_MAX_GRADE,
                 grade=DEFAULT_GRADE):
        self.text = text
        self.max_grade = max_grade
        self.grade = grade
        self.answer = answer

    def to_dict(self):
        dict_obj = {
            "question": self.text,
            "max_grade": self.max_grade,
            "grade": self.grade,
            "answer": self.answer.to_dict()
        }

        return dict_obj
