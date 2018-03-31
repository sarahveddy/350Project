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
import json
from jinja2 import Environment, FileSystemLoader
from python.dog_sighting import DogSighting

class BaseHandler(webapp2.RequestHandler):
    def get(self):
        dogs = DogSighting.list_all()
        self.render_response("templates/static.html", dogs=dogs)

    def post(self):
        form_data = dict(self.request.POST)
        picture = self.request.POST.multi["picture"].file.read()
        print form_data
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(dict())
        DogSighting.new(None, None, picture, form_data.get("breed"),
                        form_data.get("size"), None, form_data.get("description"),
                        int(form_data.get("rating")))

    def render_response(self, template, **kwargs): #kwarg = keyword argument, could also pass page_title="" as argument
        env = Environment(
            loader = FileSystemLoader(os.path.dirname(__file__)),
            extensions = ['jinja2.ext.autoescape'],
            autoescape = True
        )
        template = env.get_template(template)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(kwargs))

# class AboutHandler(BaseHandler):
#     def get(self):
#         self.render_response("templates/about.html", page_title="About")
#
# class FormHandler(BaseHandler):
#     def get(self):
#         self.render_response("templates/form.html", page_title="Form")
#     def post(self):
#         dog = DogSighting.new(None,
#                               None,
#                               self.request.get("dog_pic"),
#                               self.request.get("dog_breed"),
#                               None,
#                               None,
#                               None,
#                               None)
#         self.render_response("templates/form.html", page_title=self.request.get("title", ""))



app = webapp2.WSGIApplication([
    ('/', BaseHandler),

], debug = True)