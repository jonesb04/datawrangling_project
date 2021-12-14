import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_url(job_title, location, webpage):
    url = f'https://www.indeed.com/jobs?q={job_title}&l={location}&start={webpage}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def get_job(html):
    title = ""
    divs = html.find_all('div', class_ = 'job_seen_beacon')
    for i in divs:
        body = i.find('tbody')
        tr = body.find('tr')
        try:
            for j in tr.find_all('h2', {'class': 'jobTitle jobTitle-color-purple jobTitle-newJob'}):
                title = j.find_all('span')[1].text.strip()
        except:
            title = ""
        try:
            company_name = i.find('span', class_ = 'companyName').text.strip()
        except:
            company_name = ""
        try:
            company_rating = i.find('span', class_ = 'ratingsDisplay').text.strip()
        except:
            company_rating = ""
        try:
            company_location = i.find('div', class_ = 'companyLocation').text.strip()
        except:
            company_location = ""
        try:
            salary = i.find('div', class_ = 'attribute_snippet').text.strip()
        except:
            salary = ""
        try:
            job_summary = i.find('div', class_ = 'job-snippet').text.strip().replace('\n', '')
        except:
            job_summary = ""
        try:
            date_posted = i.find('span', class_ = 'date').text.strip()
        except:
            date_posted = ""

        job = {
            'title' : title,
            'company' : company_name,
            'company rating' : company_rating,
            'company location' : company_location,
            'salary' : salary,
            'summary' : job_summary,
            'date' : date_posted
            }
        joblist.append(job)
    return

joblist = []

for i in range(0, 800, 10):
    db_jobs = get_url('database', 'bethlehem pa', 0)
    get_job(db_jobs)


df = pd.DataFrame(joblist)

def good_salary(salary):
    if 'year' | '30,000' in salary :
        return True
    else:
        return False

def reliable_company(company_rating):
    if company_rating > 3.0:
        return True
    else:
        return False

def good_location(company_location):
    if 'Bethlehem' | 'Allentown' in company_location:
        return True
    else:
        return False

def good_job(reliable_company, good_salary, good_location):
    if reliable_company == True & good_salary == True & good_location == True:
        return True
    else:
        return False


#df['reliable company'] = df['company rating'].apply(reliable_company)
#df['good salary'] = df['salary'].apply(good_salary)
#df['good location'] = df['company location'].apply(good_location)
#df['good job'] = df.apply(good_job)

print(df.head())

df.to_csv('jobs.csv')


