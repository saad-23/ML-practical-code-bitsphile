# Data Sanitizer - Professional Data Cleaning Tool

A comprehensive, interactive Flask-based data cleaning application powered by Pandas. Perform advanced data sanitization with a modern, intuitive web interface.

## Features

### 🔧 Core Cleaning Operations

1. **Remove Duplicates**
   - Identifies and removes completely identical rows from datasets
   - Preserves data integrity while reducing dataset size

2. **Handle Missing Values**
   - Drop rows/columns with NaN values
   - Fill with statistical measures (mean, median, forward fill)
   - Smart handling of missing data across numeric and text columns

3. **Remove Outliers**
   - IQR (Interquartile Range) detection
   - Z-Score based statistical outlier removal
   - Configurable threshold values
   - Automatic numeric column detection

4. **Auto-Convert Data Types**
   - Intelligent type inference (numeric, datetime, categorical)
   - Reduces memory footprint
   - Improves data consistency

5. **Clean Text Columns**
   - Remove leading/trailing whitespace
   - Convert to lowercase for consistency
   - Remove extra spaces
   - Standardize text data

### 📊 Analytics & Reporting

- **Live Data Preview**: See your data before and after cleaning
- **Comprehensive Statistics**: Rows, columns, duplicates, missing values, memory usage
- **Cleaning Report**: Detailed log of all operations performed
- **Before/After Comparison**: Track exactly what changed during sanitization
- **Memory Savings**: Monitor file size reduction

### 🎨 User Interface

- Modern, responsive web interface
- Drag & drop file upload
- Step-by-step guided workflow
- Real-time statistics and data preview
- Visual comparison charts

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Create a virtual environment** (recommended):
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Open in browser**:
Navigate to `http://localhost:5000`

## Usage Guide

### Step 1: Upload Data
- Click the upload area or drag & drop a CSV file
- Maximum file size: 50MB
- Displays immediate statistics and preview

### Step 2: Review Preview
- Check your data statistics
- Row count, column count, duplicates, missing values
- View data sample

### Step 3: Select Cleaning Operations
Choose from available operations:
- ✓ Remove duplicates
- ✓ Handle missing values (with strategy selection)
- ✓ Remove outliers (with method selection)
- ✓ Auto-convert data types
- ✓ Clean text columns

### Step 4: Review Results
- See cleaning comparison report
- Check detailed operation log
- Preview cleaned data
- Download the sanitized CSV

## Project Structure

```
data-sanitizer/
├── app.py                    # Flask application & backend logic
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Main web interface
├── static/
│   └── app.js               # Frontend JavaScript
├── uploads/                 # Temporary data storage
└── README.md                # This file
```

## Technical Stack

- **Backend**: Flask 3.0.0
- **Data Processing**: Pandas 2.1.3, NumPy 1.24.3
- **Frontend**: Bootstrap 5.3.0, jQuery 3.6.0
- **Server**: Werkzeug 3.0.1

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main application page |
| POST | `/upload` | Upload CSV file |
| POST | `/sanitize` | Apply cleaning operations |
| GET | `/download/<filename>` | Download cleaned CSV |
| GET | `/health` | Health check |

## Data Sanitizer Class (Backend)

The `DataSanitizer` class provides all cleaning operations:

```python
from app import DataSanitizer
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Initialize sanitizer
sanitizer = DataSanitizer(df)

# Get initial stats
stats = sanitizer.get_initial_stats()

# Apply operations
sanitizer.remove_duplicates()
sanitizer.handle_missing_values(strategy='mean')
sanitizer.remove_outliers(method='iqr', threshold=1.5)
sanitizer.convert_data_types()
sanitizer.clean_text()

# Get results
cleaned_df = sanitizer.df
comparison = sanitizer.get_comparison()
log = sanitizer.cleaning_log

# Export
csv_data = sanitizer.to_csv()
```

## Example Operations

### Remove Duplicates
```python
sanitizer.remove_duplicates()
# Removes all rows that are exact duplicates
```

### Handle Missing Values (Mean)
```python
sanitizer.handle_missing_values(strategy='mean')
# Fills numeric columns with their mean value
```

### Remove Outliers (IQR Method)
```python
sanitizer.remove_outliers(method='iqr', threshold=1.5)
# Uses IQR of 1.5 * (Q3-Q1) to detect outliers
```

### Auto-Convert Types
```python
sanitizer.convert_data_types()
# Automatically detects and converts columns to appropriate types
```

### Clean Text
```python
sanitizer.clean_text()
# Removes extra spaces, converts to lowercase
```

## Performance Notes

- **File Size Limit**: 50MB (configurable in app.config)
- **Processing**: Real-time for files < 10MB
- **Memory**: Efficient dataframe operations with Pandas
- **Storage**: Temporary files cleaned on server restart

## Configuration

Edit `app.py` to customize:

```python
app.config['UPLOAD_FOLDER'] = 'uploads'  # Upload directory
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Max file size
```

## Troubleshooting

### "Only CSV files are supported"
- Ensure your file is in CSV format (.csv extension)
- Try opening and re-saving in a spreadsheet application

### "File size exceeds limit"
- Split your CSV into smaller files
- Adjust `MAX_CONTENT_LENGTH` in app.py

### Missing values not handled correctly
- Check your missing value strategy in Step 3
- Use 'drop' to remove rows with NaN
- Use 'mean' or 'median' to fill numeric columns

### Data type conversion issues
- The auto-conversion uses heuristics (80% threshold)
- Manually clean ambiguous columns in Excel first

## Advanced Usage

### Programmatic API

```python
from app import app, DataSanitizer
import pandas as pd

with app.app_context():
    df = pd.read_csv('raw_data.csv')
    sanitizer = DataSanitizer(df)

    # Chain operations
    sanitizer.remove_duplicates()
    sanitizer.handle_missing_values(strategy='median')
    sanitizer.remove_outliers(method='zscore', threshold=3)

    # Export
    sanitizer.df.to_csv('cleaned_data.csv', index=False)
```

## Best Practices

1. **Always Review**: Check the preview before downloading
2. **Backup**: Keep original files safe
3. **Strategy Selection**: Choose appropriate missing value strategies
4. **Outlier Threshold**: Adjust based on your data distribution
5. **Text Cleaning**: Use when working with categorical/address data
6. **Type Conversion**: Verify auto-detected types before proceeding

## Contributing

To extend functionality, edit the `DataSanitizer` class:

```python
class DataSanitizer:
    def custom_operation(self, **kwargs):
        """Add your custom operation here"""
        self.cleaning_log.append({
            'action': 'Custom operation',
            'details': kwargs
        })
```

## License

This project is provided as-is for data cleaning and analysis purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Flask & Pandas documentation
3. Inspect browser console for JavaScript errors
4. Check server logs for backend errors

## Future Enhancements

- [ ] PostgreSQL/MySQL database integration
- [ ] Excel file support
- [ ] Advanced statistical imputation (KNN, Multiple imputation)
- [ ] Custom regex pattern cleaning
- [ ] Data profiling reports
- [ ] Batch processing
- [ ] Scheduling and automation

---

**Version**: 1.0.0
**Last Updated**: 2024
**Author**: Data Sanitizer Team
