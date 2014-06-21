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

from google.appengine.api import oauth
from webapp2_extras import sessions

from apiclient.discovery import build
from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator

decorator = OAuth2Decorator(
  client_id='692021064973-s1m38r36dunrhusuhcvnmfbj5uj3eavf.apps.googleusercontent.com',
  client_secret='2cC1Y9SYjvLSDDJRFJFfu9dp',
  scope='https://www.googleapis.com/auth/plus.login')


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
    @decorator.oauth_required
    def get(self):
            # Get the authorized Http object created by the decorator.
        http = decorator.http()
        service = build("plus", "v1", http=http)
        # Call the service using the authorized Http object.
        request = service.people().get(userId="me")
        response = request.execute(http=http)
        self.render("home.html")
        try:
            # Get the db.User that represents the user on whose behalf the
            # consumer is making this request.
            #user = oauth.get_current_user("https://www.googleapis.com/auth/userinfo.email")
            if response:
                self.response.write('Hello, ' + response['displayName'])
                self.response.write(response)
            else:
                self.render("home.html")    

        except oauth.OAuthRequestError, e:
            self.write("Error")  

class ProfileHandler(BaseHandler):
    def get(self):
        user = User()
        user.first = "Alice"
        user.age = 19
        user.tagline = "I am awesome"
        user.tags = ["Python"]
        user.interests = ["tennis", "table tennis"]
        template_values = {"user":user}
        self.render("profile.html", **template_values)

class MatchHandler(BaseHandler):
    def get(self):
        user = User()
        user.first = "Alice"
        user.age = 19
        user.tagline = "I am awesome"
        user.tags = ["Python"]
        user.interests = ["tennis", "table tennis"]
        users = [user]
        template_values = {"users":users}
        self.render("match.html", **template_values)

class HangoutHandler(BaseHandler):
    def get(self):
        template_values = {}
        self.render("hangout.html", **template_values)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/profile', ProfileHandler),
    ('/match', MatchHandler),
    ('/hangout', HangoutHandler),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
