DEFAULT_OPTION_TEXT = "--option--"
DEFAULT_MATCHING_TEXT = "--text--"


class MatchingBlock:
    def __init__(self, text=DEFAULT_MATCHING_TEXT, selected_option=DEFAULT_OPTION_TEXT):
        self.text = text
        self.selected_option = selected_option


class MatchingAnswer:
    def __init__(self, html):
        self.matchings = []
        self.options = []
        self.parse_answer(html)

    def to_dict(self):
        dict_obj = {
            "options": [],
            "matchings": {}
        }

        for option in self.options:
            dict_obj["options"].append(option)
        for matching in self.matchings:
            dict_obj["matchings"][matching.text] = matching.selected_option

        return dict_obj

    def set_matching_options(self, options_block_html):
        options_html = options_block_html.find_all("option")

        for option in options_html:
            option_text = option.text.replace(" ", "").replace("\n", "")

            self.options.append(option_text)

    def get_selected_option(self, options_block_html):
        options_html = options_block_html.find_all("option")

        for option in options_html:
            option_text = option.text.replace(" ", "").replace("\n", "")
            try:
                if option["selected"] == "selected":
                    return option_text
            except:
                pass

        return DEFAULT_OPTION_TEXT

    def parse_answer(self, html):
        matching_blocks_html = html.find_all("tr", class_=["r0", "r1"])
        for block_html in matching_blocks_html:
            matching_block = MatchingBlock()

            matching_block.text = block_html.find("td", class_="text").text\
                .replace(" ", "")\
                .replace("\n", "")

            if not len(self.options):
                self.set_matching_options(block_html)
            matching_block.selected_option = self.get_selected_option(block_html)

            self.matchings.append(matching_block)
