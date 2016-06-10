import os, sys

class Saver():
    '''
    Scrapers save render and save page content in proper directory organization.
    '''
    def __init__(self):
        self.headers = {
            # 'User-Agent': 'LinkedInBot/1.0 (compatible; Mozilla/5.0; Jakarta Commons-HttpClient/3.1 +http://www.linkedin.com)'
            # 'User-Agent' : 'ROSIEBot/1.0 (+http://github.com/zamattiac/ROSIEBot)'
        }

    def save_html(self, html, page):
        print(page)
        page = page.split('//', 1)[1]
        self.make_dirs(page)
        f = open(page + 'index.html', 'wb')
        f.write(html)
        f.close()
        os.chdir(sys.path[0])

    def make_dirs(self, filename):
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)