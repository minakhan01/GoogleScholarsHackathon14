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

from google.appengine.api import xmpp
from webapp2_extras import sessions

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
config = {}
"""config['webapp2_extras.sessions'] = {
    'secret_key': 'madd',
}"""

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
    def get(self):
        self.render("home.html")

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
        user.age = self.request.get('age')
        user.tagline = self.request.get('mission')
        user.tags = self.request.get('tags')
        user.intersts = self.request.get('intersts')
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
