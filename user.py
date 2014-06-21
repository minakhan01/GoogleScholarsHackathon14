
from google.appengine.ext import db

class User (db.Model):
    email = db.StringProperty()
    name = db.StringProperty(required=True)
    picture = db.StringProperty() # url to picture
    tags = db.StringListProperty()
    mentorLimit = db.IntegerProperty() # default = 3
    location = db.StringProperty() # optional
    mentees = db.StringListProperty() # email address to mentee
    mentors = db.StringListProperty() # email address to mentor
    gender = db.StringProperty() # male/female
    age = db.IntegerProperty() #
    mission = db.StringProperty() # 3 word tagline
    user_id=db.StringProperty(required=True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_email(cls, email):
        u = User.all().filter('email =', email).get()
        return u

    @classmethod
    def by_user_id(cls, user_id):
        u = User.all().filter('user_id =', user_id).get()
        return u    