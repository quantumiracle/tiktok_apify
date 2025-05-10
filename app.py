import gradio as gr
import os
import json
import tempfile
import sys
import pandas as pd
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

try:
    from src.tiktok_parser import TikTokParser
except ImportError:
    # If the import fails, we'll handle it in the app itself
    pass

def create_temp_config(api_token, results_per_hashtag, max_profiles, require_email, output_format="csv"):
    """Create a temporary config file with the provided settings."""
    config = {
        "apify_api_token": api_token,
        "tiktok_actor_id": "clockworks/tiktok-scraper",
        "profile_actor_id": "clockworks/tiktok-profile-scraper",
        "results_per_hashtag": results_per_hashtag,
        "max_profiles_per_topic": max_profiles,
        "require_email": require_email,
        "output_format": output_format,
        "output_dir": "./output"
    }
    
    # Create a temporary config file
    fd, temp_config_path = tempfile.mkstemp(suffix='.json')
    with os.fdopen(fd, 'w') as f:
        json.dump(config, f, indent=4)
    
    return temp_config_path

def parse_tiktok(api_token, topics_input, results_per_hashtag=20, max_profiles=20, require_email=True, progress=gr.Progress()):
    """
    Parse TikTok profiles based on topics and return results as a DataFrame and summary.
    """
    if not api_token:
        return None, "Error: Please provide an Apify API token."
    
    # Parse topics (comma or space separated)
    topics = [t.strip() for t in topics_input.replace(",", " ").split() if t.strip()]
    
    if not topics:
        return None, "Error: Please provide at least one topic/hashtag."
    
    try:
        # Import the TikTokParser class
        from src.tiktok_parser import TikTokParser
    except ImportError:
        return None, "Error: TikTok Parser module not found. Please ensure the repository is properly set up."
    
    progress(0, desc="Creating configuration")
    
    # Create a temporary config file
    config_path = create_temp_config(
        api_token, 
        results_per_hashtag, 
        max_profiles, 
        require_email
    )
    
    try:
        progress(0.1, desc="Initializing parser")
        parser = TikTokParser(config_path)
        
        progress(0.2, desc=f"Searching for profiles with topics: {', '.join(topics)}")
        results = parser.run(topics, progress_callback=lambda x: progress(0.2 + 0.7 * x, desc="Processing profiles"))
        
        # Convert results to a DataFrame
        all_profiles = []
        for topic, profiles in results.items():
            for profile in profiles:
                profile['topic'] = topic
                all_profiles.append(profile)
        
        if not all_profiles:
            return None, "No profiles found with the specified criteria."
        
        # Create DataFrame
        df = pd.DataFrame(all_profiles)
        
        # Save to CSV
        output_path = os.path.join(parser.output_dir, "tiktok_profiles.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        
        # Generate summary
        total_profiles = len(all_profiles)
        summary = f"Found {total_profiles} profiles across {len(topics)} topics.\n\n"
        
        for topic, profiles in results.items():
            summary += f"Topic: {topic} - Found {len(profiles)} profiles"
            if require_email:
                summary += " with email"
            summary += "\n"
            
            # Show sample profiles (up to 3)
            for i, profile in enumerate(profiles[:3]):
                if require_email:
                    summary += f"  - {profile['username']} ({profile['email']})\n"
                else:
                    summary += f"  - {profile['username']}\n"
                    
            if len(profiles) > 3:
                summary += f"  - ... and {len(profiles) - 3} more\n"
            summary += "\n"
        
        progress(1.0, desc="Completed")
        return output_path, summary
        
    except Exception as e:
        return None, f"Error: {str(e)}"
    finally:
        # Clean up the temporary config file
        try:
            os.remove(config_path)
        except:
            pass

def create_ui():
    """Create the Gradio UI."""
    with gr.Blocks(title="TikTok Influencer Parser") as demo:
        gr.Markdown("# TikTok Influencer Parser")
        gr.Markdown("""
        This tool finds TikTok influencers based on specific topics (hashtags), extracts their profile data, 
        and optionally filters for profiles that include an email address in their bio.
        
        Enter your [Apify API token](https://console.apify.com/settings/integrations) below to get started.
        """)
        
        with gr.Row():
            with gr.Column():
                api_token = gr.Textbox(label="Apify API Token", placeholder="Enter your Apify API token", type="password")
                topics = gr.Textbox(label="Topics/Hashtags", placeholder="art, food, technology (comma or space separated)")
                
                with gr.Row():
                    results_per_hashtag = gr.Slider(minimum=5, maximum=100, value=20, step=5, label="Results Per Hashtag")
                    max_profiles = gr.Slider(minimum=5, maximum=100, value=20, step=5, label="Max Profiles Per Topic")
                
                require_email = gr.Checkbox(label="Require Email in Bio", value=True)
                submit_btn = gr.Button("Find Influencers", variant="primary")
            
            with gr.Column():
                output_summary = gr.Textbox(label="Results Summary", lines=10)
                download_btn = gr.File(label="Download CSV Results")
        
        submit_btn.click(
            fn=parse_tiktok,
            inputs=[api_token, topics, results_per_hashtag, max_profiles, require_email],
            outputs=[download_btn, output_summary]
        )
        
        gr.Markdown("""
        ## How It Works
        
        This tool uses a hybrid approach with two Apify APIs:
        1. **TikTok Scraper API** for topic-based searching
        2. **TikTok Profile Scraper API** for detailed profile metrics
        
        The process:
        1. Searches for TikTok users associated with your specified hashtags
        2. Retrieves detailed profile information (followers, likes, bio, etc.)
        3. Optionally filters for profiles containing email addresses
        4. Provides results as a downloadable CSV file
        
        Please note that this process may take a few minutes depending on the number of topics and profiles.
        """)
    
    return demo

# Create and launch the app
demo = create_ui()

if __name__ == "__main__":
    demo.launch() 