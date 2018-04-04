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

from google.appengine.api import images

from jinja2 import Environment, FileSystemLoader
from python.dog_sighting import DogSighting

class BaseHandler(webapp2.RequestHandler):

    APIKEY = "AIzaSyDPcGinCZer-N5pKXSy98ICF6jmmUDCSDY"

    def get(self):
        dogs = DogSighting.list_all()
        self.render_response("templates/static.html", dogs=dogs, APIkey=self.APIKEY)

    def post(self):
        form_data = dict(self.request.POST)
        picture = self.request.POST.multi["picture"].file.read()
        cropped_picture = self._crop_image(picture)
        DogSighting.new(form_data.get("lat"), form_data.get("lon"), cropped_picture, form_data.get("dog_breed"),
                        form_data.get("size"), None, form_data.get("description"),
                        int(form_data.get("rating")), form_data.get("picture_title"))

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(dict())

    def _crop_image(self, picture):
        img = images.Image(picture)
        smallest = min(img.width, img.height)
        new_img = images.resize(picture, smallest, smallest, crop_to_fit=True)
        return new_img

    def render_response(self, template, **kwargs): #kwarg = keyword argument, could also pass page_title="" as argument
        env = Environment(
            loader = FileSystemLoader(os.path.dirname(__file__)),
            extensions = ['jinja2.ext.autoescape'],
            autoescape = True
        )
        template = env.get_template(template)
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(template.render(kwargs))


class GetDogsHandler(webapp2.RequestHandler):
    def get(self):
        dogs = DogSighting.list_all()
        dict_dogs = [ndb_dog.to_dict() for ndb_dog in dogs] #list comprehension
        for dog in dict_dogs:
            dog.pop("picture") #removes picture from dictionary
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(dict_dogs, default=str))
        print "*********"
        print dict_dogs




class ImageHandler(webapp2.RedirectHandler):
    def get(self):
        dog = DogSighting.build_key(self.request.get('sighting_id')).get()
        if dog.picture:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(dog.picture)
        else:
            self.response.out.write("no image")



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
    ('/', BaseHandler), ('/getDogs', GetDogsHandler), ('/img/', ImageHandler)

], debug = True)