
from google.appengine.ext import db

class User (db.Model):
    email = db.StringProperty(required=True)
    first = db.StringProperty()
    last = db.StringProperty()
    picture = db.StringProperty() # url to picture
    tags = db.StringListProperty(required=True)
    mentorLimit = db.IntegerProperty() # default = 3
    location = db.StringProperty() # optional
    mentees = db.StringListProperty() # email address to mentee
    mentors = db.StringListProperty() # email address to mentor
    gender = db.StringProperty() # male/female
    age = db.IntegerProperty() #
    mission = db.StringProperty() # 3 word tagline

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_email(cls, email):
        u = User.all().filter('email =', email).get()
        return u

    @classmethod
    def by_name(cls, first):
        u = User.all().filter('first =', first).get()
        return u    