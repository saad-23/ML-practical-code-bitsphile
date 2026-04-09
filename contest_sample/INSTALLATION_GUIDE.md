# 📚 STEP-BY-STEP INSTALLATION & RUNNING GUIDE

## Quick Start (5 minutes)

### Prerequisites
- Windows/Mac/Linux with Python 3.7+
- Command line/Terminal access

### Steps

#### Step 1: Install Dependencies (First Time Only)
```bash
# Navigate to the project directory
cd e:\BitsPhile-Courses\AI-ML-DL\python-practical\contest_sample

# Install Python packages in one command
pip install -r requirements.txt
```

**What gets installed:**
- Flask (Web framework)
- Pandas (Data processing)
- NumPy (Numerical computing)
- scikit-learn (Machine learning)
- Plotly (Visualizations)

**Expected output:**
```
Successfully installed Flask-2.3.3 pandas-2.0.3 numpy-1.24.3 scikit-learn-1.3.0 plotly-5.16.1
```

---

#### Step 2: Verify Installation
```bash
# Test that everything is installed correctly
python -c "import flask, pandas, numpy, sklearn, plotly; print('All packages installed successfully!')"
```

---

#### Step 3: Start the Application
```bash
# From inside contest_sample directory
python app.py
```

**You should see:**
```
============================================================
AI PRODUCT RECOMMENDATION SYSTEM
============================================================
Starting Flask application...
Debug Mode: True
Upload Folder: E:\path\to\data\uploads
Export Folder: E:\path\to\data\exports

Access the application at: http://localhost:5000
============================================================
```

---

#### Step 4: Open in Browser
- Click the link or manually type: **http://localhost:5000**
- You should see the colorful home page with 4 feature cards

---

## Detailed Walkthrough

### Complete Directory Structure
```
contest_sample/
├── app.py                              # Main application (11KB)
├── config.py                           # Configuration
├── data_processor.py                   # Data cleaning
├── recommendation_engine.py            # AI recommendations
├── statistical_analyzer.py             # Statistics
├── search_engine.py                    # Search functionality
├── requirements.txt                    # Dependencies
├── README.md                           # Full documentation
├── data/
│   ├── sample_data.csv                # Pre-loaded sample (25 products)
│   ├── uploads/                       # Your uploaded CSVs
│   └── exports/                       # Downloaded files
├── static/
│   └── css/
│       └── style.css                  # Beautiful styling
└── templates/
    ├── base.html                      # Base layout
    ├── index.html                     # Home page
    ├── upload.html                    # Upload page
    ├── analysis.html                  # Analysis & charts
    ├── recommendations.html           # Recommendations
    ├── export.html                    # Export page
    └── error.html                     # Error handling
```

---

### Installation Methods

#### Method A: Automatic (Recommended)
```bash
cd contest_sample
pip install -r requirements.txt
python app.py
```

#### Method B: Individual Packages
```bash
cd contest_sample
pip install Flask==2.3.3
pip install pandas==2.0.3
pip install numpy==1.24.3
pip install scikit-learn==1.3.0
pip install plotly==5.16.1
pip install python-dotenv==1.0.0
python app.py
```

#### Method C: Using Virtual Environment (Advanced)
```bash
cd contest_sample
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

---

## Testing After Installation

### Test 1: Sample Data Test
1. Keep Flask server running
2. Go to http://localhost:5000
3. Navigate to **Analysis** page
4. You should see stats for 25 products
5. Charts should display (Price, Rating, Category)

### Test 2: Recommendation Test
1. Go to **Recommendations** page
2. Set Budget: ₹5000
3. Select Category: Any (leave blank)
4. Set Minimum Rating: 4.0
5. Click "Get Recommendations"
6. Should show 3-5 product suggestions

### Test 3: Export Test
1. Go to **Export** page
2. Click "Download CSV"
3. Check your downloads folder
4. File should be named: `cleaned_data_YYYYMMDD_HHMMSS.csv`

### Test 4: Search Test
1. Go to **Recommendations** page
2. In search box, type: "Laptop" or "Electronics"
3. Click Search
4. Results should appear below

---

## Troubleshooting

### Problem 1: "ModuleNotFoundError: No module named 'flask'"
**Cause:** Packages not installed
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem 2: "Address already in use" (Port 5000)
**Cause:** Another app using port 5000
**Solution:** Edit app.py, change port number
```python
# Line at bottom of app.py:
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 instead
```

### Problem 3: "No module named 'app'" when running
**Cause:** Not in correct directory
**Solution:**
```bash
# Make sure you're in the contest_sample folder
cd contest_sample
python app.py
```

### Problem 4: Charts not loading
**Cause:** Browser JavaScript issue
**Solution:**
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear browser cache
3. Try different browser (Chrome, Firefox)
4. Check browser console (F12) for errors

### Problem 5: Can't upload CSV
**Cause:** Wrong format or missing columns
**Solution:** CSV must have these columns:
```csv
name,category,price,rating
Product1,Electronics,999,4.5
```

### Problem 6: "Failed to load resource" errors
**Cause:** Static files not found
**Solution:**
1. Make sure you're in project root
2. Check static/ and templates/ folders exist
3. Restart Flask server

---

## Running the Full System

### Typical User Journey (10 minutes)

**Step 1: Start Server (1 min)**
```bash
python app.py
```

**Step 2: Home Page (30 sec)**
- Open http://localhost:5000
- Read the overview
- Click on features to explore

**Step 3: View Sample Data Analysis (2 min)**
- Click "Analysis" in navbar
- View Quick Stats section
- Check the 4 stat cards at top
- View charts in Charts tab

**Step 4: Get Recommendations (2 min)**
- Click "Recommendations"
- Adjust the filters on left:
  - Budget: Slide to ₹5000
  - Category: Select "Electronics"
  - Rating: Select "4.0 stars & up"
- Click "Get Recommendations"
- View Smart Picks and other recommendations

**Step 5: Search Products (1 min)**
- In Recommendations page
- Type in search box: "Headphones"
- Click Search
- View results

**Step 6: Download Data (2 min)**
- Click "Export" in navbar
- Click "Download CSV" button
- File saves to Downloads folder
- Can also download TXT, JSON, PDF reports

**Step 7: Upload Your Data (2 min)**
- Click "Upload Data"
- Select your CSV file
- Click "Upload & Process"
- Data is automatically cleaned
- Duplicates removed, missing values handled

---

## Using Your Own Data

### CSV Format Requirements
```csv
name,category,price,rating
Product A,Electronics,1000,4.5
Product B,Books,500,4.2
Product C,Electronics,2000,4.8
```

**Minimum columns needed:**
- At least one text column (name)
- At least one numeric column (price, rating)

**Optional columns:**
- category
- reviews
- in_stock
- description
- etc.

### Upload Steps
1. Click "Upload Data" in navbar
2. Click "Choose File"
3. Select your CSV
4. Click "Upload & Process"
5. System automatically:
   - Removes duplicates
   - Removes empty rows
   - Cleans text
   - Handles missing values
6. View stats in Analysis page

---

## Performance Tips

### For Large Datasets (1000+ rows)
- Filter before analyzing
- Use category filters in recommendations
- Set reasonable budget ranges
- Charts may load slower

### For Slow Computer
- Reduce chart updates
- Use smaller datasets for testing
- Close other applications
- Use different browser

### Optimize Flask Server
```python
# In app.py, change debug mode:
app.run(debug=False)  # Production mode, faster
```

---

## Advanced Features

### Using the Search Engine
```python
# You can use these filters in recommendations:
- Search by name/keyword
- Filter by price range
- Filter by category
- Filter by rating
- Combine multiple filters
```

### Recommendation Algorithm
```
Smart Recommendations use:
1. Budget constraint (price <= budget)
2. Rating threshold (rating >= min_rating)
3. Category filtering (if specified)
4. ML similarity scoring
5. Returns top N suggestions
```

### Statistical Analysis Includes
```
- Mean, Median, Std Dev
- Min, Max, Quartiles
- Missing value count
- Duplicate rows
- Data completeness %
- Distribution analysis
- Outlier detection
```

---

## Stopping the Server

### Stop Flask
```bash
# Press Ctrl+C in the terminal where Flask is running
```

You should see:
```
KeyboardInterrupt
```

That's it! The server is stopped.

---

## Getting Help

### Check Logs
- Flask prints errors to terminal
- Read error messages carefully
- Most issues are shown in terminal

### Common Error Solutions
1. **ImportError** → Missing package → `pip install -r requirements.txt`
2. **FileNotFoundError** → Wrong directory → `cd contest_sample`
3. **PortError** → Port in use → Change port in app.py
4. **BrokenPipeError** → Client disconnected → Normal, ignore

---

## Files Description

### Core Python Files
| File | Lines | Purpose |
|------|-------|---------|
| app.py | 380 | Main Flask application & all routes |
| config.py | 25 | Configuration settings |
| data_processor.py | 100+ | Pandas data cleaning |
| recommendation_engine.py | 150+ | ML recommendations |
| statistical_analyzer.py | 120+ | Statistical analysis |
| search_engine.py | 120+ | Search functionality |

### Data Files
| File | Size | Purpose |
|------|------|---------|
| sample_data.csv | <1KB | Pre-loaded example data |
| uploads/*.csv | Variable | User uploaded data |
| exports/*.csv/.json/.txt | Variable | Exported results |

### Template Files
| File | Purpose |
|------|---------|
| base.html | Navigation & layout |
| index.html | Home page |
| upload.html | File upload |
| analysis.html | Data stats & charts |
| recommendations.html | AI suggestions |
| export.html | Download page |
| error.html | Error pages |

### Static Files
| File | Purpose |
|------|---------|
| style.css | Beautiful styling |
| Plotly CDN | Interactive charts |
| Bootstrap CDN | Responsive design |

---

## Features Checklist

✅ Interactive Flask UI
✅ Dynamic filtering (category, price, rating)
✅ Data sanitization (duplicates, missing values, outliers)
✅ AI recommendation engine (ML-based)
✅ Statistical summary (mean, median, std, min, max)
✅ File export (CSV, JSON, TXT, PDF)
✅ Search functionality (text, range, categorical)
✅ Interactive visualizations (Plotly charts)
✅ Beautiful responsive design (Bootstrap)
✅ Automatic data cleaning
✅ API endpoints for integration
✅ Error handling & validation
✅ Session management
✅ Download management

---

## What's Included

### Sample Dataset (25 Products)
```
Electronics (13 items):
- Wireless Headphones, USB-C Cable, Laptop Stand, Keyboard
- LED Monitor, Wireless Mouse, Phone Stand, Desk Lamp
- HDMI Cable, Portable Charger, Microphone, Webcam,etc.

Books (12 items):
- Python Guide, ML Basics, Data Science Handbook
- Web Development, AI Applications, Advanced Python, etc.
```

### Pre-built Features
- 7 Flask routes (home, upload, analysis, recommendations, export, API)
- 4 major modules (data processing, ML, stats, search)
- 7 HTML templates with responsive design
- Custom CSS styling
- Plotly interactive charts
- Bootstrap UI framework

---

## Next Steps After Installation

1. **Explore the UI**: Click through all pages
2. **Test Features**: Try each button and filter
3. **Upload Your Data**: Use your own CSV
4. **Customize**: Modify colors, text, or features
5. **Deploy**: Use in production (modify config.py)

---

## Quick Reference Card

```bash
# Install
pip install -r requirements.txt

# Run
python app.py

# Access
http://localhost:5000

# Stop
Ctrl+C

# Change Port
# Edit app.py, change port=5000 to port=5001
```

---

## Success Indicators

✅ Flask server starts without errors
✅ Browser opens http://localhost:5000
✅ Homepage displays with 4 feature cards
✅ Analysis page shows statistics
✅ Recommendations generate suggestions
✅ Export downloads files
✅ Search finds products
✅ Charts display properly
✅ No console errors

---

## You're All Set! 🎉

Your complete AI-powered product recommendation system is ready to use!

For detailed feature documentation, see **README.md**

Happy analyzing! 📊
