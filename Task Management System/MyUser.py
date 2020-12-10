from google.appengine.ext import ndb
class MyUser(ndb.Model):
    #email address of this User
    email_address = ndb.StringProperty(repeated=False)
    taskboard_id=ndb.StringProperty(repeated=True)
