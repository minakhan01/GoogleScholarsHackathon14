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

from google.appengine.ext import ndb


from google.appengine.api import oauth
from webapp2_extras import sessions

from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator

decorator = OAuth2Decorator(
  client_id='692021064973-s1m38r36dunrhusuhcvnmfbj5uj3eavf.apps.googleusercontent.com',
  client_secret='2cC1Y9SYjvLSDDJRFJFfu9dp',
  scope='https://www.googleapis.com/auth/plus.profile.emails.read')

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def console(s):
        sys.stderr.write('%s\n' % s)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        #params['user'] = self.user
        t = jinja_environment.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(BaseHandler):
    @decorator.oauth_required
    def get(self):        
        http = decorator.http()
        service = build("plus", "v1", http=http)
        # Call the service using the authorized Http object.
        request = service.people().get(userId="me")
        response = request.execute(http=http)
        user_id=response['id']
        name=response['displayName']
        image=response['image']['url']

        self.render("home.html")

        try:
            # Get the db.User that represents the user on whose behalf the
            # consumer is making this request.
            #user = oauth.get_current_user("https://www.googleapis.com/auth/userinfo.email")
            if response:
                greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (name, users.create_logout_url('/')))
                entity = User.by_user_id(user_id)
                self.write(greeting)
                if entity is None:
                    entity = User(user_id=user_id, picture=image, name=name)
                    entity.put()
                template_values = {"user":entity, "greeting":greeting}
                #self.redirect('/profile') 
            else:
                self.render("home.html")    

        except oauth.OAuthRequestError, e:
            self.write("Error")  

    """def get(self):
        self.render("home.html")"""

class ProfileHandler(BaseHandler):
    def get(self):
        user = User()
        user.email = "david.patrzeba@gmail.com"
        user.picture = "http://upload.wikimedia.org/wikipedia/commons/7/7f/Emma_Watson_2013.jpg"
        user.first = "Alice"
        user.age = 19
        user.tagline = "I am awesome"
        user.tags = ["Python"]
        user.interests = ["tennis", "table tennis"]
        template_values = {"user":user}
        self.render("profile.html", **template_values)

    def post(self):
        user = User()
        user.picture = "http://upload.wikimedia.org/wikipedia/commons/7/7f/Emma_Watson_2013.jpg"
        user.email = self.request.get('email')
        user.age = int(self.request.get('age'))
        user.tagline = self.request.get('mission')
        user.tags = self.request.get('tags').split(",")
        user.intersts = self.request.get('interests')
        user.put()
        template_values = {"user":user}
        self.render("profile.html", **template_values)
        

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
