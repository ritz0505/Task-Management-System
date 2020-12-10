from google.appengine.ext import ndb
class TaskBoard(ndb.Model):
    #email address of this User
    creater_address = ndb.StringProperty(repeated=False)
    taskboard_name=ndb.StringProperty(repeated=False)
    team_member_added=ndb.StringProperty(repeated=True)
    task_id=ndb.StringProperty(repeated=True)
