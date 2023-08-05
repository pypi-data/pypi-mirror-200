DEFAULT_TEXT = "--text--"


class TextAnswer:
    def __init__(self, html):
        self.text = ""
        self.parse_answer(html)

    def to_dict(self):
        dict_obj = {
            "text": self.text
        }

        return dict_obj

    def parse_answer(self, html):
        text_block = html.find("input", attrs={"type": "text"})
        try:
            self.text = text_block["value"]
        except:
            self.text = DEFAULT_TEXT
