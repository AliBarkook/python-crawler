# ? request module for http request
import requests
from requests.exceptions import HTTPError

import threading

# ? Beautiful soup module for pars html
from bs4 import BeautifulSoup

# ? course class
from classes.course import CourseClass
# ? excel class
from classes.excel import ExcelClass
# ? excel class
from environment.environment import EnvironmentClass


# ? create instance from environment class
env = EnvironmentClass()

# ? create instance from ecxel class
excel = ExcelClass('maktabkhooneh_' + env.studentNumber + '-3.xlsx', 'maktabkhoone_course_list', env.coursePropTitleList)

class myThread (threading.Thread):
   def __init__(self, row, link):
      threading.Thread.__init__(self)
      self.row = row
      self.link = link
   def run(self):
      print ("Starting thread number " + str(self.row))
      getCoursesInfo(self.link, int(self.row))

# ? request to get courses info
def getCoursesInfo(link, index):
    try:

        print('getting course number ' + str(index) + '\n')

        courseResponse = requests.get(link)
        courseHtml = BeautifulSoup(courseResponse.text, 'html.parser')

        
        # ? scrap required data from DOM (title, teacher , ...)
        title = courseHtml.title.get_text()
        teacher = courseHtml.find_all(class_='teacher-card__image')[0]["title"]
        intitute = courseHtml.find_all(class_='teacher-card__image')[1]["title"]
        session = courseHtml.find(class_="chapter__clock-text").get_text()
        price = ''

        # ? check price is free or not
        if courseHtml.find(class_="fl2"):
            price = courseHtml.find(class_="fl2").get_text()
        else:
            price = 'رایگان'


        # ? create instance from course class
        course = CourseClass(title, teacher, intitute, link, price, session)

        # ? store course in excel
        excel.storeDataInExcel(index, 0, course)

        return
    except:
        print('can`t get course number ' + str(index))
        return


# ? read courses link and create thead; 
def getCouresesInformation():
    couresLinkList = []

    # ? read courses link from text
    with open('courses-link.txt') as f:
        for line in f:
            couresLinkList.append(line.strip())
    
    row = 1

    # ? loop over link
    for link in couresLinkList:
        row += 1
        try:
            # ? create instanve form thread class and pass link and row to it
            thread1 = myThread(row, link)

            # ? start thread
            thread1.start()

        # ? catch error white create and start thread 
        except:
            print ("Error: unable to start thread")

    excel.closeExcel()
   

# ? loop over pages and get courses page link
def loopOverPages(totalPage):
    print('getting coureses link ...')
    couresLinkList = []

    # ? make courses link text file empty
    open('courses-link.txt', 'w').close()

    
    # ? loop over total page and get courses link
    for page in range(totalPage):
        print('getting page number ' + str(page+1))

        pageResponse = requests.get(env.courseListUrl + '/?p=' + str(page+1) + '&')
        pageHtml = BeautifulSoup(pageResponse.content, 'html.parser')

        # ? scrap links from DOM
        allCourseLink = pageHtml.find_all('a', class_='course-card__wrapper')

        # ? loop over links of page and puth to array and write to the text file
        for link in allCourseLink:
            link = env.siteUrl + link.get_attribute_list('href')[0]
            couresLinkList.append(link)
            with open('courses-link.txt', 'a') as f:
                f.write(link + '\n')


    print('total course link count is', len(couresLinkList))
    

# ? request to site and store total course page
def getTotalPage():
    # ? try to get total page
    try:
        print('getting total page ...')

        response = requests.get(env.courseListUrl)
        html = BeautifulSoup(response.content, 'html.parser')

        # ? scrap total page count from DOM
        totalPage = html.find_all('a', class_='paginator__link')[-1].text

        print('total page is', totalPage)

        loopOverPages(int(totalPage))
    
        response.raise_for_status()

    # ? catch errors
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
    


excel.initExcel()

if env.course_link_switch:
    getTotalPage()

if env.course_info_switch:
    getCouresesInformation()