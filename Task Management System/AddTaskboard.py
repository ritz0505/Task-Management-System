import webapp2
import jinja2
import re
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from MyUser import MyUser
from TaskBoard import TaskBoard


JINJA_ENVIRONMENT= jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

#**********************************Below code to add the user id and the taskboard name to the datastore******************
class AddTaskBoard(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        user_Details_Key = ndb.Key('MyUser', user.email())
        user_Details = user_Details_Key.get()
        button=self.request.get('submit')
        self.response.write(button)
        ab=user.email()
        a=re.sub('[^A-Za-z0-9]+','',ab)
        self.response.write(a)
        #board_name=ndb.key('TaskBoard',self.request.get('taskboard_name')).get()
        board_name=ndb.Key('TaskBoard',self.request.get('taskboard_name')).get()

        if board_name == None:
            rv=TaskBoard(id=a+""+self.request.get('taskboard_name'))
            rv.creater_address=user.email()
            rv.taskboard_name=self.request.get('taskboard_name')
            rv.put()
            self.response.write("added")

            abc=ndb.Key(MyUser,user.email()).get()
            unique_id=user.email()
            a=re.sub('[^A-Za-z0-9]+','',unique_id)
            self.response.write(a)
            ab = ndb.Key(MyUser,unique_id).get()
            self.response.write(ab)
            ab.taskboard_id.append(a+""+self.request.get('taskboard_name'))
            ab.put()

            self.redirect('/')
            self.response.write("Data Added successfully")
        else:
            self.response.write("TaskBoard with the given name already exists.")
