import os
import webapp2
import jinja2
import urllib
import cgi

from google.appengine.ext import ndb


# Construct a datastore key and model
# Model for bottom guestbook
class Comment(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  content = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add= True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)

# Storing data into the DataStore
class SignGuestbook(webapp2.RequestHandler):
  def post(self):
    guestbook_name = 'bottom_book'
    checked_comment = valid_comment(self.request.get('comment'))
    comment = Comment(parent=ndb.Key('Guestbook', guestbook_name), content=checked_comment)
    comment.put()

    # Stay in the same page after passing the data
    query_params = {'Guestbook': guestbook_name}
    self.redirect('/?' + urllib.urlencode(query_params))

# Set up jinja environment
# os.path.dirname(__file__) means the current file
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# data
# Note of the class
Concept_list = [ # Concept 1
                ["Understanding of Servers",
                 '''
                 A server is a computer that interacts with a request we make to the computer. 
                 For example, whenever we type in "http://www.google.com", we are sending a request to Google's servers to return a website.
                 ''',
                 ["GET requests: Parameters will be shown in the URL. Used for fetching data/documents. There is maximum URL length and it is ok to cache but should not change the server.", "POST requests: Parameters is in request body. It is usually used for updating data. There is no max length. "]],
                 # Concept 2
                ["Importantance of Validating Input", 
                 '''
                 In computer science, data validation is the process of ensuring that a program operates on clean, correct and useful data. Otherwise, the 'bad' data might break your server/application. It is an important security sense.
                 ''',
                  ["what data your application should accept?", "what its syntax should be and its minimum and maximum lengths?"]],
                  # Concept 3
                ["HTML Templates and Abstraction", "In this course, we use Jinja to create HTML templates. It is a tactic to create a template to help you to write repeated HTML code quicker.", ["curly brackets'{}' which states is all it takes to make your current template inherit a basic format from a parent template.", "'%' is used to insert python commands"]]]


# Comment validation function
def valid_comment(comment):
    comment = cgi.escape(comment)
    return comment


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
        # Display the content of comments
        guestbook_name = 'bottom_book'
        ancestor_key = ndb.Key('Guestbook', guestbook_name)
        comments = Comment.query_book(ancestor_key).fetch(10)

        user_input = self.request.get('comment')
        self.render('index.html', error='', comment=user_input, main_concept=Concept_list, display_comment=comments)


app = webapp2.WSGIApplication([('/', MainPage)],
                              debug=True)