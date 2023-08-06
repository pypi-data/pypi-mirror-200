### Tetun LID
The Tetun Language Identification Model (Tetun LID) is an advanced machine learning model that automatically identifies the language of a given text. It has been specifically designed to recognize four languages commonly spoken in Timor-Leste: Tetun, Portuguese, Indonesian, and English.


Using a combination of cutting-edge algorithms and sophisticated linguistic features, Tetun LID has been trained on a large corpus of text data to accurately recognize the linguistic patterns and characteristics of each language. Its ability to accurately identify multiple languages makes it a valuable tool for anyone working with multilingual text data in Timor-Leste in the area of natural language processing (NLP) and information retrieval (IR) applications, such as language-specific search engines, sentiment analysis, and machine translation.

### Installation

```
pip install tetun-lid
```

### Dependecies

The Tetun LID package depends on the following packages:

* joblib
* scikit-learn
* Unicode

To install the dependencies packages, run the following commands:

```
pip install joblib
pip install scikit-learn
pip install Unidecode
```

### Usage

To use the Tetun LID, from `tetunlid` package, import `lid` as follows:

1. In case you want to predict a single input text.

```python

from tetunlid import lid

input_text = "Sé mak hamriik iha ne'ebá?"
output = lid.predict_language(input_text)

print(output)
```

The output will be:

```
Tetun
```

2. If you want to see details of why it was being predicted to Tetun, you can use the `predict_detail()` function.

```python

from tetunlid import lid

input_list_of_str = ["Sé mak hamriik iha ne'ebá?"]
output_detail = lid.predict_detail(input_list_of_str)
print('\n'.join(output_detail))
```

The output will be:

```
Input text: "Sé mak hamriik iha ne'ebá?"
Probability:
        English: 0.0007
        Indonesian: 0.0007
        Portuguese: 0.0006
        Tetun: 0.9980
Therefore, the probability of being "Tetun" is 99.80%.
```

`Note`: the input parameter and the output of `predict_detail()` is a `List[str]` or a list of string, thus, we need to use `for` loop or `join()` as in the example above to print the result.

3. You can use multiple languages as input. Observe the following example:

```python
from tetunlid import lid

multiple_langs = ["Ha'u ema baibain", "I am quite busy",
                  "Kamu malas sekali", "Vou sair daqui"]

output = [(ml, lid.predict_language(ml)) for ml in multiple_langs]
print(output)
```

The output will be:

```
[("Ha'u ema baibain", 'Tetun'), ('I am quite busy', 'English'), ('Kamu malas sekali', 'Indonesian'), ('Vou sair daqui', 'Portuguese')]
```

`Note`: This is how to simplify the codes and visualization. However, you can use `for` or any similar way to visualize in lines as follows:

```python
from tetunlid import lid

input_texts = ["Ha'u ema baibain", "I am quite busy",
               "Kamu malas sekali", "Vou sair daqui"]

for input_text in input_texts:
    lang = lid.predict_language(input_text)
    print(f"{input_text} ({lang})")
```

The output will be:

```
Ha'u ema baibain (Tetun)
I am quite busy (English)
Kamu malas sekali (Indonesian)
Vou sair daqui (Portuguese)
```

If you want to see details of each input, you can use a similar way as above. Here you go:

```python

from tetunlid import lid

input_texts = ["Ha'u ema baibain", "I am quite busy",
               "Kamu malas sekali", "Vou sair daqui"]

output_multiple_detail = lid.predict_detail(input_texts)
print('\n'.join(output_multiple_detail))
```

The output will be:

```
Input text: "Ha'u ema baibain"
Probability:
        English: 0.0027
        Indonesian: 0.0028
        Portuguese: 0.0024
        Tetun: 0.9920
Therefore, the probability of being "Tetun" is 99.20%.


Input text: "I am quite busy"
Probability:
        English: 0.9974
        Indonesian: 0.0007
        Portuguese: 0.0015
        Tetun: 0.0004
Therefore, the probability of being "English" is 99.74%.


Input text: "Kamu malas sekali"
Probability:
        English: 0.0001
        Indonesian: 0.9997
        Portuguese: 0.0001
        Tetun: 0.0001
Therefore, the probability of being "Indonesian" is 99.97%.


Input text: "Vou sair daqui"
Probability:
        English: 0.0034
        Indonesian: 0.0030
        Portuguese: 0.9912
        Tetun: 0.0023
Therefore, the probability of being "Portuguese" is 99.12%.
```

4. You can also use Tetun LID to predict a text from a file containing various languages. Here is an example:

```python
from pathlib import Path
from tetunlid import lid


file_path = Path("myfile/example.txt")

try:
    with file_path.open('r', encoding='utf-8') as f:
        contents = [line.strip() for line in f]
except FileNotFoundError:
    print(f"File not found at: {file_path}")

output = [(content, lid.predict_language(content)) for content in contents]
print(output)
```

There are a few more ways to read file contents that you can use to achieve the same output.

### Additional notes

1. Please follow the instruction as it is and try to understand how it works. All the dependencies need to be installed accordingly.
2. If you encountered an `AttributeError: 'list' object has no attribute 'predict_proba'`, you might have some issues while installing the package. Please send me an email, and I will guide you on how to handle the error.