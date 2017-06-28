import webapp2
from google.appengine.api import urlfetch
import re

class Index(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # original website
        original = 'https://www.math.uci.edu/~aaronc8/Su2017Math105A.html'
        try:
            # get original website's content
            content = urlfetch.fetch(original).content
            # replace a bunch of tags and styles and get rid of redundant whitespaces
            content += '<script>\n\
document.body.parentElement.innerHTML = document.body.parentElement.innerHTML\n\
.replace(/<\\/p>/g, "")\n\
.replace(/(<br\\s*\\/*>\\s*){2,}/g, "<br>")\n\
.replace(/\\s\\s+/g, " ")\n\
.replace(/<b>/g, "<h3>")\n\
.replace(/<\\/b>\\s*(<br>)*/g, "</h3>")\n\
.replace(/<\\/*font.*?>/g, "");\n\
document.body.style.backgroundColor = "#def";\n\
</script>'
        except:
            # redirect upon failure
            content = '<!DOCTYPE html>\n\
<head>\n\
    <title>Math 105A Discussion</title>\n\
    <style>\n\
        span {{\n\
            position: absolute;\n\
            top: 50%;\n\
            left: 50%;\n\
            transform: translate(-50%, -50%);\n\
            text-align: center;\n\
            vertical-align: middle;\n\
        }}\n\
    </style>\n\
    <meta http-equiv="refresh" content="3;url={0}">\n\
</head>\n\
<body>\n\
    <span>\n\
        Sorry, something went wrong.\n\
        <br>\n\
        You should be redirected to the original webpage soon.\n\
        <br>\n\
        <a href="{0}">Click here if it\'s taking too long.</a>\n\
    </span>\n\
</body>'.format(original)
        # display the revised content
        self.response.write(content)

class Local(webapp2.RequestHandler):
    def get(self, path):
        self.response.headers['Content-Type'] = 'text/html'
        # get original website's root
        root = 'https://www.math.uci.edu/~aaronc8/'
        # redirect to original file
        self.response.write('<!DOCTYPE html>\n\
<head>\n\
    <title>Math 105A Discussion</title>\n\
    <style>\n\
        span {{\n\
            position: absolute;\n\
            top: 50%;\n\
            left: 50%;\n\
            transform: translate(-50%, -50%);\n\
            text-align: center;\n\
            vertical-align: middle;\n\
        }}\n\
    </style>\n\
    <meta http-equiv="refresh" content="0;url={0}">\n\
</head>\n\
<body>\n\
    <span>\n\
        You should be redirected to the original file soon.\n\
        <br>\n\
        <a href="{0}">Click here if it\'s taking too long.</a>\n\
    </span>\n\
</body>'.format(root + path))

sitemap = [
    ('/', Index),
    ('/(.*)', Local)
]

app = webapp2.WSGIApplication(sitemap, debug=True)
