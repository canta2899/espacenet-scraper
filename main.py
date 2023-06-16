import sys
from csv_helper import CsvHelper
from input import Input
from ranker import Ranker
from scraper import Scraper

def main():
    input_file_path = sys.argv[1] or "./input.yaml"

    try:
        inputs : list[Input] = Input.from_yaml(input_file_path)
    except Exception:
        print("Error while parsing the input file")
        sys.exit(1)

    ranker = Ranker()
    scraper = Scraper()

    try:
        for entry in inputs:
            output = CsvHelper(entry)
            scraper.start(entry)
            scraper.rank_patents(ranker, output)
    except KeyboardInterrupt:
        print("Closing...")
        sys.exit(0)
    finally:
        scraper.quit()
        

if __name__ == '__main__':
    main()

