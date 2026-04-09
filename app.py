from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import os
from io import BytesIO
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DataSanitizer:
    """Complete data sanitization toolkit using Pandas"""

    def __init__(self, df):
        self.original_df = df.copy()
        self.df = df.copy()
        self.cleaning_log = []

    def get_initial_stats(self):
        """Get initial data statistics"""
        return {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'duplicates': self.df.duplicated().sum(),
            'missing': self.df.isnull().sum().to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2
        }

    def handle_missing_values(self, strategy='drop', column=None, fill_value=None):
        """Handle missing values with various strategies"""
        if strategy == 'drop':
            if column:
                before = len(self.df)
                self.df = self.df.dropna(subset=[column])
                after = len(self.df)
                self.cleaning_log.append({
                    'action': 'Drop NaN',
                    'column': column,
                    'rows_affected': before - after
                })
            else:
                before = len(self.df)
                self.df = self.df.dropna()
                after = len(self.df)
                self.cleaning_log.append({
                    'action': 'Drop all NaN rows',
                    'rows_affected': before - after
                })

        elif strategy == 'mean':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            self.cleaning_log.append({
                'action': 'Fill numeric NaN with mean',
                'columns': len(numeric_cols)
            })

        elif strategy == 'median':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            self.cleaning_log.append({
                'action': 'Fill numeric NaN with median',
                'columns': len(numeric_cols)
            })

        elif strategy == 'forward_fill':
            self.df = self.df.fillna(method='ffill')
            self.cleaning_log.append({'action': 'Forward fill NaN'})

        elif strategy == 'fill_value':
            self.df = self.df.fillna(fill_value)
            self.cleaning_log.append({'action': f'Fill NaN with {fill_value}'})

    def remove_duplicates(self, subset=None):
        """Remove duplicate rows"""
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset)
        after = len(self.df)
        self.cleaning_log.append({
            'action': 'Remove duplicates',
            'rows_removed': before - after
        })

    def remove_outliers(self, method='iqr', columns=None, threshold=1.5):
        """Remove outliers using IQR or Z-score"""
        if columns is None:
            columns = self.df.select_dtypes(include=[np.number]).columns

        before = len(self.df)

        if method == 'iqr':
            for col in columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]

        elif method == 'zscore':
            for col in columns:
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                self.df = self.df[z_scores <= threshold]

        after = len(self.df)
        self.cleaning_log.append({
            'action': f'Remove outliers ({method})',
            'rows_removed': before - after,
            'columns': list(columns)
        })

    def convert_data_types(self):
        """Auto-convert columns to appropriate data types"""
        changes = {}
        for col in self.df.columns:
            original_type = str(self.df[col].dtype)

            # Try to convert to numeric
            try:
                converted = pd.to_numeric(self.df[col], errors='coerce')
                if converted.notna().sum() / len(self.df) > 0.8:  # If 80%+ values converted
                    self.df[col] = converted
                    changes[col] = f"{original_type} -> numeric"
                    continue
            except:
                pass

            # Try to convert to datetime
            try:
                converted = pd.to_datetime(self.df[col], errors='coerce')
                if converted.notna().sum() / len(self.df) > 0.8:
                    self.df[col] = converted
                    changes[col] = f"{original_type} -> datetime"
                    continue
            except:
                pass

            # Convert object to category if < 20% unique values
            if self.df[col].dtype == 'object' and self.df[col].nunique() / len(self.df) < 0.2:
                self.df[col] = self.df[col].astype('category')
                changes[col] = f"{original_type} -> category"

        self.cleaning_log.append({
            'action': 'Convert data types',
            'columns_changed': len(changes),
            'details': changes
        })

    def clean_text(self, columns=None):
        """Clean text columns: lowercase, strip whitespace, remove special chars"""
        if columns is None:
            columns = self.df.select_dtypes(include=['object']).columns

        for col in columns:
            before = self.df[col].copy()
            self.df[col] = self.df[col].str.strip()  # Remove leading/trailing whitespace
            self.df[col] = self.df[col].str.lower()  # Lowercase

            # Remove extra spaces
            self.df[col] = self.df[col].str.replace(r'\s+', ' ', regex=True)

        self.cleaning_log.append({
            'action': 'Clean text columns',
            'columns': list(columns)
        })

    def get_final_stats(self):
        """Get final data statistics"""
        return {
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'duplicates': self.df.duplicated().sum(),
            'missing': self.df.isnull().sum().to_dict(),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2
        }

    def get_comparison(self):
        """Compare before and after stats"""
        initial = self.get_initial_stats()
        final = self.get_final_stats()

        return {
            'rows_removed': initial['rows'] - final['rows'],
            'duplicates_removed': initial['duplicates'] - final['duplicates'],
            'memory_saved_mb': initial['memory_usage'] - final['memory_usage']
        }

    def to_csv(self):
        """Convert cleaned dataframe to CSV"""
        return self.df.to_csv(index=False)

    def get_preview(self, rows=10):
        """Get preview of cleaned data"""
        return self.df.head(rows).to_html(classes='table table-striped')


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are supported'}), 400

    try:
        df = pd.read_csv(file)

        # Store in session-like manner
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df.to_csv(filepath, index=False)

        # Get initial stats
        sanitizer = DataSanitizer(df)
        stats = sanitizer.get_initial_stats()

        return jsonify({
            'success': True,
            'filename': filename,
            'stats': {
                'rows': stats['rows'],
                'columns': stats['columns'],
                'duplicates': int(stats['duplicates']),
                'missing_count': sum(stats['missing'].values()),
                'memory_mb': round(stats['memory_usage'], 2)
            },
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.astype(str).to_dict(),
            'preview': df.head(5).to_dict('records')
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/sanitize', methods=['POST'])
def sanitize():
    """Apply sanitization operations"""
    try:
        data = request.json
        filename = data.get('filename')
        operations = data.get('operations', [])

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        df = pd.read_csv(filepath)

        sanitizer = DataSanitizer(df)

        # Apply operations in order
        for op in operations:
            op_type = op.get('type')

            if op_type == 'remove_duplicates':
                sanitizer.remove_duplicates()

            elif op_type == 'handle_missing':
                strategy = op.get('strategy', 'drop')
                column = op.get('column')
                sanitizer.handle_missing_values(strategy=strategy, column=column)

            elif op_type == 'remove_outliers':
                method = op.get('method', 'iqr')
                threshold = op.get('threshold', 1.5)
                columns = op.get('columns')
                sanitizer.remove_outliers(method=method, columns=columns, threshold=threshold)

            elif op_type == 'convert_types':
                sanitizer.convert_data_types()

            elif op_type == 'clean_text':
                columns = op.get('columns')
                sanitizer.clean_text(columns=columns)

        # Save cleaned data
        cleaned_filename = f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        cleaned_filepath = os.path.join(app.config['UPLOAD_FOLDER'], cleaned_filename)
        sanitizer.df.to_csv(cleaned_filepath, index=False)

        return jsonify({
            'success': True,
            'cleaned_filename': cleaned_filename,
            'initial_stats': sanitizer.get_initial_stats(),
            'final_stats': sanitizer.get_final_stats(),
            'comparison': sanitizer.get_comparison(),
            'cleaning_log': sanitizer.cleaning_log,
            'preview': sanitizer.get_preview(10)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download(filename):
    """Download cleaned CSV file"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
