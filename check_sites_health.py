import requests
import sys
from whois import whois
from datetime import datetime, timedelta

PAID_DAYS_CHECK = 30


def load_urls4check(path):
    with open(path, 'r', encoding="utf8") as input_file:
        url_list = input_file.read().split()
    return url_list


def is_server_respond_with_200(url):
    try:
        server_answer = requests.get(url)
        return server_answer.status_code == 200
    except requests.ConnectionError:
        pass


def get_domain_expiration_date(domain_name):
    site_info = whois(url)
    if type(site_info['expiration_date']) == list:
        return site_info['expiration_date'][0]
    return site_info['expiration_date']


def is_domain_paid_month_ahead(expiration_date):
    return expiration_date - datetime.today().date() >= timedelta(days=PAID_DAYS_CHECK)


def print_table_header():
    print('{0:40s}{4:3}{1:3s}{4:2}{2:10s}{4:3}{3:14s} |'.format('Site url', '200', 'd.exp.date',
                                                                'paid for month', ' | '))
    print('-' * 78)


if __name__ == '__main__':
    url_file_path = sys.argv[1]
    url_list = load_urls4check(url_file_path)
    print_table_header()
    for url in url_list:
        is_responding = 'No'
        if is_server_respond_with_200(url):
            is_responding = 'Yes'
        expiration_date = get_domain_expiration_date(url)
        is_paid = 'No info'
        if expiration_date:
            expiration_date = expiration_date.date()
            is_paid = 'No'
            if is_domain_paid_month_ahead(expiration_date):
                is_paid = 'Yes'
        else:
            expiration_date = 'No info'
        print('{0:40s}{4:3}{1:3s}{4:3}{2:10s}{4:3}{3:14s} |'.format(url, is_responding,
                                                                    str(expiration_date), is_paid,
                                                                    ' | '))
