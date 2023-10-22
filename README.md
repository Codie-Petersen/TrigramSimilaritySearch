# Trigram Similarity Search

This experiment utilizes trigram next character probability matrices combined with 1D cellular automata to showcase the efficacy of a nano model similarity search.

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Folder Structure](#folder-structure)
4. [How It Works](#how-it-works)
4. [Usage](#usage)
5. [Components Breakdown](#components-breakdown)
6. [Contribution](#contribution)
7. [License](#license)

## Introduction
Trigrams are sequences of three adjacent characters from a given string. This project aims to build a similarity search tool based on the probability matrix of known trigrams and their next character. In essence, it captures patterns in texts to provide similarity metrics for any given input.

## Installation
To get started with the Trigram Similarity Search project, follow these steps:

Clone the repository:
```bash
git clone https://github.com/your_username/trigram-similarity-search.git
cd trigram-similarity-search
```

## Folder Structure
The project is organized as follows:
```
trigram/
├── __init__.py
├── utils.py
└── vdb.py
.gitignore
explore.py
LICENSE
README.md
```

- `trigram/` contains the core modules of the project.
- `.gitignore` is a standard python ignore file.
- `LICENSE` is an MIT license detailing the terms of use.
- `README.md` provides this documentation.

## How It Works
The Trigram-Based Similarity Search represents a distinctive approach to evaluating textual similarity. By incorporating trigrams and a 1D cellular automata algorithm, this methodology offers a novel perspective on understanding the relationships between texts. Let's explore the process step by step:

### Entry Addition & Trigram Matrix Creation
Upon the addition of a new entry to the database, a key process is initiated:
- A unique trigram probability matrix (trigram model), tailored specifically for that entry, is crafted.
- This matrix encapsulates the particular patterns and structures of the entry, turning them into probabilities associated with every present trigram.
    - In the text "HELLO", "L" would have 100% chance coming after "HEL".
    - A sliding window approach is taken for all possible combinations of 3 chars (including spaces).
- It's essential to emphasize that every indvidual entry has its own exclusive trigram model.


### Brief Introduction to 1D Cellular Automata

1D Cellular Automata consist of a series of cells with defined states. Each cell's next state is determined by its current state combined with its neighbors' states based on set rules. Consider the following rule table:

| Trigram Pattern (Left-Center-Right) | Next State of Center Cell |
|------------------------------------|---------------------------|
| 000                                | 0                         |
| 001                                | 1                         |
| 010                                | 1                         |
| 011                                | 0                         |
| 100                                | 1                         |
| 101                                | 0                         |
| 110                                | 0                         |
| 111                                | 1                         |

Where 0 is represented by a space and 1 is represented by #.
Starting with an initial pattern: 0001000 (or visually: # )
The next iterations, using the above rules, will look as follows:
```
   #   
  # #  
 #   # 
# # # #
   #   
  # #  
 #   # 
```

### 1D Cellular Automata Transformation Using Trigram Model
Once a user inputs a prompt to discern similar entries, the engine delves into the core of its methodology:
- The input prompt is exposed to a transformation using the 1D cellular automata algorithm. This metamorphosis is guided by the trigram model associated with each entry in the database. Here, each character trigram acts as the guiding pattern that determines the next character's state.
- The logic here is nuanced but intuitive: The unique trigram model of an entry, distilled from its textual essence, directs the transformation of the user's prompt. This process is akin to 'seeing' the user's text through the 'lens' of each database entry's trigram model.
- An indicator of similarity lies in the extent of transformation: the more intact the prompt remains post-transformation, the more related it likely is to the entry. In other words, similar patterns exist in the entry as they do in the user prompt.

### Scoring the Transformed Prompts

Following the transformation process, a scoring mechanism is set in motion:
- Each transformed version of the prompt (after being processed using the trigram model of each entry) is scored based on its weighted Levenshtein distance from the original prompt. The weighted aspect ensures that certain transformations are deemed more significant than others, based on their inherent importance in relation to the content.
- The score signifies the degree of alteration the prompt has undergone. A lower score, indicating minimal transformation, suggests a stronger relationship between the prompt and the respective database entry.
- Next, we employ standard deviation scoring. In a dataset where many entries have transformed the prompt similarly, it's the outliers we are most interested in. A significant deviation from the average score could indicate either a very high or very low similarity with the original prompt, making these entries particularly noteworthy. Using standard deviation helps us highlight these entries and better understand the nature of their relationship with the input prompt.

## Usage
To explore the functionality:

1. Run `explore.py`:
```bash
python explore.py
```

2. When prompted, enter a sentence. The program will then display the similarity scores based on the built-in examples.

## Components Breakdown

1. **utils.py**: 
    - Provides essential functions such as `preprocess` for text cleaning, `get_trigram_model` for generating a probability matrix, `infer` for character inference, and various distance and scoring utilities.
   
2. **vdb.py**: 
    - Houses the core of the trigram database, facilitating functionalities such as adding, deleting, updating, and searching entries based on their trigram similarity scores.

3. **explore.py**: 
    - Serves as a demonstration script showcasing the project's capabilities with predefined sentences.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.We encourage the community to contribute and utilize this project while adhering to the terms outlined in our license.