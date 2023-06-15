import sys
import yaml
from yaml.loader import SafeLoader

def get_word_with_weight(a):
    entry = a.split(":")
    return {"word": entry[0], "weight": float(entry[1])}

def parse_input_file(path):
    try:
        with open(path, "r") as f:
            data = yaml.load(f, Loader=SafeLoader)
            print(type(data))
            return data.values()
    except:
        print("Invalid input file")
        sys.exit(1)

def write_output_header(input_entry):
    filename = input_entry["filename"]
    print(input_entry)
    words = list(map(lambda x: x["word"], input_entry["words"]))
    line = f"publication_number;{';'.join(words)}"
    with open(filename, "w") as f:
        f.write(f"{line}\n")
