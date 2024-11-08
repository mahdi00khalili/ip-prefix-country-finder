import requests
import json
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession


def get_ips(x_input, y_input):
    list_of_ips = []
    for i in range(256):
        for j in range(256):
            ip = f'{x_input}.{y_input}.{i}.{j}'
            list_of_ips.append(ip)

    list_of_ips = list(set(list_of_ips))

    return '\n'.join(list_of_ips)


def request_to_map_ips(x_input, y_input):
    # Define the SOCKS5 proxy

    try:
        url = "https://ipinfo.io/tools/map"
        payload = {
            "ips": get_ips(x_input, y_input)  # "8.8.8.8\n4.4.4.4"
        }

        # Make the request using the SOCKS5 proxy
        response = requests.post(url, data=payload)

        # Return response if successful
        return response
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


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


def get_countries_page_with_request_html(url):
    session = HTMLSession()

    # Make the request with the proxy and custom headers
    response = session.get(url)

    # Wait until a specific element is present
    response.html.render(wait=3, sleep=2, scrolldown=3)  # Additional scrolling and waiting
    html_content = response.html.html

    list_all_countries(html_content)
    countries = list_all_countries(html_content)
    for country in countries:
        print(country)


if __name__ == '__main__':
    x_y = input('ip-prefix (x.y): ')
    x, y = x_y.split('.')
    response_json = request_to_map_ips(x, y)

    # Parse the JSON string
    data = json.loads(response_json.text)

    # Extract the report URL
    report_url = data.get("reportUrl")
    get_countries_page_with_request_html(report_url)
