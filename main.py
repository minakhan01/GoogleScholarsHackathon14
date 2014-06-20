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

from webapp2_extras import sessions

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'madd',
}

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
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
        return self.session_store.get_session()

class MainHandler(BaseHandler):
    def get(self):
        self.response.write('Hello world!')
        user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write("<html><body>%s</body></html>" % greeting)

class ProfileHandler(BaseHandler):
    def get:
        template_values = {}
        template = jinja_environment.get_template("profile.html")
        self.response.out.write(template.render(template_values))

class MatchHandler(BaseHandler):
    def get:
        template_values = {}
        template = jinja_environment.get_template("matching.html")
        self.response.out.write(template.render(template_values))

class HangoutHandler(BaseHandler):
    def get:
        template_values = {}
        template = jinja_environment.get_template("hangout.html")
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/profile', ProfileHandler),
    ('/matching', MatchHandler),
    ('/hangout', HangoutHandler)
], debug=True)
