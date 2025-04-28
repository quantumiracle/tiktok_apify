#!/usr/bin/env python3
"""
Web interface for the TikTok Parser
"""

import os
import json
import logging
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from markupsafe import Markup
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.tiktok_parser import TikTokParser

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # For flash messages and session

# Custom Jinja2 filter for handling newlines in bio text
@app.template_filter('nl2br')
def nl2br(value):
    if value:
        return Markup(value.replace('\n', '<br>'))
    return value

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Render the main page with the form."""
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    """Handle form submission and run the parser."""
    # Get form data
    topics = request.form.get('topics', '').strip().split(',')
    topics = [topic.strip() for topic in topics if topic.strip()]
    
    api_token = request.form.get('api_token', '').strip()
    results_per_hashtag = int(request.form.get('results_per_hashtag', 20))
    max_profiles = int(request.form.get('max_profiles', 20))
    require_email = request.form.get('require_email') == 'on'
    output_format = request.form.get('output_format', 'csv')
    
    # Validate inputs
    if not topics:
        flash('Please enter at least one topic', 'error')
        return redirect(url_for('index'))
    
    if not api_token:
        flash('Please enter your Apify API token', 'error')
        return redirect(url_for('index'))
    
    # Create a temporary config file
    config = {
        "apify_api_token": api_token,
        "tiktok_actor_id": "clockworks/tiktok-scraper",
        "profile_actor_id": "clockworks/tiktok-profile-scraper",
        "results_per_hashtag": results_per_hashtag,
        "max_profiles_per_topic": max_profiles,
        "require_email": require_email,
        "output_format": output_format,
        "output_dir": "./hybrid_output"
    }
    
    fd, temp_config_path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(config, f, indent=4)
    
    try:
        # Initialize and run the parser
        parser = TikTokParser(temp_config_path)
        results = parser.run(topics)
        
        # Store results in session for display
        session['results'] = {
            'topics': topics,
            'total_profiles': sum(len(profiles) for profiles in results.values()),
            'topic_results': {topic: len(profiles) for topic, profiles in results.items()},
            'output_dir': parser.output_dir,
            'output_format': output_format
        }
        
        # Store a sample of profiles for display
        sample_profiles = {}
        for topic, profiles in results.items():
            sample_profiles[topic] = profiles[:5]  # Show up to 5 profiles per topic
        
        session['sample_profiles'] = sample_profiles
        
        flash('Parsing completed successfully!', 'success')
        return redirect(url_for('results'))
        
    except Exception as e:
        logger.error(f"Error running TikTok parser: {e}")
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Clean up temporary config file
        try:
            os.remove(temp_config_path)
        except:
            pass

@app.route('/results')
def results():
    """Display the parsing results."""
    if 'results' not in session:
        flash('No results to display. Please run the parser first.', 'error')
        return redirect(url_for('index'))
    
    return render_template(
        'results.html',
        results=session['results'],
        sample_profiles=session.get('sample_profiles', {})
    )

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a result file."""
    return send_from_directory(
        os.path.abspath('./hybrid_output'),
        filename,
        as_attachment=True
    )

if __name__ == '__main__':
    # Ensure output directory exists
    os.makedirs('./hybrid_output', exist_ok=True)
    app.run(debug=True)
