
from google.appengine.ext import ndb

class User (ndb.Model):
    email = ndb.StringProperty(required=True)
    first = ndb.StringProperty()
    last = ndb.StringProperty()
    picture = ndb.StringProperty() # url to picture
    tags = ndb.StringProperty(repeated=True)
    mentorLimit = ndb.IntegerProperty() # default = 3
    location = ndb.StringProperty() # optional
    mentees = ndb.StringProperty(repeated=True) # email address to mentee
    mentors = ndb.StringProperty(repeated=True) # email address to mentor
    gender = ndb.StringProperty() # male/female
    age = ndb.IntegerProperty() #
    mission = ndb.StringProperty() # 3 word tagline
