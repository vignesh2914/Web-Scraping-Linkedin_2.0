#last updated on 2-2-24 ----->14:56
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time  

# CSV file save process
def create_file_path(user_keywords):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f'linkedin-jobs-{user_keywords}-{timestamp}.csv'
    return file_path

def linkedin_scraper(webpage, keywords, file_path, page_number=0):
    while True:
        # Number of pages to scrape from the webpage
        next_page = f"{webpage}&keywords={keywords}&start={page_number * 25}"
        print(next_page)

        try:
            response = requests.get(next_page)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting for a longer while.")
                time.sleep(60)  # Waiting time if hits error 429 it will wait for 60 seconds
                continue
            else:
                print(f"Error in request: {e}")
                return

        soup = BeautifulSoup(response.content, 'html.parser')

        jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        if not jobs:
            print("No more jobs found.")
            break  

        for job in jobs:
            job_title = job.find('h3', class_='base-search-card__title').text.strip()
            job_company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            job_location = job.find('span', class_='job-search-card__location').text.strip()
            job_link = job.find('a', class_='base-card__full-link')['href']

            with open(file_path, 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([job_title, job_company, job_location, job_link])

        print(f'Data updated. Total records: {page_number * 50 + len(jobs)}')

        page_number += 1

        #  sleep after every 50 records to avoid rate limiting
        if page_number % 50 == 0:
            print("Taking a break after fetching 50 records. Sleeping for 60 seconds.")
            time.sleep(60)

user_keywords = input("Enter the job keywords: ")
user_location = input("Enter the location: ")
user_filter = int(input("Enter the value (1-4): "))

job_filters = [
    None,
    'https://www.linkedin.com/jobs/search/?currentJobId=3810061572&keywords={}&location={}&origin=JOB_SEARCH_PAGE_LOCATION_HISTORY&refresh=true',
    'https://www.linkedin.com/jobs/search/?currentJobId=3799271140&f_TPR=r2592000&keywords={}&location={}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true',
    'https://www.linkedin.com/jobs/search/?currentJobId=3812840127&f_TPR=r604800&keywords={}&location={}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true',
    'https://www.linkedin.com/jobs/search/?currentJobId=3812840127&f_TPR=r86400&keywords={}&location={}&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'
]

file_path = create_file_path(user_keywords)

# Validation process for 1-4 number filter values
if 1 <= user_filter <= 4:
    linkedin_scraper(job_filters[user_filter].format(user_keywords, user_location), user_keywords, file_path)
else:
    print("Invalid filter value. Please enter a value between 1 and 4.")
