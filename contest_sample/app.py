"""
AI Product Recommendation System
A Flask-based web application for intelligent product recommendations
"""
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from config import Config, DevelopmentConfig
from data_processor import DataProcessor
from recommendation_engine import RecommendationEngine
from statistical_analyzer import StatisticalAnalyzer
from search_engine import SearchEngine

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Global session state
session_data = {
    'df': None,
    'cleaned_df': None,
    'original_file': None,
    'recommendations': None,
    'search_results': None
}

def load_sample_data():
    """Load sample data from CSV"""
    sample_path = os.path.join(os.path.dirname(__file__), 'data', 'sample_data.csv')
    if os.path.exists(sample_path):
        return pd.read_csv(sample_path)
    return None

# Initialize with sample data
session_data['df'] = load_sample_data()
session_data['cleaned_df'] = session_data['df'].copy() if session_data['df'] is not None else None

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload and process CSV files"""
    current_file = None

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('upload'))

        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('upload'))

        if not file.filename.lower().endswith('.csv'):
            flash('Please upload a CSV file', 'error')
            return redirect(url_for('upload'))

        try:
            # Save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Load and process data
            df = pd.read_csv(filepath)

            # Data validation
            if df.empty:
                flash('CSV file is empty', 'error')
                return redirect(url_for('upload'))

            # Apply automatic cleaning
            processor = DataProcessor(df)
            processor.remove_duplicates()
            processor.handle_missing_values(strategy='drop')
            processor.clean_text_columns()

            # Update session
            session_data['df'] = df
            session_data['cleaned_df'] = processor.get_data()
            session_data['original_file'] = {
                'name': filename,
                'rows': len(df),
                'cols': len(df.columns)
            }

            flash(f'File uploaded successfully! ({len(df)} rows, {len(df.columns)} columns)', 'success')
            return redirect(url_for('upload'))

        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'error')
            return redirect(url_for('upload'))

    if session_data['original_file']:
        current_file = session_data['original_file']

    return render_template('upload.html', current_file=current_file)

@app.route('/analysis')
def analysis():
    """Data analysis and statistics"""
    if session_data['cleaned_df'] is None:
        flash('Please upload data first', 'error')
        return redirect(url_for('upload'))

    df = session_data['cleaned_df']
    analyzer = StatisticalAnalyzer(df)
    stats = analyzer.get_quick_stats()

    # Calculate missing values count
    missing_count = df.isnull().sum().sum()
    data_completeness = (1 - missing_count / (len(df) * len(df.columns))) * 100 if len(df) * len(df.columns) > 0 else 100

    # Prepare chart data
    price_chart_data = None
    rating_chart_data = None
    category_chart_data = None

    if 'price' in df.columns:
        price_bins = pd.cut(df['price'], bins=10).value_counts().sort_index()
        price_chart_data = {
            'bins': [str(interval) for interval in price_bins.index],
            'counts': price_bins.values.tolist()
        }

    if 'rating' in df.columns:
        rating_counts = df['rating'].value_counts().sort_index()
        rating_chart_data = {
            'ratings': rating_counts.index.tolist(),
            'counts': rating_counts.values.tolist()
        }

    if 'category' in df.columns:
        cat_counts = df['category'].value_counts()
        category_chart_data = {
            'categories': cat_counts.index.tolist(),
            'counts': cat_counts.values.tolist()
        }

    return render_template('analysis.html',
                         stats=stats,
                         missing_count=int(missing_count),
                         data_completeness=int(data_completeness),
                         price_chart_data=price_chart_data,
                         rating_chart_data=rating_chart_data,
                         category_chart_data=category_chart_data)

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    """AI-powered recommendations"""
    if session_data['cleaned_df'] is None:
        flash('Please upload data first', 'error')
        return redirect(url_for('upload'))

    df = session_data['cleaned_df']
    engine = RecommendationEngine(df)

    # Get unique categories
    categories = df['category'].unique().tolist() if 'category' in df.columns else []

    recommendations = None
    search_results = None

    if request.method == 'POST':
        if request.path == '/recommendations':
            # Get recommendations
            budget = float(request.form.get('budget', 5000))
            category = request.form.get('category') or None
            min_rating = float(request.form.get('min_rating', 0))

            recommendations = engine.smart_recommendation(
                budget=budget,
                preferred_rating=min_rating,
                category=category,
                top_n=5
            )

            session_data['recommendations'] = recommendations

    # Check for search request
    if 'search_form' in request.form or request.path == '/search':
        search_query = request.form.get('search_query') or request.args.get('search_query', '')
        if search_query:
            searcher = SearchEngine(df)
            results_df = searcher.search(search_query)
            search_results = results_df.to_dict('records') if not results_df.empty else []
            session_data['search_results'] = search_results

    return render_template('recommendations.html',
                         categories=categories,
                         recommendations=recommendations or session_data['recommendations'],
                         search_results=search_results)

@app.route('/search', methods=['POST'])
def search():
    """Search functionality"""
    return recommendations()

@app.route('/export', methods=['GET'])
def export():
    """Export page"""
    exports = []
    export_folder = app.config['EXPORT_FOLDER']

    if os.path.exists(export_folder):
        for filename in os.listdir(export_folder):
            filepath = os.path.join(export_folder, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                size_str = f"{size / 1024:.1f} KB" if size > 1024 else f"{size} B"
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                exports.append({
                    'name': filename,
                    'type': filename.split('.')[-1].upper(),
                    'size': size_str,
                    'date': mod_time.strftime('%Y-%m-%d %H:%M'),
                    'url': f'/download/{filename}'
                })

    return render_template('export.html', exports=exports)

@app.route('/export/csv', methods=['POST'])
def export_csv():
    """Export cleaned data as CSV"""
    if session_data['cleaned_df'] is None:
        flash('No data to export', 'error')
        return redirect(url_for('export'))

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'cleaned_data_{timestamp}.csv'
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)

        session_data['cleaned_df'].to_csv(filepath, index=False)
        flash(f'Data exported successfully: {filename}', 'success')

        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('export'))

@app.route('/export/stats', methods=['POST'])
def export_stats():
    """Export statistical summary"""
    if session_data['cleaned_df'] is None:
        flash('No data to export', 'error')
        return redirect(url_for('export'))

    try:
        analyzer = StatisticalAnalyzer(session_data['cleaned_df'])
        report = analyzer.get_summary_report()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'statistics_report_{timestamp}.txt'
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)

        with open(filepath, 'w') as f:
            f.write(report)

        flash(f'Statistics exported: {filename}', 'success')
        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('export'))

@app.route('/export/recommendations', methods=['POST'])
def export_recommendations():
    """Export recommendations as JSON"""
    if session_data['recommendations'] is None:
        flash('Generate recommendations first', 'error')
        return redirect(url_for('recommendations'))

    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'recommendations_{timestamp}.json'
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)

        # Convert recommendations to JSON-serializable format
        recs_data = {}
        for key, value in session_data['recommendations'].items():
            if isinstance(value, list):
                recs_data[key] = [dict(item) if hasattr(item, '__dict__') else item for item in value]
            else:
                recs_data[key] = value

        with open(filepath, 'w') as f:
            json.dump(recs_data, f, indent=4, default=str)

        flash(f'Recommendations exported: {filename}', 'success')
        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('export'))

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    """Export complete report as PDF (simplified text-based)"""
    if session_data['cleaned_df'] is None:
        flash('No data to export', 'error')
        return redirect(url_for('export'))

    try:
        analyzer = StatisticalAnalyzer(session_data['cleaned_df'])
        report = analyzer.get_summary_report()

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'complete_report_{timestamp}.txt'
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)

        with open(filepath, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("AI PRODUCT RECOMMENDATION SYSTEM - COMPLETE REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(report)

            if session_data['recommendations']:
                f.write("\n" + "=" * 60 + "\n")
                f.write("RECOMMENDATIONS\n")
                f.write("=" * 60 + "\n")
                f.write(str(session_data['recommendations']))

        flash(f'Report exported: {filename}', 'success')
        return send_file(filepath, as_attachment=True, download_name=filename)

    except Exception as e:
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('export'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download exported file"""
    filepath = os.path.join(app.config['EXPORT_FOLDER'], secure_filename(filename))
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    flash('File not found', 'error')
    return redirect(url_for('export'))

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    if session_data['cleaned_df'] is None:
        return jsonify({'error': 'No data loaded'}), 400

    analyzer = StatisticalAnalyzer(session_data['cleaned_df'])
    stats = analyzer.get_quick_stats()
    return jsonify(stats)

@app.route('/api/recommendations')
def api_recommendations():
    """API endpoint for recommendations"""
    if session_data['cleaned_df'] is None:
        return jsonify({'error': 'No data loaded'}), 400

    budget = float(request.args.get('budget', 5000))
    category = request.args.get('category') or None
    min_rating = float(request.args.get('min_rating', 0))

    engine = RecommendationEngine(session_data['cleaned_df'])
    recs = engine.smart_recommendation(budget, min_rating, category, 5)

    # Convert to JSON-serializable format
    return jsonify(json.loads(json.dumps(recs, default=str)))

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('error.html', code=404, message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('error.html', code=500, message='Internal server error'), 500

# ============================================================================
# CONTEXT PROCESSORS
# ============================================================================

@app.context_processor
def inject_config():
    """Inject config into templates"""
    return dict(app_name='AI Recommendation System')

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("AI PRODUCT RECOMMENDATION SYSTEM")
    print("=" * 60)
    print(f"Starting Flask application...")
    print(f"Debug Mode: {app.config['DEBUG']}")
    print(f"Upload Folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Export Folder: {app.config['EXPORT_FOLDER']}")
    print("\nAccess the application at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
