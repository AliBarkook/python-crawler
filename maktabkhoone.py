import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import xlsxwriter

from course import Course

courseListUrl = 'https://maktabkhooneh.org/learn'
siteUrl = 'https://maktabkhooneh.org'
studentNumber = '98521081'
coursePropTitleList = ['عنوان دوره', 'نام استاد', 'نام موسسه', 'هزینه دوره', 'تعداد جلسه و ساعات', 'لینک']

# ? get courses info
def getCouresesInformation(couresLinkList):
    totalCourse = []

    excelFile = xlsxwriter.Workbook('Example2.xlsx')
    worksheet = excelFile.add_worksheet()

    # ? write excel title
    row = 0
    col = 0
    for title in coursePropTitleList:

        worksheet.write(row, col, title)
        col += 1

    row += 1
    for link in couresLinkList:
        print('getting course number ' + str(couresLinkList.index(link)+1))
        courseResponse = requests.get(siteUrl + link)
        courseHtml = BeautifulSoup(courseResponse.text, 'html.parser')

        
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


        course = Course(title, teacher, intitute, siteUrl + link, price, session)
        totalCourse.append(course)


        
        
        col = 0
        for prop in course.getCourseList():

            worksheet.write(row, col, prop)
            col += 1
        row += 1

        

    excelFile.close()
    

    # Html_file= open("htmlDom2.txt","w", encoding="utf8")
    # Html_file.write(str(courseHtml.prettify()))
    # Html_file.close()
 





# ? loop over pages and get courses page link
def loopOverPages(totalPage):
    print('getting coureses link ...')
    couresLinkList = []

    
    for page in range(1):
        pageResponse = requests.get(courseListUrl + '/?p=' + str(page+1) + '&')
        pageHtml = BeautifulSoup(pageResponse.content, 'html.parser')
        allCourseLink = pageHtml.find_all('a', class_='course-card__wrapper')
        for link in allCourseLink:
            couresLinkList.append(link.get_attribute_list('href')[0])

    print('total link count is', len(couresLinkList))

    getCouresesInformation(couresLinkList)

# ? request to site and store total course page
def getTotalPage():
    try:
        print('getting total page ...')
        response = requests.get(courseListUrl)
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