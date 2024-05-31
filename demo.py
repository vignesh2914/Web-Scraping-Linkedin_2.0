import csv
import requests
from bs4 import BeautifulSoup

file_path = 'linkedin-jobs-python_developer.csv'

def linkedin_scraper(webpage, keywords, page_number):
    next_page = f"{webpage}&keywords={keywords}&start={page_number}"
    print(next_page)
    
    try:
        response = requests.get(next_page)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error in request: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        job_title = job.find(class_='').text.strip()
        job_company = job.find(class_='').text.strip()
        job_location = job.find(class_='').text.strip()  
        job_link = job.find(class_='')

        with open(file_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([job_title, job_company, job_location, job_link]) 
    print('Data updated')

    if page_number < 25:
        page_number += 25
        linkedin_scraper(webpage, keywords, page_number)
    else:
        print('File closed')

user_keywords = input("Enter the job keywords: ")

dynamic_url = f'{user_keyword},{location } your prefered linkedin url'
linkedin_scraper(dynamic_url, user_keywords, page_number=0)
