from input import Input
from rank_output import RankOutput


class CsvHelper:

    def __init__(self, entry : Input) -> None:
        words : list[str] = [str(w["word"]) for w in entry.words_map]
        self.words_with_index : dict[str, int] = {word : i for i, word in enumerate(words)}

        self.filename : str = entry.output_file_name 

        self.initialize()


    def initialize(self) -> None:
        line = f"pub_number;{';'.join(self.words_with_index.keys())}"
        with open(self.filename, "a") as f:
            f.write(f"{line}\n")


    def write_line(self, ranks : RankOutput) -> None:
        pub_number = ranks.pub_number
        words = sorted(ranks.ranked_words, key = lambda x : self.words_with_index[str(x['word'])])

        with open(self.filename, "a") as f:
            f.write(f"{pub_number};{';'.join([str(w['rank']) for w in words])}\n")
         
