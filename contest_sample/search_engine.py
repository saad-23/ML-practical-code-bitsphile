"""
Search Engine - Full-text search functionality
"""
import pandas as pd
from typing import List, Dict, Any

class SearchEngine:
    """Search functionality for dataframes"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.text_columns = df.select_dtypes(include=['object']).columns.tolist()

    def search(self, query: str, columns: List[str] = None, exact: bool = False) -> pd.DataFrame:
        """
        Search for query in dataframe
        """
        if not columns:
            columns = self.text_columns

        if not columns:
            return pd.DataFrame()

        query_lower = query.lower()
        mask = pd.Series([False] * len(self.df))

        for col in columns:
            if col in self.df.columns:
                if exact:
                    mask |= (self.df[col].astype(str).str.lower() == query_lower)
                else:
                    mask |= (self.df[col].astype(str).str.lower().str.contains(query_lower, na=False))

        return self.df[mask]

    def filter_numeric(self, column: str, min_val: float = None,
                      max_val: float = None) -> pd.DataFrame:
        """Filter by numeric range"""
        result = self.df.copy()

        if column in self.df.columns:
            if min_val is not None:
                result = result[result[column] >= min_val]
            if max_val is not None:
                result = result[result[column] <= max_val]

        return result

    def filter_categorical(self, column: str, values: List[str]) -> pd.DataFrame:
        """Filter by categorical values"""
        if column not in self.df.columns:
            return pd.DataFrame()

        return self.df[self.df[column].isin(values)]

    def advanced_filter(self, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Advanced filtering with multiple conditions
        filters = {
            'search_query': 'keyword',
            'column_filters': {
                'category': ['electronics', 'books'],
                'price': {'min': 100, 'max': 5000},
                'rating': {'min': 3.5}
            }
        }
        """
        result = self.df.copy()

        # Text search
        if 'search_query' in filters and filters['search_query']:
            search_result = self.search(filters['search_query'])
            result = result.loc[result.index.intersection(search_result.index)]

        # Column-specific filters
        if 'column_filters' in filters:
            for col, condition in filters['column_filters'].items():
                if col not in result.columns:
                    continue

                if isinstance(condition, dict):
                    # Numeric range
                    if 'min' in condition:
                        result = result[result[col] >= condition['min']]
                    if 'max' in condition:
                        result = result[result[col] <= condition['max']]
                elif isinstance(condition, list):
                    # Categorical values
                    result = result[result[col].isin(condition)]
                else:
                    # Single value
                    result = result[result[col] == condition]

        return result

    def get_suggestions(self, column: str, prefix: str) -> List[str]:
        """Get autocomplete suggestions"""
        if column not in self.df.columns:
            return []

        unique_vals = self.df[column].unique()
        suggestions = [str(v).lower() for v in unique_vals if str(v).lower().startswith(prefix.lower())]
        return list(set(suggestions))[:10]

    def get_filter_options(self, column: str) -> Dict[str, Any]:
        """Get available filter options for a column"""
        if column not in self.df.columns:
            return {}

        col_data = self.df[column]

        if col_data.dtype in ['int64', 'float64']:
            return {
                'type': 'numeric',
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'mean': float(col_data.mean())
            }
        else:
            return {
                'type': 'categorical',
                'unique_values': sorted(col_data.unique().tolist())[:100]
            }

    def multi_column_search(self, queries: Dict[str, str]) -> pd.DataFrame:
        """Search multiple columns with different queries"""
        result = self.df.copy()

        for column, query in queries.items():
            if column in self.df.columns:
                col_result = self.search(query, columns=[column])
                result = result.loc[result.index.intersection(col_result.index)]

        return result
