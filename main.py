
# ! modules:
# ? improt request module for http request
import requests
from requests.exceptions import HTTPError
# ? import thrading module
import threading
# ? import time and speep module
from time import time, sleep
# ? import Beautiful soup module for pars html
from bs4 import BeautifulSoup


# ! class:
# ? import course class
from classes.course import CourseClass
# ? import excel class
from classes.excel import ExcelClass
# ? import environment class
from environment.environment import EnvironmentClass



# ? create instance from environment class
env = EnvironmentClass()
# ? create instance from ecxel class
excel = ExcelClass('excel/maktabkhooneh_' + env.studentNumber + '.xlsx', 'maktabkhoone_course_list', env.coursePropTitleList)

# ? set interval to log active thread count every 1 second
def interval():
    previousThreadCount = 0
    while True:
        sleep(1 - time() % 1)
        if threading.active_count() == 6 and previousThreadCount > 6:
            if env.course_link_switch and env.course_info_switch:
                env.course_link_switch = False
                getCouresesInformation()
            elif env.course_link_switch and not(env.course_info_switch):
                break
            else:
                excel.closeExcel()
                break
                
            
        previousThreadCount = threading.active_count()
        print('number of actice thread is: ' + str(threading.active_count()))

class CourseThreadClass (threading.Thread):
   def __init__(self, row, link):
      threading.Thread.__init__(self)
      self.row = row
      self.link = link
   def run(self):
      getCoursesInfo(self.link, int(self.row))

class PageThreadClass (threading.Thread):
   def __init__(self, pageNumber):
      threading.Thread.__init__(self)
      self.pageNumber = pageNumber
   def run(self):
      getPageLink(self.pageNumber)

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


# ? read courses link from text file; 
def getCouresesInformation():
    couresLinkList = []

    # ? read courses link from text
    with open('courses-link.txt') as f:
        for line in f:
            couresLinkList.append(line.strip())
    
    print('total course link count is', len(couresLinkList))

    row = 1

    # ? loop over link
    for link in couresLinkList:
        row += 1
        try:

            if env.multithead_switch:
                # ? create instanve form thread class and pass link and row to it
                thread1 = CourseThreadClass(row, link)

                # ? start thread
                thread1.start()
            else:
                getCoursesInfo(link, int(row))

        # ? catch error white create and start thread 
        except:
            print ("Error: unable to start thread")

    # excel.closeExcel()
   
# ? request to get page and scrap link and write to text file
def getPageLink(page):
    print('getting page number ' + str(page+1))

    pageResponse = requests.get(env.courseListUrl + '/?p=' + str(page+1) + '&')
    pageHtml = BeautifulSoup(pageResponse.content, 'html.parser')

    # ? scrap links from DOM
    allCourseLink = pageHtml.find_all('a', class_='course-card__wrapper')

    # ? loop over links of page and puth to array and write to the text file
    for link in allCourseLink:
        link = env.siteUrl + link.get_attribute_list('href')[0]
        with open('courses-link.txt', 'a') as f:
            f.write(link + '\n')


# ? loop over pages and get courses page link
def loopOverPages(totalPage):
    print('getting coureses link ...')

    # ? make course link text file empty
    open('courses-link.txt', 'w').close()

    
    # ? loop over total page and get courses link
    for page in range(totalPage):
        try:

            if env.multithead_switch:
                # ? create instanve form thread class and pass link and row to it
                thread1 = PageThreadClass(page)

                # ? start thread
                thread1.start()

            else:
                getPageLink(page)

        # ? catch error white create and start thread 
        except:
            print ("Error: unable to start thread")


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
    

# ? create excel file and worksheet
excel.initExcel()

if env.multithead_switch:
    if env.course_link_switch:
        getTotalPage()
    elif env.course_info_switch:
        getCouresesInformation()


    interval()

else:
    if env.course_link_switch:
        getTotalPage()
    if env.course_info_switch:
        getCouresesInformation()
    excel.closeExcel()
