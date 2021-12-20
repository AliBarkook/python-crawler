# ? course class
class Course():

    def __init__(self, courseName, teacherName, instituteName, courseLink, coursePrice, courseSessionCountOrTime):

        self.courseName = courseName
        self.teacherName = teacherName
        self.instituteName = instituteName
        self.courseLink = courseLink
        self.coursePrice = coursePrice
        self.courseSessionCountOrTime = courseSessionCountOrTime

    def getCourseList(self):
        proplist = []
        proplist.append(self.courseName)
        proplist.append(self.teacherName)
        proplist.append(self.instituteName)
        proplist.append(self.coursePrice)
        proplist.append(self.courseSessionCountOrTime)
        proplist.append(self.courseLink)
        return proplist
    