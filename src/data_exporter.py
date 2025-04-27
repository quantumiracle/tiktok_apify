"""
Data Exporter Module - Exports processed data to files
"""

import csv
import json
import logging
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataExporter:
    """
    Exports the final, filtered influencer data to CSV or JSON files.
    """
    
    def __init__(self, output_dir: str = "./output_api"):
        """
        Initializes the DataExporter.
        
        Args:
            output_dir (str): Directory where output files will be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logger.info(f"Initialized DataExporter. Output directory: {self.output_dir}")

    def _write_csv(self, data: List[Dict[str, Any]], filename: str):
        """
        Writes data to a CSV file.
        """
        if not data:
            logger.warning(f"No data to write to CSV file: {filename}")
            return
            
        filepath = os.path.join(self.output_dir, filename)
        try:
            # Define headers based on the keys of the first item
            headers = list(data[0].keys())
            
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            logger.info(f"Successfully wrote {len(data)} records to CSV: {filepath}")
        except Exception as e:
            logger.error(f"Error writing CSV file {filepath}: {e}")

    def _write_json(self, data: List[Dict[str, Any]], filename: str):
        """
        Writes data to a JSON file.
        """
        if not data:
            logger.warning(f"No data to write to JSON file: {filename}")
            return
            
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, mode="w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            logger.info(f"Successfully wrote {len(data)} records to JSON: {filepath}")
        except Exception as e:
            logger.error(f"Error writing JSON file {filepath}: {e}")

    def export_data(self, data: List[Dict[str, Any]], base_filename: str, output_format: str = "csv"):
        """
        Exports the data to the specified format.
        
        Args:
            data (List[Dict[str, Any]]): The list of processed influencer data.
            base_filename (str): The base name for the output file (e.g., "topic_art" or "all_topics").
            output_format (str): The desired output format ("csv" or "json").
        """
        filename = f"{base_filename}.{output_format}"
        
        if output_format.lower() == "csv":
            self._write_csv(data, filename)
        elif output_format.lower() == "json":
            self._write_json(data, filename)
        else:
            logger.error(f"Unsupported output format: {output_format}. Please use 'csv' or 'json'.")

# Example usage (for testing purposes)
if __name__ == '__main__':
    # Setup basic logging
    logging.basicConfig(level=logging.INFO)
    
    # Example processed data
    example_data = [
        {
            "topic": "testing", "username": "testuser1", "profile_url": "url1", 
            "followers": 1000, "likes": 50000, 
            "bio": "This is my bio. Contact: test@example.com", 
            "email": "test@example.com", "has_email": True
        },
        {
            "topic": "testing", "username": "testuser3", "profile_url": "url3", 
            "followers": 500, "likes": 10000, 
            "bio": "Bio 3. Email me at user3@domain.net", 
            "email": "user3@domain.net", "has_email": True
        }
    ]
    
    exporter = DataExporter(output_dir="./test_output")
    
    # Export as CSV
    exporter.export_data(example_data, base_filename="test_export", output_format="csv")
    
    # Export as JSON
    exporter.export_data(example_data, base_filename="test_export", output_format="json")
    
    # Test empty data
    exporter.export_data([], base_filename="empty_export", output_format="csv")
    
    print(f"\nCheck the '{exporter.output_dir}' directory for output files.")
