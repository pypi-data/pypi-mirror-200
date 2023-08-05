"""
Match
----- 

Module containing table matching functionality. 

1. Columns from one table can be compared with columns from another table.
2. Columns from one table can be compared to columns from the same table.
3. Can return an overall match score between two tables. 

Tables are expected to be inputted as pandas dataframes with text or categorical features.
"""
import pandas as pd
from semanticmatcher.search import semantic_search_df


def column_search(df1: pd.DataFrame, df2: pd.DataFrame, num_matches: int = 2):
    """
    Get n best matches between the columns of two dataframes.

    Args:
        df1 - The query dataframe
        df2 - The corpus dataframe
        num_matches - The number of matches we want to find
    Returns:
        results_df - Dataframe with two columns, one with the column name from df1,
                    and another column containing a list of n closest matches.
    """
    scores, indices = semantic_search_df(df1, df2, num_matches=num_matches)
    results = {}
    for i, col in enumerate(df1.columns):
        results[col] = [df2.columns[idx] for idx in indices[i]]

    # Create a new DataFrame to display the results
    results_df = pd.DataFrame(
        results.items(), columns=["df1_column", "df2_similar_columns"]
    )
    return results_df


def similarity_matrix(df1: pd.DataFrame, df2: pd.DataFrame):
    """
    Get a similarity matrix containing similarity values between all columns in a dataframe.
    A higher value represents a stronger match.

    Args:
        df1 - The query dataframe
        df2 - The corpus dataframe
        num_matches - The number of matches we want to find
    Returns:
        similarity_matrix - Matrix dataframe containing the similarity between columns from each dataframe.
    """

    scores, indices = semantic_search_df(df1, df2, num_matches=df2.shape[1])
    similarity_matrix = pd.DataFrame(0, index=df1.columns, columns=df2.columns)
    for i, col in enumerate(df1.columns):
        similarity_matrix.loc[col, df2.columns[indices[i]]] = scores[i]

    # Display the similarity matrix
    return similarity_matrix


if __name__ == "__main__":
    df = pd.read_csv("data/titanic.csv")
    df = df[["Lname", "Name", "Sex"]]
    res = similarity_matrix(df, df)
    breakpoint()
