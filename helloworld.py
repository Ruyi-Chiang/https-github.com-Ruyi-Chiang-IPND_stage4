import os
import webapp2
import jinja2
import urllib
import cgi

from google.appengine.ext import ndb


# Switch reference key
def reference_key(reference_name):
  return ndb.Key('Reference', reference_name)

# Construct a datastore key and model
# Model for bottom guestbook
class Comment(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  content = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add= True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)


class Reference(ndb.Model):
  """Models reference titles and links"""
  title = ndb.StringProperty()
  link = ndb.StringProperty()
    

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


class PostReference(webapp2.RequestHandler):
  def post(self):
    reference_id = self.request.get('form_name')
    reference_title = self.request.get('reference_title')
    reference_link = valid_comment(self.request.get('reference_link'))
    reference = Reference(parent=ndb.Key('Reference', reference_id), title=reference_title, link=reference_link)
    reference.put()

    # # Stay in the same page after passing the data
    query_params = {'Reference': reference_id}
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

        # CHECK: how to query Reference data
        # reference_key = ndb.Key('Reference', 'reference_0')
        # print '[DEBUG]'
        # print 'reference_key:', reference_key
        # reference_query = Reference.query(ancestor=reference_key)
        # self.write(reference_query)
        # reference_query.ancestor(Reference)
        
        
        # self.response.headers['Content-Type'] = 'text/plain'
        # self.response.out.write(form)
        # self.write_form()
        user_input = self.request.get('comment')
        self.render('index.html', error='', comment=user_input, main_concept=Concept_list, display_comment=comments)

    def post(self):
        user_input = self.request.get('comment')
        self.redirect('/thanks')
        # if valid_comment(user_input):
        #     error_mes = "That's not a valid input."
        #     self.render("index.html", error=error_mes, comment=user_input)
        # else:
        #     # Redirect users to thanks page
        #     self.redirect("/thanks")
    

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
                               ('/guestbook', SignGuestbook), 
                               ('/postreference',PostReference),
                               ('/thanks', ThanksHandler),
                               ('/testform', TestHandler)],
                              debug=True)