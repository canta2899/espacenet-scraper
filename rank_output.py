from utils import WordsMapType

class RankOutput:

    def __init__(self, pub_number : str, ranked_words : WordsMapType) -> None:
        self.pub_number : str = pub_number
        self.ranked_words : list[dict[str, str | int]] = ranked_words

