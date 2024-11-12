import requests
from models.models import Country
from main import session


def get_country_names_and_codes():
    # REST Countries API endpoint
    url = "https://restcountries.com/v3.1/all"

    try:
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()

        # Create a dictionary with full names as keys and abbreviations as values
        country_name_code_dict = {country["name"]["common"]: country["cca2"] for country in countries if
                                  "name" in country and "cca2" in country}

        return country_name_code_dict

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e} (function: get_country_name_and_codes).")
        quit()
    except ValueError as e:
        print(f"Error decoding JSON: {e} (function: get_country_name_and_codes).")
        quit()


def save_countries_in_database():
    countries = get_country_names_and_codes()
    if countries:
        for name, abbr in countries.items():
            country_obj = session.query(Country).filter_by(abbr=abbr).first()
            if not country_obj:
                print(name, ' : ', abbr)
                new_country = Country(name=name, abbr=abbr)
                session.add(new_country)  # Add the new country object to the session
                session.commit()


save_countries_in_database()
