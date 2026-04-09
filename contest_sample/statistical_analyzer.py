"""
Statistical Analyzer - Quick Stats and Data Analysis
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List

class StatisticalAnalyzer:
    """Automated statistical analysis and summary generation"""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    def get_quick_stats(self) -> Dict[str, Any]:
        """Get comprehensive quick statistics"""
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage': float(self.df.memory_usage(deep=True).sum() / 1024),  # KB
            'numeric_summary': {},
            'categorical_summary': {},
            'missing_values': {},
            'duplicates': len(self.df) - len(self.df.drop_duplicates())
        }

        # Numeric statistics
        for col in self.numeric_cols:
            stats['numeric_summary'][col] = {
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'q1': float(self.df[col].quantile(0.25)),
                'q3': float(self.df[col].quantile(0.75)),
                'iqr': float(self.df[col].quantile(0.75) - self.df[col].quantile(0.25))
            }

        # Categorical statistics
        for col in self.categorical_cols:
            stats['categorical_summary'][col] = {
                'unique_values': int(self.df[col].nunique()),
                'most_common': self.df[col].mode().values[0] if len(self.df[col].mode()) > 0 else 'N/A',
                'value_counts': self.df[col].value_counts().to_dict()
            }

        # Missing values
        stats['missing_values'] = self.df.isnull().sum().to_dict()

        return stats

    def get_distribution_analysis(self, column: str) -> Dict[str, Any]:
        """Analyze distribution of a column"""
        if column not in self.df.columns:
            return {}

        col_data = self.df[column]

        if col_data.dtype in [np.int64, np.float64]:
            # Numeric distribution
            return {
                'type': 'numeric',
                'mean': float(col_data.mean()),
                'median': float(col_data.median()),
                'std': float(col_data.std()),
                'min': float(col_data.min()),
                'max': float(col_data.max()),
                'skewness': float(col_data.skew()),
                'kurtosis': float(col_data.kurtosis()),
                'bins': list(col_data.hist(bins=10)[0])
            }
        else:
            # Categorical distribution
            value_counts = col_data.value_counts()
            return {
                'type': 'categorical',
                'unique_count': int(col_data.nunique()),
                'most_common': col_data.mode().values[0],
                'distribution': value_counts.to_dict()
            }

    def get_correlation_analysis(self) -> Dict[str, float]:
        """Get correlation matrix for numeric columns"""
        if len(self.numeric_cols) < 2:
            return {}

        corr_matrix = self.df[self.numeric_cols].corr()
        return corr_matrix.to_dict()

    def get_summary_report(self) -> str:
        """Generate a text summary report"""
        report = "=" * 50 + "\n"
        report += "DATA SUMMARY REPORT\n"
        report += "=" * 50 + "\n\n"

        # Basic info
        report += f"Total Records: {len(self.df)}\n"
        report += f"Total Features: {len(self.df.columns)}\n"
        report += f"Duplicate Rows: {len(self.df) - len(self.df.drop_duplicates())}\n"
        report += f"Memory Usage: {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB\n\n"

        # Missing values
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            report += "Missing Values:\n"
            for col, count in missing[missing > 0].items():
                report += f"  {col}: {count} ({count/len(self.df)*100:.2f}%)\n"
        else:
            report += "No missing values found!\n"

        report += "\n" + "=" * 50 + "\n"
        report += "NUMERIC COLUMNS STATISTICS\n"
        report += "=" * 50 + "\n\n"

        for col in self.numeric_cols:
            report += f"{col}:\n"
            report += f"  Mean: {self.df[col].mean():.4f}\n"
            report += f"  Median: {self.df[col].median():.4f}\n"
            report += f"  Std Dev: {self.df[col].std():.4f}\n"
            report += f"  Min: {self.df[col].min():.4f}\n"
            report += f"  Max: {self.df[col].max():.4f}\n\n"

        report += "=" * 50 + "\n"

        return report

    def get_outlier_analysis(self, column: str) -> Dict[str, Any]:
        """Identify outliers in a column"""
        if column not in self.numeric_cols:
            return {}

        col_data = self.df[column]
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]

        return {
            'column': column,
            'total_points': len(col_data),
            'outlier_count': len(outliers),
            'outlier_percentage': (len(outliers) / len(col_data)) * 100,
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'outlier_values': outliers.tolist()
        }
