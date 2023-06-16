import yaml
from yaml import SafeLoader
from utils import WordsMapType

class Input:

    link : str
    output_file_name : str
    words_map : WordsMapType


    def __init__(self, link : str, output_file_name : str, words_map : WordsMapType) -> None:
        self.link = link
        self.output_file_name = output_file_name
        self.words_map = words_map


    @staticmethod
    def from_yaml(path : str):
        inputs : list[Input] = []

        with open(path, "r") as f:
            data = yaml.load(f, Loader=SafeLoader)
            for entry in data.values():
                inputs.append(Input(entry["link"], entry["filename"], entry["words"]))

        return inputs

