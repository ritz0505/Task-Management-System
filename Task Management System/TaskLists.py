from google.appengine.ext import ndb
class TaskList(ndb.Model):
    #email address of this User
    taskboard_name=ndb.StringProperty(repeated=False)
    tasklist_name=ndb.StringProperty(repeated=False)
    task_due_date=ndb.StringProperty(repeated=False)
    task_status=ndb.StringProperty(repeated=False)
    task_assigned_to=ndb.StringProperty(repeated=False)
    date_completion=ndb.StringProperty(repeated=False)
    time_completion=ndb.StringProperty(repeated=False)
