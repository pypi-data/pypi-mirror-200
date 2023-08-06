from bs4 import BeautifulSoup

from .Models.ChoiceAnswer import ChoiceAnswer
from .Models.MatchingAnswer import MatchingAnswer
from .Models.TextAnswer import TextAnswer

from .Models.Question import Question
from .Models.Answer import Answer
from .Models.Answer import AnswerType


class QuizParser:
    def __init__(self):
        self.tags = {
            "div": AnswerType.CHOICE,
            "span": AnswerType.TEXT,
            "table": AnswerType.MATCHING
        }

    def get_answer(self, answer_html):
        answer_type = self.tags[answer_html.name]
        if answer_type == AnswerType.CHOICE:
            answer_content = ChoiceAnswer(answer_html)
        elif answer_type == AnswerType.TEXT:
            answer_content = TextAnswer(answer_html)
        else:
            answer_content = MatchingAnswer(answer_html)

        answer = Answer(answer_type, answer_content)

        return answer

    def get_grade(self, target_html):
        grade_str = target_html.find("div", class_="grade").text.replace(" ", "")

        if grade_str.find("Баллов") != -1 or grade_str.find("Mark ") != -1:
            grade = float(grade_str[grade_str.find(" ") + 1:grade_str.find(" ") + 5].replace(",", "."))
        else:
            grade = 0.0

        return grade

    def get_max_grade(self, target_html):
        grade_str = target_html.find("div", class_="grade").text.replace(" ", "")
        max_grade = float(grade_str[len(grade_str)-4:len(grade_str)].replace(",", "."))

        return max_grade

    def to_dict(self, questions):
        dict_obj = []
        for question in questions:
            dict_obj.append(question.to_dict())

        return dict_obj

    def parse_html(self, html_text, parse_type="all", as_dict=False):
        html_content = BeautifulSoup(html_text, "html.parser")

        targets = html_content.body.find_all("div", class_="que")

        questions = []
        for target in targets:
            question = Question()
            text = target.find("div", class_="qtext").text.replace(" ", "").replace("\n", "")
            question.text = text

            if parse_type == "all":
                grade = self.get_grade(target)
                max_grade = self.get_max_grade(target)
                ablock = target.find("div", class_="ablock")
                answer = self.get_answer(ablock.find(class_="answer"))

                question.grade = grade
                question.max_grade = max_grade
                question.answer = answer
            questions.append(question)

        if as_dict:
            return self.to_dict(questions)

        return questions
