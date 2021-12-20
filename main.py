# ? request module for http request
import requests
from requests.exceptions import HTTPError

# ? Beautiful soup module for pars html
from bs4 import BeautifulSoup

# ? course class
from classes.course import CourseClass
# ? excel class
from classes.excel import ExcelClass
# ? excel class
from environment.environment import EnvironmentClass

env = EnvironmentClass()

excel = ExcelClass('maktabkhooneh_' + env.studentNumber + '.xlsx', 'maktabkhoone_course_list', env.coursePropTitleList)

# ? get courses info
def getCouresesInformation():
    couresLinkList = []
    with open('courses-link.txt') as f:
        for line in f:
            couresLinkList.append(line.strip())
    
    row = 1
    for link in couresLinkList:
        try:

            print('getting course number ' + str(couresLinkList.index(link)+1))

            courseResponse = requests.get(link)
            courseHtml = BeautifulSoup(courseResponse.text, 'html.parser')

            
            # ? fill neccessary data from DOM
            title = courseHtml.title.get_text()
            teacher = courseHtml.find_all(class_='teacher-card__image')[0]["title"]
            intitute = courseHtml.find_all(class_='teacher-card__image')[1]["title"]
            session = courseHtml.find(class_="chapter__clock-text").get_text()
            price = ''

            # ? check price
            if courseHtml.find(class_="fl2"):
                price = courseHtml.find(class_="fl2").get_text()
            else:
                price = 'رایگان'


            course = CourseClass(title, teacher, intitute, env.siteUrl + link, price, session)
            excel.storeDataInExcel(row, 0, course)
            row += 1

        except:
            print('can`t get course number ' + str(couresLinkList.index(link)+1))
            continue


    excel.closeExcel()
   

# ? loop over pages and get courses page link
def loopOverPages(totalPage):
    print('getting coureses link ...')
    couresLinkList = []
    open('courses-link.txt', 'w').close()

    
    for page in range(totalPage):
        print('getting page number ' + str(page+1))

        pageResponse = requests.get(env.courseListUrl + '/?p=' + str(page+1) + '&')
        pageHtml = BeautifulSoup(pageResponse.content, 'html.parser')
        allCourseLink = pageHtml.find_all('a', class_='course-card__wrapper')
        for link in allCourseLink:
            link = env.siteUrl + link.get_attribute_list('href')[0]
            couresLinkList.append(link)
            with open('courses-link.txt', 'a') as f:
                f.write(link + '\n')


    print('total course link count is', len(couresLinkList))
    

# ? request to site and store total course page
def getTotalPage():
    try:
        print('getting total page ...')
        response = requests.get(env.courseListUrl)
        html = BeautifulSoup(response.content, 'html.parser')

        totalPage = html.find_all('a', class_='paginator__link')[-1].text

        print('total page is', totalPage)

        loopOverPages(int(totalPage))

        
        
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
    
excel.initExcel()

if not(env.link_crawled_sitch):
    getTotalPage()

getCouresesInformation()