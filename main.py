import requests

NEWS_RESOURCE_BASE_URL = 'https://firstmetro.cdn.technistock.net/news/n-psendc-hist-json.asp?code={0}'
target_company_code = 'MEG'
NEWS_RESOURCE_URL = NEWS_RESOURCE_BASE_URL.format(target_company_code)
request_timeout = 5 ## Server might take some time to respond so use 5 seconds


def get_company_news(url):
    '''

    :param url: URL for the company news
    :return:
    '''
    result = ''
    try:

        result = requests.get(NEWS_RESOURCE_URL, timeout=request_timeout)

        ## Save to file the log for dissection
        with open("news.log", "w") as file:
            file.writelines(result.text)

        if result.status_code == 200:
            return result.text

    except Exception as e:
        print(f'Unable to gather the company news: {e.args}')

    return result



def gather_reports(url):
    '''
    Gathers the reports using the provided links of the buy back
    :param report_url: URL of the report from the trading platform
    :return:
    '''
    try:

        result = requests.get(NEWS_RESOURCE_URL, timeout=request_timeout)

    except Exception as e:
        print(f'Unable to gather the report: {e.args}')

if __name__ == '__main__':

    print(get_company_news(NEWS_RESOURCE_URL))
