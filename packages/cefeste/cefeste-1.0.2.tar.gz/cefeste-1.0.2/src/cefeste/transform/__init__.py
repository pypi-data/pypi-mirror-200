import pandas as pd


class ColumnExtractor(object):
    """Simple Class for extracting columns from a database.

    To be used in pipeline to apply the feature selection or elimination results
    """

    def __init__(self, cols):
        """Initialize the class with colums to keep."""
        self.cols = cols

    def transform(self, X):
        """Apply to a pd.DataFrame."""
        return X[self.cols]

    def fit(self, X, y=None):
        """No Fitter."""
        return self


class ColumnRenamer(object):
    """Simple Class for rename columns from a database.

    To be used in pipeline after transformers to allow further steps.
    """

    def __init__(self, col_names):
        """Initialize the class with columns name."""
        self.col_names = col_names

    def transform(self, X):
        """Apply to a np.array or pd.DataFrame."""
        X = pd.DataFrame(X, columns=self.col_names)
        return X

    def fit(self, X, y=None):
        """No Fitter."""
        return self
