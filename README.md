# Espacenet Scraper

A simpler scraper for espacenet

## Running the program

After installing the requirements by running

```
pip install -r requirements.txt
```

you can run

```
python main.py [path-to-your-input-file]
```

The input file must be a YAML file providing the following variables:

```yaml
action1:
  filename: output-file-name
  link: query-link
  words:
    -
      word: word1
      weight: word-weight (ex. 0.1)
    -
      word: word2 
      weight: word-weight (ex. 0.9)
    ...

action2:
  filename: output-file-name-2
  link: query-link-2
  words:
    -
      word: word1
      weight: word-weight (ex. 0.4)
    -
      word: word2 
      weight: word-weight (ex. 0.5)
    ...
```

Each action involves scraping a link analyzing words for each patent and provides an output file (whose name depends on the `filename` attribute) containing, for each patent provided by the query result, the patent ID and the weight for each word.

The weight is calculated by multiplying the given word weight by the number of occurences of the word inside the report description.



