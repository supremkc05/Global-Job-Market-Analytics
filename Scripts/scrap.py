#!/usr/bin/env python3
"""
RemoteOK Job Scraper
A robust web scraper for RemoteOK job listings with comprehensive error handling
"""

import requests
import json
import csv
import time
import re
import sys
from datetime import datetime
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class RemoteOKScraper:
    """
    A comprehensive scraper for RemoteOK job listings
    """
    
    def __init__(self, delay: float = 1.0):
        """
        Initialize the scraper
        
        Args:
            delay: Delay between requests in seconds
        """
        self.base_url = "https://remoteok.com"
        self.api_url = "https://remoteok.com/api"
        self.delay = delay
        self.session = requests.Session()
        
        # Headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://remoteok.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })
        
        # Set timeout
        self.session.timeout = 30
    
    def make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """
        Make a request with retry logic
        
        Args:
            url: URL to request
            max_retries: Maximum number of retries
            
        Returns:
            Response object or None if failed
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Making request to {url} (attempt {attempt + 1}/{max_retries})")
                response = self.session.get(url)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:
                    # Rate limited
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.warning(f"HTTP {response.status_code}: {response.reason}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))
                    continue
                    
        return None
    
    def get_jobs(self, limit: int = 100) -> List[Dict]:
        """
        Fetch jobs from RemoteOK API
        
        Args:
            limit: Maximum number of jobs to fetch
            
        Returns:
            List of job dictionaries
        """
        try:
            logger.info("Fetching jobs from RemoteOK API...")
            response = self.make_request(self.api_url)
            
            if not response:
                logger.error("Failed to fetch data from API")
                return []
            
            # Parse JSON response
            try:
                jobs_data = response.json()
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                return []
            
            # Handle different response formats
            if not isinstance(jobs_data, list):
                logger.error(f"Unexpected response format: {type(jobs_data)}")
                return []
            
            # Filter out non-job entries (like legal notices)
            valid_jobs = []
            for item in jobs_data:
                if isinstance(item, dict) and 'id' in item and 'position' in item:
                    valid_jobs.append(item)
            
            # Apply limit
            if limit > 0:
                valid_jobs = valid_jobs[:limit]
            
            logger.info(f"Successfully fetched {len(valid_jobs)} jobs")
            return valid_jobs
            
        except Exception as e:
            logger.error(f"Unexpected error in get_jobs: {e}")
            return []
    
    def parse_salary(self, job_data: Dict) -> str:
        """
        Extract salary information from job data
        
        Args:
            job_data: Job dictionary
            
        Returns:
            Formatted salary string
        """
        try:
            salary_min = job_data.get('salary_min')
            salary_max = job_data.get('salary_max')
            
            # Convert to integers if they're strings
            if isinstance(salary_min, str) and salary_min.isdigit():
                salary_min = int(salary_min)
            if isinstance(salary_max, str) and salary_max.isdigit():
                salary_max = int(salary_max)
            
            if salary_min and salary_max:
                return f"${salary_min:,} - ${salary_max:,}"
            elif salary_min:
                return f"${salary_min:,}+"
            elif salary_max:
                return f"Up to ${salary_max:,}"
            else:
                return "Not specified"
                
        except (ValueError, TypeError) as e:
            logger.debug(f"Error parsing salary: {e}")
            return "Not specified"
    
    def parse_date(self, timestamp) -> str:
        """
        Convert timestamp to readable date
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            Formatted date string
        """
        try:
            if timestamp:
                # Handle both string and int timestamps
                if isinstance(timestamp, str):
                    timestamp = int(timestamp)
                return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        except (ValueError, TypeError, OSError) as e:
            logger.debug(f"Error parsing date: {e}")
        
        return "Not specified"
    
    def extract_experience_level(self, description: str, tags: List[str]) -> str:
        """
        Extract experience level from description and tags
        
        Args:
            description: Job description
            tags: List of tags
            
        Returns:
            Experience level string
        """
        try:
            # Combine text for analysis
            text_parts = [description or ""]
            if isinstance(tags, list):
                text_parts.extend(tags)
            elif isinstance(tags, str):
                text_parts.append(tags)
            
            text = " ".join(text_parts).lower()
            
            # Define keywords for each level
            entry_keywords = ['junior', 'entry', 'graduate', 'intern', '0-2 years', 'new grad', 'beginner']
            senior_keywords = ['senior', 'lead', 'principal', '5+ years', '7+ years', 'expert', 'architect']
            mid_keywords = ['mid', 'intermediate', '3-5 years', '2-4 years', 'experienced']
            
            if any(keyword in text for keyword in senior_keywords):
                return "Senior"
            elif any(keyword in text for keyword in entry_keywords):
                return "Entry"
            elif any(keyword in text for keyword in mid_keywords):
                return "Mid"
            else:
                return "Not specified"
                
        except Exception as e:
            logger.debug(f"Error extracting experience level: {e}")
            return "Not specified"
    
    def clean_text(self, text) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        try:
            # Convert to string
            text = str(text)
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', text)
            
            # Replace multiple whitespaces with single space
            text = re.sub(r'\s+', ' ', text)
            
            # Remove control characters
            text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
            
            # Normalize quotes for CSV
            text = text.strip().replace('"', '""')
            
            return text
            
        except Exception as e:
            logger.debug(f"Error cleaning text: {e}")
            return ""
    
    def process_jobs(self, jobs_data: List[Dict]) -> List[Dict]:
        """
        Process raw job data into structured format
        
        Args:
            jobs_data: List of raw job dictionaries
            
        Returns:
            List of processed job dictionaries
        """
        processed_jobs = []
        
        for i, job in enumerate(jobs_data):
            try:
                # Extract basic information
                job_id = job.get('id', f'job_{i}')
                position = job.get('position', 'Not specified')
                company = job.get('company', 'Not specified')
                location = job.get('location', 'Remote')
                
                # Handle tags
                tags = job.get('tags', [])
                if isinstance(tags, list):
                    tags_str = ', '.join(tags)
                elif isinstance(tags, str):
                    tags_str = tags
                else:
                    tags_str = str(tags) if tags else ""
                
                # Build job URL
                slug = job.get('slug', '')
                job_url = f"{self.base_url}/job/{job_id}"
                
                # Extract description
                description = job.get('description', '')
                
                # Process all fields
                processed_job = {
                    'job_title': self.clean_text(position),
                    'company_name': self.clean_text(company),
                    'location': self.clean_text(location),
                    'tags_skills': self.clean_text(tags_str),
                    'job_url': job_url,
                    'posted_date': self.parse_date(job.get('date')),
                    'salary': self.parse_salary(job),
                    'job_type': self.clean_text(job.get('type', 'Not specified')),
                    'experience_level': self.extract_experience_level(description, tags),
                    'industry_department': self.clean_text(tags_str),
                    'job_description': self.clean_text(description),
                    'application_deadline': 'Not specified',
                    'apply_url': job.get('apply_url', ''),
                    'company_logo': job.get('logo', ''),
                    'verified': job.get('verified', False),
                    'remote_ok_id': job_id,
                    'raw_date': job.get('date', ''),
                }
                
                processed_jobs.append(processed_job)
                
            except Exception as e:
                logger.error(f"Error processing job {i}: {e}")
                continue
        
        return processed_jobs
    
    def save_to_csv(self, jobs: List[Dict], filename: str = 'remoteok_jobs.csv') -> bool:
        """
        Save jobs data to CSV file
        
        Args:
            jobs: List of job dictionaries
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        if not jobs:
            logger.warning("No jobs to save")
            return False
        
        fieldnames = [
            'job_title', 'company_name', 'location', 'tags_skills', 'job_url',
            'posted_date', 'salary', 'job_type', 'experience_level',
            'industry_department', 'job_description', 'application_deadline',
            'apply_url', 'company_logo', 'verified', 'remote_ok_id', 'raw_date'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(jobs)
            
            logger.info(f"Successfully saved {len(jobs)} jobs to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return False
    
    def scrape_jobs(self, limit: int = 100, filename: str = 'remoteok_jobs.csv') -> Optional[List[Dict]]:
        """
        Main method to scrape jobs and save to CSV
        
        Args:
            limit: Maximum number of jobs to scrape
            filename: Output CSV filename
            
        Returns:
            List of processed jobs or None if failed
        """
        logger.info("Starting RemoteOK job scraping...")
        
        try:
            # Fetch raw job data
            raw_jobs = self.get_jobs(limit)
            
            if not raw_jobs:
                logger.error("No jobs fetched. Exiting.")
                return None
            
            # Add delay to be respectful
            time.sleep(self.delay)
            
            # Process jobs data
            processed_jobs = self.process_jobs(raw_jobs)
            
            if not processed_jobs:
                logger.error("No jobs processed. Exiting.")
                return None
            
            # Save to CSV
            if self.save_to_csv(processed_jobs, filename):
                logger.info(f"Scraping completed! {len(processed_jobs)} jobs saved to {filename}")
                return processed_jobs
            else:
                logger.error("Failed to save jobs to CSV")
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error in scrape_jobs: {e}")
            return None

def main():
    """
    Main function to run the scraper
    """
    print("🚀 RemoteOK Job Scraper")
    print("=" * 50)
    
    try:
        # Initialize scraper
        scraper = RemoteOKScraper(delay=1.0)
        
        # Get user input for number of jobs
        try:
            limit = int(input("Enter number of jobs to scrape (default 100): ") or "100")
        except ValueError:
            limit = 100
            print("Using default limit of 100 jobs")
        
        # Scrape jobs
        jobs = scraper.scrape_jobs(limit=limit, filename='remoteok_jobs.csv')
        
        if jobs:
            print(f"\n✅ Successfully scraped {len(jobs)} jobs!")
            print(f"📁 Data saved to 'remoteok_jobs.csv'")
            print(f"\n📊 Sample job:")
            print(f"   Title: {jobs[0]['job_title']}")
            print(f"   Company: {jobs[0]['company_name']}")
            print(f"   Location: {jobs[0]['location']}")
            print(f"   Posted: {jobs[0]['posted_date']}")
            print(f"   Salary: {jobs[0]['salary']}")
        else:
            print("❌ No jobs were scraped. Check the logs for errors.")
            
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        logger.error(f"Main function error: {e}")

if __name__ == "__main__":
    main()