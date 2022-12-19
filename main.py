'''
    Author: Jenver I.

    Currently for logging the frequency of company's significant news
    on a given date range. Can be used to scrape for:
        - Buy-backs
        - Dividends

    An example of web scrapper
'''

import requests
import json
import datetime

NEWS_RESOURCE_BASE_URL = 'https://firstmetro.cdn.technistock.net/news/n-psendc-hist-json.asp?code={0}'
target_company_code = 'MEG'
NEWS_RESOURCE_URL = NEWS_RESOURCE_BASE_URL.format(target_company_code)

request_timeout = 5 ## Server might take some time to respond so use 5 seconds

date_format = '%m/%d/%Y'
target_date_range = {
    'begin': '01/01/2022',
    'begin_format': date_format,
    'end': '12/31/2022',
    'end_format': date_format
}

sample_data = '''{"newslist":{"1":{"newsid" :"0852201","newsdate" :"12/05/2022","newstime" :"08:52:20","newsHeader" :"[08:52] (9-1) Share Buy-Back Transactions","newsSeccode" :"MEG","newsurl" :"http://edge.pse.com.ph/openDiscViewer.do?edge_no=91d32d036942af043470cea4b051ca8f"},"2":{"newsid" :"0758021","newsdate" :"12/01/2022","newstime" :"07:58:02","newsHeader" :"[07:57] (9-1) Share Buy-Back Transactions","newsSeccode" :"MEG","newsurl" :"http://edge.pse.com.ph/openDiscViewer.do?edge_no=5ec49c2217f8e0933470cea4b051ca8f"}}}'''

def get_company_news(url):
    '''
    Use the news URL and get the list of news available for the company
    save it to log file for reference and return the data

    :param url: URL for the company news
    :return: JSON text data
    '''

    result = ''
    filename = f'{target_company_code}-raw news.log'

    try:

        result = requests.get(NEWS_RESOURCE_URL, timeout=request_timeout)

        ## Save to file the log for dissection
        with open(filename, "w") as file:
            file.writelines(result.text)

        if result.status_code == 200:
            return result.text

    except Exception as e:
        print(f'Unable to gather the company news: {e.args}')

    return result

def preprocess_report(json_text):
    '''
    Parse the response then extract the data from the main key of the json

    :param json_text: Response data from the request in str datatype
    :return: parsed JSON data filtered using the target date range
    '''

    main_key = 'newslist'
    json_data = {}

    try:
        dummy_json = json.loads(json_text)[main_key]
        for idx in dummy_json.keys():
            if is_within_date_range(dummy_json[idx].get('newsdate')):
                json_data[idx] = dummy_json[idx]

    except Exception as e:
        print(f'Unable to parse the json data: {e.args}')

    return json_data


def is_within_date_range(news_date):
    '''
    Check if the date from the news was within the desired date range

    :param news_date: Datestring of the news
    :return: Boolean whether the date was within range
    '''
    try:
        test_date = datetime.datetime.strptime(news_date, date_format)
        begin_date = datetime.datetime.strptime(target_date_range['begin'], target_date_range['begin_format'])
        end_date = datetime.datetime.strptime(target_date_range['end'], target_date_range['end_format'])

        if begin_date <= test_date <= end_date:
            return True

    except Exception as e:
        print(f'Failed to validate: {e.args}')

    return False


def gather_reports(json_data, target_report):
    '''
    Gather the reports based on the desired data

    :param json_data: JSON data that was already preprocessed
    :param target_report: filter to use on each news headers
    '''

    lookup_keyword = ''
    num_of_entries = 0
    collected_reports = []
    filename = f'{target_company_code}-no data.log'

    if target_report == 'buybacks':
        lookup_keyword = 'Share Buy-Back Transactions'
        filename = f'{target_company_code}-buybacks.log'
    elif target_report == 'dividends':
        lookup_keyword = 'Declaration of Cash Dividends'
        filename = f'{target_company_code}-dividends.log'

    try:
        with open(filename, "w") as file:

            # for idx in json_data.keys():
            #     if lookup_keyword in json_data[idx].get('newsHeader'):

            for idx in json_data.keys():
                if lookup_keyword in json_data[idx].get('newsHeader'):
                    num_of_entries += 1
                    ## Construct the data
                    report_data = '{0} {1}\n{2}\n{3}\n\n'.format(
                        json_data[idx].get("newsdate"),
                        json_data[idx].get("newstime"),
                        json_data[idx].get("newsHeader"),
                        json_data[idx].get("newsurl")
                    )
                    collected_reports.append(report_data)
                    ## Save to the log file the result

                    print(report_data)

            collected_reports.insert(0, f'Total of {num_of_entries} entries collected\n\n')
            file.writelines(collected_reports)

    except Exception as e:
        print(f'Error encountered during extraction of data {e.args}')


if __name__ == '__main__':

    news_data = get_company_news(NEWS_RESOURCE_URL)
    report_data = preprocess_report(news_data)

    gather_reports(report_data, 'buybacks')
    gather_reports(report_data, 'dividends')
