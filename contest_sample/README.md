# 🚀 AI Product Recommendation System

A comprehensive Flask-based web application for intelligent product recommendations powered by Machine Learning and Pandas.

## ✨ Features

### 1. **Interactive UI with Flask**
- Modern, responsive Bootstrap-based interface
- Dynamic filtering by category, price range, and rating
- Smooth navigation and user-friendly design
- Interactive tabs and collapsible sections

### 2. **Data Sanitizer (Pandas Cleaning)**
- Remove duplicate rows
- Handle missing values (drop, mean, median, forward-fill)
- Remove outliers (IQR and Z-score methods)
- Normalize numeric columns
- Clean text data (strip, lowercase)
- Comprehensive cleaning report

### 3. **AI Logic Recommendation Engine**
- Content-based recommendations using cosine similarity
- Price-based filtering and smart recommendations
- Rating-based product suggestions
- Combined smart recommendations based on budget, rating, and category
- Machine Learning with scikit-learn

### 4. **Automated Statistical Summary**
- Quick stats dashboard (rows, columns, memory usage)
- Numeric statistics (mean, median, std, min, max, quartiles)
- Categorical distribution analysis
- Missing values report
- Duplicate detection
- Data completeness indicator

### 5. **File Export Capability**
- Export cleaned data as CSV
- Export statistics report as TXT
- Export recommendations as JSON
- Export complete analysis report
- Download history and management

### 6. **Search Functionality**
- Full-text search across multiple columns
- Numeric range filtering
- Categorical value filtering
- Advanced filtering with multiple conditions
- Autocomplete suggestions
- Multi-column search

### 7. **Interactive Visualizations**
- Price distribution (Bar chart)
- Rating distribution (Line chart)
- Category distribution (Pie chart)
- Interactive Plotly charts
- Real-time chart rendering

## 📋 Project Structure

```
contest_sample/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── data_processor.py           # Data sanitization module
├── recommendation_engine.py    # AI recommendation logic
├── statistical_analyzer.py     # Statistical analysis
├── search_engine.py            # Search functionality
├── requirements.txt            # Python dependencies
├── data/
│   ├── sample_data.csv        # Sample dataset
│   ├── uploads/               # Uploaded files
│   └── exports/               # Exported files
├── static/
│   └── css/
│       └── style.css          # Custom styling
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── upload.html            # Upload page
    ├── analysis.html          # Analysis page
    ├── recommendations.html   # Recommendations page
    ├── export.html            # Export page
    └── error.html             # Error page
```

## 🛠️ Installation & Setup

### Step 1: Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 2: Install Dependencies

```bash
# Navigate to the contest_sample directory
cd contest_sample

# Install required packages
pip install -r requirements.txt
```

**Packages installed:**
- Flask 2.3.3 - Web framework
- pandas 2.0.3 - Data processing
- numpy 1.24.3 - Numerical computing
- scikit-learn 1.3.0 - Machine learning
- plotly 5.16.1 - Interactive visualizations
- python-dotenv 1.0.0 - Environment variables

### Step 3: Create Required Directories

```bash
# Directories are auto-created by the app, but you can manually create them:
mkdir -p data/uploads
mkdir -p data/exports
mkdir -p static/css
mkdir -p templates
```

## 🚀 Running the Application

### Start the Flask Server

```bash
# From the contest_sample directory
python app.py
```

You should see output like:
```
============================================================
AI PRODUCT RECOMMENDATION SYSTEM
============================================================
Starting Flask application...
Debug Mode: True
Upload Folder: /path/to/data/uploads
Export Folder: /path/to/data/exports

Access the application at: http://localhost:5000
============================================================
```

### Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

## 📖 User Guide

### 🏠 Home Page (`/`)
- Overview of features
- Quick navigation to all modules
- Information about the system

### 📤 Upload Data (`/upload`)
**Steps:**
1. Click "Upload Data" in navigation
2. Select your CSV file
3. Click "Upload & Process"
4. Data is automatically cleaned and validated

**CSV Format Requirements:**
```csv
name,category,price,rating
Product1,Electronics,999,4.5
Product2,Books,599,4.2
```

### 📊 Analysis (`/analysis`)
**Features:**
- **Overview Tab**: Dataset summary, data completeness
- **Numeric Stats Tab**: Mean, median, std dev, quartiles
- **Categories Tab**: Unique values, distributions
- **Charts Tab**: Price, rating, and category visualizations

### ⭐ Recommendations (`/recommendations`)
**How to Use:**
1. Adjust filters:
   - Budget (₹)
   - Category
   - Minimum Rating
2. Click "Get Recommendations"
3. View smart picks, budget-friendly, and highly-rated products

**Search:**
- Enter product name or keyword
- View filtered results

### 📥 Export (`/export`)
**Export Options:**
- **Cleaned Data (CSV)**: Your processed dataset
- **Statistics Report (TXT)**: Analysis summary
- **Recommendations (JSON)**: AI suggestions
- **Complete Report (TXT)**: Full analysis

## 🔬 Sample Dataset

The system comes with a pre-loaded sample dataset containing:
- **25 Products** across 2 categories
- **Electronics**: Headphones, Cables, Monitors, etc.
- **Books**: Programming, ML, Data Science guides

**Columns:**
- name: Product name
- category: Product category
- price: Product price (₹)
- rating: Customer rating (0-5)
- reviews: Number of reviews
- in_stock: Availability

## 🧠 How the AI Works

### Recommendation Engine
```
1. Content-Based Filtering
   → Calculates similarity between products using cosine similarity
   → Recommends similar products to user preferences

2. Price-Based Filtering
   → Filters products within budget
   → Optionally by category
   → Sorts by rating and price

3. Rating-Based Filtering
   → Recommends top-rated products
   → Filters by minimum rating threshold

4. Smart Recommendations
   → Combines all strategies
   → Uses ML algorithms for scoring
   → Returns best matches
```

### Data Cleaning Process
```
1. Remove Duplicates → Delete identical rows
2. Handle Missing Values → Fill or remove
3. Remove Outliers → Identify extreme values
4. Normalize Data → Scale to 0-1 range
5. Clean Text → Strip whitespace, convert to lowercase
```

## 📊 Sample API Endpoints

### Get Statistics
```
GET /api/stats
Response: JSON with stats data
```

### Get Recommendations
```
GET /api/recommendations?budget=5000&category=Electronics&min_rating=4.0
Response: JSON with recommended products
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Change port in app.py
```python
# Line 377 in app.py
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001
```

### Issue: Data not loading
**Solution:** Check data/sample_data.csv exists and is not empty

### Issue: Charts not displaying
**Solution:** Check browser console for JavaScript errors. Ensure Plotly CDN is accessible.

## 🔒 Security Notes

- File uploads are validated
- Maximum file size: 16MB
- All filenames are sanitized
- No sensitive data in exports
- CSRF protection enabled (Flask default)

## 📈 Performance Tips

1. **Large datasets**: Use filtering before analysis
2. **Multiple exports**: Check export history for previous files
3. **Recommendations**: Set reasonable budget ranges
4. **Charts**: Charts render faster with smaller datasets

## 🎯 Testing the System

### Quick Test Flow
1. Go to http://localhost:5000
2. Click "Analysis" → View statistics of sample data
3. Click "Recommendations" → Adjust filters and get suggestions
4. Click "Export" → Download CSV of cleaned data
5. Click "Upload Data" → Upload your own CSV

### Sample CSV for Testing
```csv
name,category,price,rating
Laptop,Electronics,45000,4.8
Mouse,Electronics,800,4.5
Python Book,Books,599,4.7
Monitor,Electronics,12000,4.4
Keyboard,Electronics,3500,4.6
```

## 🔧 Configuration

Edit `config.py` to customize:
```python
UPLOAD_FOLDER = 'path/to/uploads'
EXPORT_FOLDER = 'path/to/exports'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # File size limit
```

## 📝 Example Workflows

### Workflow 1: Analyze Your Products
1. Prepare CSV (name, category, price, rating)
2. Upload via `Upload Data`
3. View analysis in `Analysis` tab
4. Export statistics
5. Share report with team

### Workflow 2: Get Product Recommendations
1. Set budget ₹3000
2. Select category "Electronics"
3. Set minimum rating 4.0
4. Click "Get Recommendations"
5. View smart picks and export as JSON

### Workflow 3: Search & Filter
1. Go to `Recommendations`
2. Use search box at bottom
3. Enter product name or keyword
4. View filtered results
5. Combine with filter controls

## 🌟 Key Highlights

✅ **Production-Ready**: Proper error handling and validation
✅ **Scalable**: Can handle thousands of products
✅ **User-Friendly**: Clean, intuitive interface
✅ **Well-Organized**: Modular code structure
✅ **Documented**: Comprehensive docstrings
✅ **Secure**: Input sanitization and validation
✅ **Responsive**: Works on desktop, tablet, mobile

## 📚 Technologies Used

- **Backend**: Flask, Python
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-learn
- **Frontend**: Bootstrap 5, Plotly
- **Database**: CSV (file-based)

## 🤝 Code Quality

- PEP 8 compliant
- Type hints included
- Comprehensive docstrings
- Error handling throughout
- Logging and debugging support

## 📄 License

Open source - Feel free to use and modify

## 👨‍💻 Development Notes

### Adding Custom Features

1. **New Analysis Type**:
   - Add method to `StatisticalAnalyzer` class
   - Create route in `app.py`
   - Update template

2. **New Filter**:
   - Update `SearchEngine.advanced_filter()`
   - Modify HTML form in templates
   - Update route handler

3. **New Export Format**:
   - Add export method in `app.py`
   - Create button in export.html
   - Implement file generation

## 🚀 Next Steps

1. Read through the code to understand structure
2. Test with sample data
3. Upload your own CSV
4. Generate recommendations
5. Export and analyze results
6. Customize features as needed

## 📞 Support

If you encounter issues:
1. Check troubleshooting section above
2. Verify all requirements are installed
3. Check data format matches CSV requirements
4. Review Flask error messages in console
5. Restart Flask server

## 🎉 Enjoy Using the System!

The AI Product Recommendation System is ready to use. Start exploring your data and get intelligent product recommendations!

For any questions or improvements, refer to the code documentation.

**Happy Analyzing! 📊**
