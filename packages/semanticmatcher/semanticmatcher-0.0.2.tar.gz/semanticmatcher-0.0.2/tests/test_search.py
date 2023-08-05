import pandas as pd
import pytest
from semanticmatcher.search import semantic_search, semantic_search_df


@pytest.fixture
def queries():
    return ["Hello world", "How are you?"]


@pytest.fixture
def documents():
    return ["Hello", "World", "How", "Are", "You"]


@pytest.fixture
def df1():
    return pd.DataFrame({"col1": ["Hello", "How"], "col2": ["World", "Are"]})


@pytest.fixture
def df2():
    return pd.DataFrame(
        {"col1": ["Hello", "How"], "col2": ["World", "Are"], "col3": ["Good", "Bye"]}
    )


def test_semantic_search(queries, documents):
    # Test Case 1: Basic functionality
    scores, indices = semantic_search(
        queries, documents, model_name="all-MiniLM-L6-v2", num_matches=2
    )
    assert scores.shape == (2, 2)
    assert indices.shape == (2, 2)

    # Test Case 2: Empty input
    with pytest.raises(ValueError):
        semantic_search([], [], model_name="all-MiniLM-L6-v2", num_matches=2)


def test_semantic_search_df(df1, df2):
    # Test Case 1: Basic functionality
    scores, indices = semantic_search_df(
        df1, df2, model_name="all-MiniLM-L6-v2", num_matches=2
    )
    assert scores.shape == (2, 2)
    assert indices.shape == (2, 2)

    # Test Case 2: Empty input
    with pytest.raises(ValueError):
        semantic_search_df(
            pd.DataFrame(), pd.DataFrame(), model_name="all-MiniLM-L6-v2", num_matches=2
        )

    # Test Case 3: Non-text input
    with pytest.raises(TypeError):
        semantic_search_df(
            pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
            df2,
            model_name="all-MiniLM-L6-v2",
            num_matches=2,
        )

    # Test Case 4: Unknown model name
    with pytest.raises(ValueError):
        semantic_search_df(df1, df2, model_name="unknown-model", num_matches=2)
