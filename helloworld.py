import os
import webapp2
import jinja2
import urllib


# Set Google App Engine Datastore
from google.appengine.ext import ndb

# Construct a datastore key and model
def guestbook_key():
  return ndb.Key('Guestbook', 'Bottom_book')

class Author(ndb.Model):
  """Sub model for representing an author."""
  identity = ndb.StringProperty(indexed= False)
  email = ndb.StringProperty(indexed= False)

class Comment(ndb.Model):
  """A main model for representing an individual comment entry"""
  author = ndb.StructuredProperty(Author)
  content = ndb.StringProperty(indexed= False)
  date = ndb.DateTimeProperty(auto_now_add= True)

# Put date into the DataStore
class Guestbook(webapp2.RequestHandler):
  def post(self):
    comment = Comment(parent= guestbook_key())

    if users.get_current_user():
      greeting.author = Author(
        identity = users.get_current_user().user_id(),
        email = users.get_current_user().email())

    comment.content = self.request.get('comment')
    comment.put()

    query_params = {'Bottom_book': 'Bottom_book'}
    self.redirect('/?' + urllib.urlencode(query_params))

# Set up jinja environment
# os.path.dirname(__file__) means the current file
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# data
# make a basic Concept class
Concept_list = [["Understanding of Servers",
                 '''
                 A server is a computer that interacts with a request we make to the computer. 
                 For example, whenever we type in "http://www.google.com", we are sending a request to Google's servers to return a website.
                 ''',
                 ["sub_concept", "sub_concept", "sub_concept"]],
                ["Importantance of Validating Input", "Summary of concept2", ["sub_concept", "sub_concept", "sub_concept"]],
                ["HTML Templates and Abstraction", "Summary of concept3", ["sub_concept", "sub_concept"]]]


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
    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(form)
        # self.write_form()
        user_input = self.request.get("comment")
        self.render("index.html", error="", comment=user_input, main_concept=Concept_list)
        
        comment_query = Comment.query(
          ancestor= guestbook_key()).order(-Comment.date)
        comments = comment_query.fetch(10)

        self.response.write('It works')

        # Display the content of comments
        for i in range(len(comments)):
          self.response.write('It works')
          self.response.write('<br> %s </br>' %i)
    
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
                               ('/guestbook', Guestbook),
                               ('/thanks', ThanksHandler),
                               ('/testform', TestHandler)],
                              debug=True)