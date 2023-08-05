# semantic-matcher

[![Unit Tests](https://github.com/Aayushchou/semantic-matcher/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/Aayushchou/semantic-matcher/actions/workflows/unit_tests.yml)

This library is built to handle anything related to semantic matching.

In its current state, it has two main uses:

* Find the closest matches of a user query to a text corpus, using sentence transformer encodings and FAISS for optimization.
* Measure the semantic similarity between two tables and determine common columns. Useful for detecting duplicates and determining which columns to join on.


## 1. Installation

This package can be installed after cloning by running "make install". Alternatively it can be installed using pip: 

```
pip install semanticmatcher
```

## 2. Usage: 

This package can be used to simply search for a query within a text corpus. 

```python
from semanticmatcher.search import semantic_search

query = ["boy jumping"]
corpus = ["There was a young man running around town", "The mayor is looking for a new house", "I had pasta for dinner"]

scores, indices = semantic_search(query, corpus)

```

Additionally, the package can also be used to determine the similarity between two tables. It returns a matrix that compares each column.

```python
df1 = pd.DataFrame(
        {
            "col1": ["hello", "world"], 
            "col2": ["how", "are"], 
            "col3": ["you", "doing"]
         }
    )
    
df2 = pd.DataFrame(
        {
            "col1": ["hola", "mundo"],
            "col2": ["como", "estas"],
            "col3": ["tu", "haciendo"],
        }
    )

similarity_matrix_df = similarity_matrix(df1, df2)
```

By default, the following sentence transformer model is used to encode the text: "all-MiniLM-L6-v2".

## 3. Next Steps

Add functionality to allow users to join two tables on a column, depending on the similarity match between the columns. 
