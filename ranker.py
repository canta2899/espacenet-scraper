from rank_output import RankOutput
from utils import WordsMapType
from input import Input
import re

class Ranker:
    
    def __init__(self) -> None:
        pass


    def rank(self, pub_number : str, description : str, input : Input) -> RankOutput:
        result : WordsMapType = []

        for entry in input.words_map:

            current_word : str = str(entry["word"])
            weight = int(entry["weight"])
            pattern = re.compile(current_word)
            matches = pattern.findall(description)
            computed_rank = len(matches) * weight
            result.append({
                "word": current_word,
                "rank": computed_rank
            })

        return RankOutput(pub_number, result) 

