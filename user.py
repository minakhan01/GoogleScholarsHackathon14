
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

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, email, tags):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)