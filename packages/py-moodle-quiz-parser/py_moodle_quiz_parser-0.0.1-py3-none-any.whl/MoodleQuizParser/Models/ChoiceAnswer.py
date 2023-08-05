DEFAULT_CHOICE_TEXT = "--text--"


class ChoiceBlock:
    def __init__(self, text=DEFAULT_CHOICE_TEXT, selected=False):
        self.text = text
        self.selected = selected


class ChoiceAnswer:
    def __init__(self, html):
        self.choices = []
        self.parse_answer(html)

    def to_dict(self):
        dict_obj = []
        for choice in self.choices:
            dict_choice = {
                "text": choice.text,
                "selected": choice.selected
            }

            dict_obj.append(dict_choice)

        return dict_obj

    def parse_answer(self, html):
        choice_blocks_html = html.find_all("div", class_=["r0", "r1"])

        for block_html in choice_blocks_html:
            choice_block = ChoiceBlock()

            check_input = block_html.find("input", attrs={"checked": "checked"})
            if check_input is not None:
                choice_block.selected = True

            choice_block.text = block_html.text.replace(" ", "").replace("\n", "")

            self.choices.append(choice_block)
