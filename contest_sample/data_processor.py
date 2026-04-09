"""
Data Sanitizer Module - Pandas-based Data Cleaning
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

class DataProcessor:
    """Data cleaning and sanitization using Pandas"""

    def __init__(self, df: pd.DataFrame):
        self.original_df = df.copy()
        self.df = df.copy()
        self.cleaning_report = {}

    def remove_duplicates(self) -> int:
        """Remove duplicate rows"""
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        removed = before - after
        self.cleaning_report['duplicates_removed'] = removed
        return removed

    def handle_missing_values(self, strategy: str = 'drop') -> Dict[str, int]:
        """
        Handle missing values
        strategy: 'drop', 'mean', 'median', 'forward_fill'
        """
        missing_before = self.df.isnull().sum().to_dict()

        if strategy == 'drop':
            self.df = self.df.dropna()
        elif strategy == 'mean':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                self.df[col].fillna(self.df[col].mean(), inplace=True)
        elif strategy == 'median':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                self.df[col].fillna(self.df[col].median(), inplace=True)
        elif strategy == 'forward_fill':
            self.df = self.df.fillna(method='ffill')

        missing_after = self.df.isnull().sum().to_dict()
        self.cleaning_report['missing_values_handled'] = missing_before
        return missing_before

    def remove_outliers(self, columns: list = None, method: str = 'iqr') -> int:
        """Remove outliers using IQR or Z-score"""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns

        before = len(self.df)

        if method == 'iqr':
            for col in columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]

        elif method == 'zscore':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            z_scores = np.abs((self.df[numeric_cols] - self.df[numeric_cols].mean()) / self.df[numeric_cols].std())
            self.df = self.df[(z_scores < 3).all(axis=1)]

        after = len(self.df)
        removed = before - after
        self.cleaning_report['outliers_removed'] = removed
        return removed

    def normalize_columns(self, columns: list = None) -> None:
        """Normalize numeric columns to 0-1 range"""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns

        for col in columns:
            if col in self.df.columns:
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                if max_val - min_val != 0:
                    self.df[col] = (self.df[col] - min_val) / (max_val - min_val)

    def clean_text_columns(self) -> None:
        """Clean text columns (strip, lowercase)"""
        text_cols = self.df.select_dtypes(include=['object']).columns
        for col in text_cols:
            self.df[col] = self.df[col].str.strip().str.lower()

    def get_data(self) -> pd.DataFrame:
        """Get cleaned dataframe"""
        return self.df.copy()

    def get_report(self) -> Dict[str, Any]:
        """Get cleaning report"""
        return {
            'original_rows': len(self.original_df),
            'cleaned_rows': len(self.df),
            'original_cols': len(self.original_df.columns),
            'cleaned_cols': len(self.df.columns),
            'report': self.cleaning_report
        }
