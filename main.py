#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import users
import webapp2
import jinja2
import os
import logging
from user import User
import sys

"""from google.appengine.api import oauth
from webapp2_extras import sessions

from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator

decorator = OAuth2Decorator(
  client_id='692021064973-s1m38r36dunrhusuhcvnmfbj5uj3eavf.apps.googleusercontent.com',
  client_secret='2cC1Y9SYjvLSDDJRFJFfu9dp',
  scope='https://www.googleapis.com/auth/plus.profile.emails.read')"""


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
config = {}
"""config['webapp2_extras.sessions'] = {
    'secret_key': 'madd',
}"""

def console(s):
        sys.stderr.write('%s\n' % s)

class BaseHandler(webapp2.RequestHandler):
    """def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()"""

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        #params['user'] = self.user
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainHandler(BaseHandler):
    """@decorator.oauth_required
    def get(self):
            # Get the authorized Http object created by the decorator.
        http = decorator.http()
        service = build("plus", "v1", http=http)
        # Call the service using the authorized Http object.
        request = service.people().get(userId="me")
        response = request.execute(http=http)
        id_user=response['displayName']
        email=response['image']['url']
        
        self.render("home.html")
        try:
            # Get the db.User that represents the user on whose behalf the
            # consumer is making this request.
            #user = oauth.get_current_user("https://www.googleapis.com/auth/userinfo.email")
            if response:
                self.response.write('Hello, '+id_user)
                self.response.write(response)
                greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (id_user, users.create_logout_url('/')))
                self.response.out.write("<html><body>%s</body></html>" % greeting)

            else:
                self.render("home.html","")    

        except oauth.OAuthRequestError, e:
            self.write("Error") """
    def get(self):
        user = users.get_current_user()

        if user:
            self.render("mentor.html")
        else:
            self.redirect(users.create_login_url(self.request.uri)) 

class ProfileHandler(BaseHandler):
    def get(self):
        user = User()
        user.picture = "http://upload.wikimedia.org/wikipedia/commons/7/7f/Emma_Watson_2013.jpg"
        user.first = "Alice"
        user.age = 19
        user.tagline = "I am awesome"
        user.tags = ["Python"]
        user.interests = ["tennis", "table tennis"]
        template_values = {"user":user}
        self.render("profile.html", **template_values)

    def post(self):
        user = User.get_or_insert(self.request.get('email'))
        user.age = self.request.get('age')
        user.tagline = self.request.get('mission')
        user.tags = self.request.get('tags')
        user.intersts = self.request.get('interests')
        user.put()
        

class MatchHandler(BaseHandler):
    def get(self):
        user = User()
        user.email = "david.patrzeba@gmail.com"
        user.picture = "http://upload.wikimedia.org/wikipedia/commons/7/7f/Emma_Watson_2013.jpg"
        user.first = "Alice"
        user.age = 19
        user.tagline = "I am awesome"
        user.tags = ["Python"]
        user.interests = ["tennis", "table tennis"]

        user2 = User()
        user2.picture = "http://cdn.images.express.co.uk/img/dynamic/79/590x/emma-watson-376861.jpg"
        user2.first = "Alice2"
        user2.age = 192
        user2.tagline = "I am awesome2"
        user2.tags = ["Python2"]
        user2.interests = ["tennis2", "table tennis2"]

        current_user = User()
        users = [user, user2]
        template_values = {"users":users, "current_user":current_user}
        self.render("match.html", **template_values)

class HangoutHandler(BaseHandler):
    def get(self):
        self.redirect("https://www.google.com/+/learnmore/hangouts/")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/profile', ProfileHandler),
    ('/match', MatchHandler),
    ('/hangout', HangoutHandler)
], debug=True)
