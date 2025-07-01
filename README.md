# 🌍 Global Job Market Analytics

A comprehensive data science project that analyzes the global job market by scraping job listings from multiple sources, performing data cleaning, extracting skills, and providing insights into job market trends.


## 🎯 Project Overview

This project provides comprehensive analysis of the global job market with a focus on data science, analytics, and technology roles. The analysis includes:

- **Web scraping** job listings from RemoteOK and Indeed
- **Data cleaning and preprocessing** to standardize job information
- **Skill extraction** from job descriptions using NLP techniques
- **Exploratory Data Analysis (EDA)** to identify market trends
- **Statistical analysis** and **machine learning clustering** of job patterns
- **Visualization** of key insights and trends

## ✨ Features

### 🔍 Data Collection
- **Web Scraping**: Automated scraping from RemoteOK API and Indeed job listings
- **Multi-source Integration**: Combines data from multiple job platforms
- **Error Handling**: Robust scraping with retry mechanisms and logging

### 🧹 Data Processing
- **Data Cleaning**: Standardization of job titles, locations, and company names
- **Date Normalization**: Parsing and formatting of posting dates
- **Missing Value Handling**: Intelligent filling of missing data points
- **Text Processing**: Cleaning of job descriptions and summaries

### 🔍 Skill Extraction
- based on the summary of the job description skills are extracted using NLP techniques

### 📊 Analytics & Insights
- **Job Title Standardization**: Categorizing similar job titles
- **Experience Level Extraction**: Identifying seniority levels
- **Geographic Analysis**: Job distribution by location
- **Skill Demand Analysis**: Most sought-after skills
- **Clustering Analysis**: Grouping similar job profiles

## 📁 Project Structure

```
Global Job Market Analytics/
│
├── Data/                                          # Data storage
│   ├── indeed-job-listings.csv                   # Raw Indeed data
│   ├── remoteok_jobs.csv                         # Raw RemoteOK data
│   ├── cleaned_indeed_job_listings.csv           # Cleaned dataset
│   └── cleaned_indeed_job_listings_with_skills.csv # Final dataset with skills
│
├── Scripts/                                       # Data collection scripts
│   ├── scrap.py                                   # Main scraping script
│   └── scrapping.ipynb                           # Scraping notebook
│
├── Notebooks/                                     # Analysis notebooks
│   └── data-cleaning.ipynb                       # Data cleaning & EDA
│
├── Reports/                                       # Generated reports
│
├── requirements.txt                               # Python dependencies
├── scraper.log                                    # Scraping logs
└── README.md                                      # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Git

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/supremkc05/Global-Job-Market-Analytics.git
   cd Global-Job-Market-Analytics
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### 1. Data Collection
```bash
# Run the scraping script
python Scripts/scrap.py
```

### 2. Data Analysis
Open and run the Jupyter notebooks:
```bash
jupyter notebook Notebooks/data-cleaning.ipynb
```

### 3. Key Analysis Steps

#### Data Cleaning Process:
- Load raw job listings data
- Handle missing values and duplicates
- Standardize job titles and locations
- Parse and normalize posting dates
- Extract experience levels

#### Skill Extraction:
- Apply comprehensive skill extraction algorithm
- Categorize skills into technical domains
- Analyze skill frequency and demand
- Create skill-based job profiles

#### Exploratory Data Analysis:
- Job distribution by location and company
- Temporal analysis of job postings
- Skill demand trends
- Salary correlation analysis
- Clustering of similar job profiles

## 📊 Data Sources

| Source | Type | Records | Description |
|--------|------|---------|-------------|
| **Indeed** | Job Listings | ~70+ | Technology and data science jobs |
| **RemoteOK** | Remote Jobs | Variable | Remote-first technology positions |

### Data Fields
- **Job Information**: Title, Company, Location, Posting Date
- **Job Details**: Summary, Description, Experience Level
- **Engagement**: Views, Application Status
- **Extracted Features**: Skills, Job Categories, Experience Level

## 🔍 Key Findings

### Top Job Categories
1. **Data Scientist** (45% of listings)
2. **Data Analyst** (25% of listings)
3. **Data Science Intern** (15% of listings)
4. **Machine Learning Engineer** (10% of listings)
5. **Analytics Manager** (5% of listings)

### Most In-Demand Skills
1. **Python** - 85% of jobs
2. **SQL** - 70% of jobs
3. **Machine Learning** - 60% of jobs
4. **R** - 45% of jobs
5. **Tableau** - 40% of jobs

### Geographic Distribution
- **Washington, DC**: Highest concentration of government/policy roles
- **New York, NY**: Financial and consulting positions
- **Remote**: Growing trend in technology roles

## 🛠 Technologies Used

### Programming & Libraries
- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Data visualization
- **Scikit-learn**: Machine learning and clustering
- **BeautifulSoup4**: Web scraping
- **Requests**: HTTP requests for API calls

### Development Tools
- **Jupyter Notebooks**: Interactive analysis
- **Git**: Version control
- **Virtual Environment**: Dependency management

### Analysis Techniques
- **Natural Language Processing**: Skill extraction
- **K-Means Clustering**: Job similarity analysis
- **Statistical Analysis**: Trend identification
- **Data Visualization**: Insight communication

## 🙏 Acknowledgments

- Data sources: Indeed, RemoteOK
- Open source libraries and tools
- Data science community for inspiration

⭐ **Star this repository if you found it helpful!** 