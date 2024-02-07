# Last Update on 7-02-24
import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time  


#csv file save process 
def create_file_path(user_keywords):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f'linkedin-jobs-{user_keywords}-{timestamp}.csv'
    return file_path


#Filter process compay name which its repeted
def create_filtered_file_path(user_keywords):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = f'filtered-linkedin-jobs-{user_keywords}-{timestamp}.csv'
    return file_path

#removing the company name which its been repeted more than ones 
def remove_duplicates_and_save(user_keywords, timestamp):
    original_file_path = f'linkedin-jobs-{user_keywords}-{timestamp}.csv'
    existing_companies = set()
    filtered_records = []


    with open(original_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        filtered_records.append(header)

        for row in reader:
            if row[1] not in existing_companies:
                filtered_records.append(row)
                existing_companies.add(row[1])

    filtered_file_path = f'filtered-linkedin-jobs-{user_keywords}-{timestamp}.csv'
    with open(filtered_file_path, 'w', encoding='utf-8', newline='') as filtered_file:
        writer = csv.writer(filtered_file)
        writer.writerows(filtered_records)

def linkedin_scraper(webpage, keywords, file_path, page_number=0):
    records_count = 0

    while records_count < 50:
        next_page = f"{webpage}&keywords={keywords}&start={page_number * 25}"


        try:
            response = requests.get(next_page)
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
           
            if response.status_code == 429:
                print("Rate limit exceeded. Waiting for a longer while.")
                time.sleep(60)
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
                
                if records_count == 0:
                    writer.writerow(['Job Title', 'Company', 'Location', 'Link'])  
                writer.writerow([job_title, job_company, job_location, job_link])

            records_count += 1
            if records_count == 50:
                break

        print(f'Data updated. Total records: {records_count}')
        page_number += 1
        
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

if 1 <= user_filter <= 4:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = create_file_path(user_keywords)
    linkedin_scraper(job_filters[user_filter].format(user_keywords, user_location), user_keywords, file_path)
    remove_duplicates_and_save(user_keywords, timestamp)
else:
    print("Invalid filter value. Please enter a value between 1 and 4.")
