class EnvironmentClass:

    """

    |--------------------------------------------------------------------------------------------
    |                                                                                           |
    |     environment Class                                                                     |
    |                                                                                           |
    |--------------------------------------------------------------------------------------------
    |                                                                                           |
    |   1 - initial Class                                                                       |
    |       store cours list url, site url, student number excel property list,                 |                        |
    |       switch for course link request functionality and course info request functionality  |                                         |
    |       switch for multiple threading functionality                                         |
    |                                                                                           |
    ---------------------------------------------------------------------------------------------

    """
    # ? -> 1
    def __init__(self):
        
        self.courseListUrl = 'https://maktabkhooneh.org/learn'
        self.siteUrl = 'https://maktabkhooneh.org'
        self.studentNumber = '98521081'
        self.coursePropTitleList = ['عنوان دوره', 'نام استاد', 'نام موسسه', 'هزینه دوره', 'تعداد جلسه و ساعات', 'لینک']
        self.course_link_switch = True
        self.course_info_switch = True
        self.multithead_switch = True

