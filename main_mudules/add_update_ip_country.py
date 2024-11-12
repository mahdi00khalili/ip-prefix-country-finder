from models.models import IpPerfix
from main import session
from ip_finder import request_to_map_ips_from_api


def add_update_ip_country():
    ip_perfixes_object = session.query(IpPerfix).filter_by(is_public = True).all()
    for ip_perfix_object in ip_perfixes_object:
        print(f'Adding {ip_perfix_object.ip_perfix}')
        x,y = ip_perfix_object.ip_perfix.split('.')
        request_to_map_ips_from_api(x,y)

add_update_ip_country()