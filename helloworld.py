import webapp2
import os
import jinja2

# Set up jinja environment
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

form = '''
<form method="post">
    Leave your comments. I would appreciate. :)
    <br>
    <input type="text" name="comment" value="%(comment)s">
    <br>
    %(error)s
    <br>
    <input type="submit">
</form>
'''

# Comment validation function
def valid_comment(comment):
    if comment != "Good":
        return True


class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", comment=""):
        self.response.out.write(form % {"comment": comment, "error": error})

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(form)
        self.write_form()

    def post(self):
        user_input = self.request.get("comment")
        if valid_comment(user_input):
            self.write_form("That's not a valid input.", user_input)
        else:
            self.response.out.write("Thanks!")


class TestHandler(webapp2.RequestHandler):
    def post(self):
        comment = self.request.get("comment")
        self.response.out.write(comment)

        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/testform', TestHandler)],
                              debug=True)