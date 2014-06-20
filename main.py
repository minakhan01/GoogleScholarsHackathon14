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

class XMPPHandler(BaseHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        if message.body[0:5].lower() == 'hello':
            message.reply("Greetings!")

class XMPPHandler_available(BaseHandler):
    def post(self):
        sender = self.request.get('from').split('/')[0]
        xmpp.send_presence(sender, status=self.request.get('status'), presence_show=self.request.get('show'))    

class XMPPHandler_unavailable(BaseHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)

class XMPPHandler_probe(BaseHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        if message.body[0:5].lower() == 'hello':
            message.reply("Greetings!")                               

class MainHandler(BaseHandler):
    def get(self):
        self.response.write('Hello world!')
        """user = users.get_current_user()
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))

        self.response.out.write("<html><body>%s</body></html>" % greeting)"""


class ProfileHandler(BaseHandler):
    def get(self):
        template_values = {}
        self.write("profile.html", *template_values)

class MatchHandler(BaseHandler):
    def get(self):
        template_values = {}
        self.render("match.html", *template_values)

class HangoutHandler(BaseHandler):
    def get(self):
        template_values = {}
        self.render("hangout.html", *template_values)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/profile', ProfileHandler),
    ('/match', MatchHandler),
    ('/hangout', HangoutHandler),
    ('/_ah/xmpp/presence/available/', XMPPHandler_available),
    ('/_ah/xmpp/presence/unavailable/', XMPPHandler_unavailable),
    ('/_ah/xmpp/presence/probe/', XMPPHandler_probe),
    ('/_ah/xmpp/message/chat/', XMPPHandler)
], debug=True)
