
from google.appengine.ext import ndb
import uuid
import datetime



class DogSighting(ndb.Model):

    sighting_id = ndb.StringProperty(required = True)
    date_time = ndb.DateTimeProperty()
    location = ndb.GeoPtProperty()
    picture = ndb.StringProperty()
    breed = ndb.StringProperty()
    size = ndb.StringProperty()
    user = ndb.StringProperty()
    notes = ndb.StringProperty()
    rating = ndb.IntegerProperty()


    @classmethod
    def build_key(cls, sighting_id):
        return ndb.Key("DogSighting", sighting_id)

    @classmethod
    def new(cls, lat, lon, picture, breed, size, user, notes, rating):
        sighting = cls()
        sighting.sighting_id = uuid.uuid4().hex
        sighting.key = cls.build_key(sighting.sighting_id)
        if lat and lon:
            sighting.location = ndb.GeoPt(lat, lon)
        sighting.picture = picture
        sighting.breed = breed
        sighting.size = size
        sighting.user = user
        sighting.notes = notes
        sighting.rating = rating
        sighting.date_time = datetime.datetime.utcnow()
        sighting.put()
        return sighting


