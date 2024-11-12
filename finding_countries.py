from models.models import IpCountry, IpPerfix, Country
from ip_finder import request_to_map_ips_from_api
from main import session


def is_public_ip_perfix(x_y_input):
    ip_perfix_object = session.query(IpPerfix).filter_by(ip_perfix = x_y_input).first()
    if ip_perfix_object.is_public:
        return True
    else:
        return False


def finding_countries_in_database(x_y_input):
    ip_perfix_id = session.query(IpPerfix).filter_by(ip_perfix = x_y_input).first().id
    ip_countries_obj = session.query(IpCountry).filter_by(ip_perfix_id = ip_perfix_id).all()
    if ip_countries_obj:
        for ip_country_obj in ip_countries_obj:
            country_obj = session.query(Country).filter_by(id = ip_country_obj.country_id).first()
            print(country_obj.abbr)
        return True
    else:
        return False

def finding_countries_with_api(x_y_input):
    print('please wait to getting the result from api and saving it in database')
    x, y = x_y_input.split('.')
    countries = request_to_map_ips_from_api(x, y)
    for country in countries:
        country_obj = session.query(Country).filter_by(name = country).first()
        if country_obj:
            print(country_obj.abbr)
        else:
            print(country)


def finding_countries(x_y_input):
    check = finding_countries_in_database(x_y_input)
    if not check:
        finding_countries_with_api(x_y_input)


if __name__ == '__main__':
    x_y = input('ip-prefix (x.y): ')
    if is_public_ip_perfix(x_y):
        finding_countries(x_y)
    else:
        print('Enter a public ip perfix')
