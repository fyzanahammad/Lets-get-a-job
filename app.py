import streamlit as st
import requests
from bs4 import BeautifulSoup

def scrape_internshala_job(url):
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract job title
    job_title = soup.find('h1', {'class': 'profile_on_detail_page'}).get_text(strip=True) if soup.find('h1', {'class': 'profile_on_detail_page'}) else 'N/A'
    
    # Extract company name
    company_name = soup.find('a', {'class': 'link_display_like_text'}).get_text(strip=True) if soup.find('a', {'class': 'link_display_like_text'}) else 'N/A'
    
    # Extract other job details
    job_details = {}
    
    detail_sections = soup.find_all('div', {'class': 'internship_other_details_container'})
    for section in detail_sections:
        key = section.find('div', {'class': 'item_heading'}).get_text(strip=True)
        value = section.find('div', {'class': 'item_body'}).get_text(strip=True)
        job_details[key] = value

    # Extract stipend
    stipend = soup.find('span', {'class': 'stipend'}).get_text(strip=True) if soup.find('span', {'class': 'stipend'}) else 'N/A'
    job_details['Stipend'] = stipend

    # Extract benefits and perks if available
    benefits_section = soup.find('div', {'class': 'section_heading'})
    if benefits_section and 'Perks' in benefits_section.get_text(strip=True):
        benefits_list = benefits_section.find_next('div').find_all('span', {'class': 'round_tabs'})
        benefits = [benefit.get_text(strip=True) for benefit in benefits_list]
        job_details['Benefits'] = benefits

    return {
        "Job Title": job_title,
        "Company Name": company_name,
        **job_details
    }

st.title('Internshala Job Scraper')

url = st.text_input('Enter the Internshala Job URL')

if url:
    with st.spinner('Scraping job details...'):
        job_info = scrape_internshala_job(url)
    
    if isinstance(job_info, str):
        st.error(job_info)
    else:
        st.success('Job details scraped successfully!')
        for key, value in job_info.items():
            st.write(f"**{key}:** {value}")
