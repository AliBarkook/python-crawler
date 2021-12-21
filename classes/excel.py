# ? excel module
import xlsxwriter 

class ExcelClass:
    def __init__(self, excelName, sheetName, coursePropTitleList):

        self.excelName = excelName
        self.sheetName = sheetName
        self.coursePropTitleList = coursePropTitleList

        self.excelFile = xlsxwriter.Workbook(excelName)
        self.worksheet = self.excelFile.add_worksheet(sheetName)

    # ? write excel title
    def initExcel(self):
        col = 0
        for title in self.coursePropTitleList:

            self.worksheet.write(0, col, title)
            col += 1

    def closeExcel(self):
        while True:
            try:
                self.excelFile.close()
                break
            except xlsxwriter.exceptions.FileCreateError as e:
                decision = input("Exception caught in workbook.close(): %s\n"
                                "Please close the file if it is open in Excel.\n"
                                "Try to write file again? [Y/n]: " % e)
                if decision != 'n':
                    continue

    def storeDataInExcel(self, row, col, course):
        try:
            worksheet = self.excelFile.get_worksheet_by_name('maktabkhoone_course_list')
            for prop in course.getCourseList():
                worksheet.write(row, col, prop)
                col += 1
        except:
            print('can not write to excel file course number' + str(row))