import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

baseUrl = 'https://maktabkhooneh.org/learn'
siteUrl = 'https://maktabkhooneh.org'

def getCouresesInformation(couresLinkList):
    for coureslink in couresLinkList:
        print(siteUrl + coureslink)

def loopOverPages(totalPage):
    print('getting coureses link ...')
    couresLinkList = []

    
    for page in range(2):
        pageResponse = requests.get(baseUrl + '/?p=' + str(page+1) + '&')
        pageHtml = BeautifulSoup(pageResponse.content, 'html.parser')
        allCourseLink = pageHtml.find_all('a', class_='course-card__wrapper')
        for link in allCourseLink:
            couresLinkList.append(link.get_attribute_list('href')[0])

    print(couresLinkList)

    getCouresesInformation(couresLinkList)

try:
    print('getting total page ...')
    response = requests.get(baseUrl)
    html = BeautifulSoup(response.content, 'html.parser')

    totalPage = html.find_all('a', class_='paginator__link')[-1].text

    loopOverPages(totalPage)

    
    
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6
else:
    print('Success!')

