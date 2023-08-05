# py-moodle-quiz-parser

**py-moodle-quiz-parser** is simple Python library for fast parsing HTML documents with Moodle quizes.
```python
from MoodleQuizParser.QuizParser import QuizParser

parser = QuizParser()
file = open("moodle_quiz.html", encoding="utf-8")

parsed_data = parser.parse_html(file.read(), as_dict=True)
```
## How to use this library

To use **py-moodle-quiz-parser** you should simply install it using PIP
```python
pip install py-moodle-quiz-parser
```
