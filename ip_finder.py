import requests
import json
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from main import session
from models.models import IpPerfix, Country, IpCountry


def remove_expired_ip_country(ip_country_dict):
    ip_perfix_id = list(ip_country_dict.keys())[0]
    ip_country_list_in_database = session.query(IpCountry).filter_by(ip_perfix_id=int(ip_perfix_id)).all()

    for ip_country in ip_country_list_in_database:
        if ip_country.country_id not in ip_country_dict[ip_perfix_id]:
            print(ip_country.country_id)
            session.delete(ip_country)
    session.commit()


def convert_country_list_to_id_list(countries):
    countries_id = []
    for country in countries:
        country_obj = session.query(Country).filter_by(name=country).first()
        if country_obj:
            countries_id.append(country_obj.id)
    return countries_id


def save_ip_country_in_db(countries_id, ip_perfix):
    ip_perfix_id = session.query(IpPerfix).filter_by(ip_perfix=ip_perfix).first().id

    for country_id in countries_id:
        ip_country_obj = session.query(IpCountry).filter_by(ip_perfix_id=ip_perfix_id, country_id=country_id).first()
        if not ip_country_obj:
            new_ip_country = IpCountry(ip_perfix_id=ip_perfix_id, country_id=country_id)
            session.add(new_ip_country)
    session.commit()

    ip_country_dict = {f'{ip_perfix_id}': [country_id for country_id in countries_id]}
    remove_expired_ip_country(ip_country_dict)


def get_countries_page_with_request_html(url, ip_perfix):
    session_html = HTMLSession()

    # Make the request with the proxy and custom headers
    response = session_html.get(url)

    # Wait until a specific element is present
    response.html.render(wait=3, sleep=2, scrolldown=3)  # Additional scrolling and waiting
    html_content = response.html.html

    list_all_countries(html_content)
    countries = list_all_countries(html_content)
    countries_id = convert_country_list_to_id_list(countries)
    save_ip_country_in_db(countries_id, ip_perfix)
    return countries


def get_ips(x_input, y_input):
    list_of_ips = []
    for i in range(256):
        for j in range(256):
            ip = f'{x_input}.{y_input}.{i}.{j}'
            list_of_ips.append(ip)

    list_of_ips = list(set(list_of_ips))

    return '\n'.join(list_of_ips)


def request_to_map_ips_from_api(x_input, y_input):
    try:
        url = "https://ipinfo.io/tools/map"
        payload = {
            "ips": get_ips(x_input, y_input)  # "8.8.8.8\n4.4.4.4"
        }
        response = requests.post(url, data=payload)

        # Parse the JSON string
        response_data = json.loads(response.text)

        # Extract the report URL
        report_url = response_data.get("reportUrl")
        ip_perfix = x_input + '.' + y_input
        countries = get_countries_page_with_request_html(report_url, ip_perfix)
        return countries
    except requests.exceptions.RequestException as e:
        print("Request failed:", e, '(on request_to_map_ips_from_api function)')
        quit()


def list_all_countries(html_content):
    # Open the HTML file
    html_content = html_content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <li> tags with the specified class pattern
    li_tags = soup.find_all("li", class_="px-5 lg:px-8 py-3 lg:py-5 cursor-pointer")

    # Define the regex pattern to capture the country and IP count
    pattern = re.compile(r"([A-Za-z\s]+)\s*\d+\s*IPs")
    list_of_countries = []
    # Loop through each <li> tag and apply the regex
    for index, li_tag in enumerate(li_tags, start=1):
        content = li_tag.get_text(strip=True)  # Get the text content of the tag
        match = pattern.search(content)  # Search for the pattern in the content

        if match:
            country = match.group(1).strip()
            if country != 'Worldwide':
                list_of_countries.append(country.strip())

    return list_of_countries


