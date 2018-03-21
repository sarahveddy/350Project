# Copyright 2016 Google Inc.
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

import os
import webapp2 
from jinja2 import Environment, FileSystemLoader

class BaseHandler(webapp2.RequestHandler):
    def get(self):
        self.render_response("templates/static.html")

    def render_response(self, template, **kwargs):
        env = Environment(
            loader = FileSystemLoader(os.path.dirname(__file__)),
            extensions = ['jinja2.ext.autoescape'],
            autoescape = True
        )
        template = env.get_template(template)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(kwargs))

class AboutHandler(BaseHandler):
    def get(self):
        self.render_response("templates/about.html", page_title = "About")



app = webapp2.WSGIApplication([
    ('/', BaseHandler), ('/about', AboutHandler)
], debug = True)