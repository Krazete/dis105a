import webapp2
from google.appengine.api import urlfetch
import re

class Index(webapp2.RequestHandler):
    def set(self, path, header):
        # set header
        self.response.headers['Content-Type'] = header
        try:
            # get original content
            content = urlfetch.fetch(path).content
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
        # return the content
        return content
    def get(self):
        # original website
        path = 'https://www.math.uci.edu/~aaronc8/Su2017Math105A.html'
        # get original website content
        content = self.set(path, 'text/html')
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
var ico = document.head.appendChild(document.createElement("link"));\n\
ico.rel="icon";\n\
ico.href="./favicon.ico";\n\
</script>'
        # display revised content
        self.response.write(content)

class Local(Index):
    def get(self, path):
        # get original website
        path = 'https://www.math.uci.edu/~aaronc8/' + path
        # set header based on extension
        ext = path.split('.')[-1]
        if ext == 'pdf':
            header = 'application/' + ext
        else:
            header = 'text/' + ext
        # get original website content
        content = self.set(path, header)
        # display original content
        self.response.write(content)

sitemap = [
    ('/', Index),
    ('/(.*)', Local)
]

app = webapp2.WSGIApplication(sitemap, debug=True)
