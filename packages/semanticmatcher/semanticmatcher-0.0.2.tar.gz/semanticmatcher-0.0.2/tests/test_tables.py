import pandas as pd
import pytest
from semanticmatcher.tables import column_search, similarity_matrix


@pytest.fixture
def df1():
    return pd.DataFrame(
        {"col1": ["hello", "world"], "col2": ["how", "are"], "col3": ["you", "doing"]}
    )


@pytest.fixture
def df2():
    return pd.DataFrame(
        {
            "col1": ["hola", "mundo"],
            "col2": ["como", "estas"],
            "col3": ["tu", "haciendo"],
        }
    )


def test_column_search(df1, df2):
    # Test Case 1: Basic functionality
    results_df = column_search(df1, df2, num_matches=2)
    assert len(results_df) == 3
    assert set(results_df["df1_column"].tolist()) == set(["col1", "col2", "col3"])
    assert isinstance(results_df["df2_similar_columns"].iloc[0], list)
    assert len(results_df["df2_similar_columns"].iloc[0]) == 2

    # Test Case 2: Empty input
    with pytest.raises(ValueError):
        column_search(pd.DataFrame(), pd.DataFrame(), num_matches=2)

    # Test Case 3: Non-text input
    with pytest.raises(TypeError):
        column_search(
            pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}), df2, num_matches=2
        )


def test_similarity_matrix(df1, df2):
    # Test Case 1: Basic functionality
    similarity_matrix_df = similarity_matrix(df1, df2)
    assert similarity_matrix_df.shape == (3, 3)
    assert similarity_matrix_df.max().max() <= 1.0
    assert similarity_matrix_df.min().min() >= 0.0

    # Test Case 2: Empty input
    with pytest.raises(ValueError):
        similarity_matrix(pd.DataFrame(), pd.DataFrame())

    # Test Case 3: Non-text input
    with pytest.raises(TypeError):
        similarity_matrix(pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}), df2)
