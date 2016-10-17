import requests
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
        if server_answer.status_code == 200:
            return 'Yes'
    except requests.ConnectionError:
        pass
    return 'No'


def get_domain_expiration_date(domain_name):
    site_info = whois(url)
    if type(site_info['expiration_date']) == list:
        return site_info['expiration_date'][0]
    return site_info['expiration_date']


def is_domain_paid_month_ahead(expiration_date):
    if expiration_date - datetime.today().date() >= timedelta(days=PAID_DAYS_CHECK):
        return 'Yes'
    return 'No'


if __name__ == '__main__':
    url_list = load_urls4check('urls.txt')
    print('{0:40s}{4:5}{1:30s}{4:5}{2:25s}{4:5}{3:35s}{4:5}'.format('Site url', 'Does server respond with "200"',
                                                                    'Domain expiration date',
                                                                    'Is domain paid for month ahead', '  |  '))
    print('-' * 148)
    for url in url_list:
        is_responding = is_server_respond_with_200(url)
        expiration_date = get_domain_expiration_date(url)
        is_paid = 'No info'
        if expiration_date:
            expiration_date = expiration_date.date()
            is_paid = is_domain_paid_month_ahead(expiration_date)

        else:
            expiration_date = 'No info'
        print(
            '{0:40s}{4:5}{1:30s}{4:5}{2:25s}{4:5}{3:35s}{4:5}'.format(url, is_responding,
                                                                      str(expiration_date), is_paid, '  |  '))
