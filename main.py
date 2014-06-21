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
    def get(self):
        user = users.get_current_user()

        if user:
            entity_key = ndb.Key.from_path(user.email())
            entity = entity_key.get()
            if entity is None:
                entity = User(key_name=user.email(), **kwds)
                entity.put()
                self.redirect("profile.html")
            else:
                self.redirect("match.html")
        else:
            self.render("home.html")

class ProfileHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        template_values = {"user":user}
        self.render("profile.html", **template_values)

    def post(self):
        user = users.get_current_user()
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
