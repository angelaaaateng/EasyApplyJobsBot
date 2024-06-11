import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Function to parse the text file and extract relevant information
def parse_text_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Category:"):
                category = line.split(",")[0].split(": ")[1]
                location = line.split(",")[1].split(": ")[1]
                total_jobs = int(line.split()[-3])
            elif line.strip() and line[0].isdigit():
                parts = line.split(" | ")
                job_num = int(parts[0])
                title = parts[1].strip()
                company = parts[2].strip()
                location = parts[3].strip()
                status = "Need manual submission" if "* 🥵 Cannot apply" in parts[-1] else "Submitted"
                url = parts[-1].split()[-1]
                date_applied = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                salary = ""  # Since salary information is not provided in the text file
                if not title or not company:
                    title, company = get_title_and_company(url)
                data.append([title, company, location, status, url, date_applied, salary])
    return data

# Function to get job title and company from LinkedIn job page using URL
def get_title_and_company(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('h1', class_='topcard__title').text.strip()
        company = soup.find('a', class_='topcard__org-name-link').text.strip()
        return title, company
    except Exception as e:
        print(f"Error fetching data from URL: {url}")
        print(e)
        return "", ""

# Function to write the parsed data to a CSV file
def write_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Job Title", "Company", "Location", "Status", "URL", "Date Applied", "Salary"])
        writer.writerows(data)

# Main function to execute the parsing and writing to CSV
def main():
    file_path = './data/Applied Jobs DATA - 20240611.txt'
    csv_file = '/data/applied_jobs_0.csv'
    data = parse_text_file(file_path)
    write_to_csv(data, csv_file)
    print("CSV file created successfully.")

if __name__ == "__main__":
    main()
