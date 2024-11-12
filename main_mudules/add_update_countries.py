import requests
from models.models import Country
from main import session

def get_country_names_and_codes():
    # REST Countries API endpoint
    url = "https://restcountries.com/v3.1/all"

    # Make the GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        countries = response.json()
        # Create a dictionary with full names as keys and abbreviations as values
        country_name_code_dict = {country["name"]["common"]: country["cca2"] for country in countries if
                                  "name" in country and "cca2" in country}

        return country_name_code_dict
    else:
        print("Failed to retrieve data:", response.status_code)
        return {}


def save_countries_in_database():
    countries = get_country_names_and_codes()
    if countries:
        for name, abbr in countries.items():
            country_obj = session.query(Country).filter_by(abbr=abbr).first()
            if not country_obj:
                print(name, ' : ',abbr)
                new_country = Country(name=name, abbr=abbr)
                session.add(new_country)  # Add the new country object to the session
                session.commit()

    else:
        print('no country')


save_countries_in_database()