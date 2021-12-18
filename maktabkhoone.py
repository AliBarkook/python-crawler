import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from course import Course

baseUrl = 'https://maktabkhooneh.org/learn'
siteUrl = 'https://maktabkhooneh.org'

# ? get courses info
def getCouresesInformation(couresLinkList):
    totalCourse = []
    courseResponse = requests.get('https://maktabkhooneh.org/course/%D8%A2%D9%85%D9%88%D8%B2%D8%B4-%D8%B1%D8%A7%DB%8C%DA%AF%D8%A7%D9%86-%D8%A2%D9%85%D8%A7%D8%B1-%D8%A7%D8%AD%D8%AA%D9%85%D8%A7%D9%84-mk1365/')
    courseHtml = BeautifulSoup(courseResponse.text, 'html.parser')
    # courseHtml.findChild(right-padding)
    x = courseHtml.select_one('.course-page')
    
    print(x)
    # for coureslink in couresLinkList:
        # print(siteUrl + coureslink)

        # course = Course()
        # totalCourse.append(course)



# ? loop over pages and get courses page link
def loopOverPages(totalPage):
    print('getting coureses link ...')
    couresLinkList = []

    
    for page in range(1):
        pageResponse = requests.get(baseUrl + '/?p=' + str(page+1) + '&')
        pageHtml = BeautifulSoup(pageResponse.content, 'html.parser')
        allCourseLink = pageHtml.find_all('a', class_='course-card__wrapper')
        for link in allCourseLink:
            couresLinkList.append(link.get_attribute_list('href')[0])

    print('total link count is', len(couresLinkList))
    # print(couresLinkList)
    x = []
    x.append(couresLinkList[0])
    getCouresesInformation(x)

# ? request to site and store total course page
def getTotalPage():
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
    

getTotalPage()