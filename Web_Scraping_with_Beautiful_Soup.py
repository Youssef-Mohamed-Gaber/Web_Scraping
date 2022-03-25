from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import requests

job_title = []
company_name = []
location = []
Type = []
date = []
links = []
salaries = []
requirements = []
page_num = 0

while True:
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=spbg&q=python&start={page_num}")

    src = result.content

    soup = BeautifulSoup(src, "lxml")

    page_limit = int(soup.find("strong").text)
    if page_num > page_limit // 15:
        print("done")
        break

    job_titles = soup.find_all("h2", {"class": "css-m604qf"})
    company_names = soup.find_all("root", {"class": "css-17s97q8"})
    job_locations = soup.find_all("span", {"class": "css-5wys0k"})
    job_type = soup.find_all("div", {"class": "css-1w0948b"})
    job_templates = soup.find_all("div", {"class": "css-1o5ybe7 e1581u7e0"})

    for i in range(len(job_titles)):
        job_title.append(job_titles[i].text)
        company_name.append(company_names[i].text)
        location.append(job_locations[i].text)
        Type.append(job_type[i].text)
        links.append(job_titles[i].find("root").attrs["href"])

    for job_template in job_templates:
        if job_template.find("div", {"class": "css-4c4ojb"}):
            posted_new = job_template.find("div", {"class": "css-4c4ojb"})
            date.append(posted_new.text.replace("-", "").strip())
        elif job_template.find("div", {"class": "css-do6t5g"}):
            posted_old = job_template.find("div", {"class": "css-do6t5g"})
            date.append(posted_old.text.replace("-", "").strip())

    for link in links:
        result = requests.get(link)
        src = result.content
        soup = BeautifulSoup(src, "lxml")
        job_salaries = soup.find("div", {"class": "matching-requirement-icon-container",
                                         "data-toggle": "tooltip",
                                         "data-placement": "top"})
        salaries.append(job_salaries.text.strip())
        job_requirements = soup.find("span", {"itemprop": "responsibilities"}).find("ul")
        requirements_text = ""
        for li in job_requirements.find_all("li"):
            requirements_text += li.text + "| "
        requirements_text = requirements_text[: -2]
        requirements.append(requirements_text)

    page_num += 1
    print("page switched")
file_list = [job_title, company_name, date, location, Type, links, salaries, requirements]
Exported = zip_longest(*file_list)
with open("jobs_test.csv", "w") as file:
    wr = csv.writer(file)
    wr.writerow(["Job Title", "Company Name", "Date", "Location", "Type", "Link", "Salary", "Requirements"])
    wr.writerows(Exported)

file.close()
