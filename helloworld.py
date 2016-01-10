import os

import webapp2
import jinja2

# Set up jinja environment
# os.path.dirname(__file__) means the current file
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

# HTML of the comment form
form = '''

'''


# Comment validation function
def valid_comment(comment):
    if comment != "Good":
        return True


# Handler class to make following webapp2 Handler more neat
class Handler(webapp2.RequestHandler):
    # Use .write to replace response.out.write
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # Useful functions to generate jinja templates
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


# Main page Handler
class MainPage(Handler):
    def write_form(self, error="", comment=""):
        self.write(form % {"comment": comment, "error": error})

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(form)
        # self.write_form()
        user_input = self.request.get("comment")
        self.render("index.html", error="", comment=user_input)

    def post(self):
        user_input = self.request.get("comment")
        if valid_comment(user_input):
            error_mes = "That's not a valid input."
            self.render("index.html", error=error_mes, comment=user_input)
        else:
            # Redirect users to thanks page
            self.redirect("/thanks")


# Thanks page Handler
class ThanksHandler(Handler):
    def get(self):
        self.write("Thanks!")


class TestHandler(webapp2.RequestHandler):
    def post(self):
        comment = self.request.get("comment")
        self.response.out.write(comment)

        #self.response.headers['Content-Type'] = 'text/plain'
        #self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', ThanksHandler),
                               ('/testform', TestHandler)],
                              debug=True)