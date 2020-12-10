import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import re
from MyUser import MyUser
from TaskBoard import TaskBoard
from TaskLists import TaskList

JINJA_ENVIRONMENT= jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class fetchTask(webapp2.RequestHandler):
    def get(self):
        result=[]
        user = users.get_current_user()
        value=self.request.get('taskboard_name')
        #self.response.write(value)
        creater_address=self.request.get('creater_address')
        #self.response.write(creater_address)
        result=[]
        highlightvalue={}

        #user = users.get_current_user()

        unique_id=self.request.get('creater_address')
        a=re.sub('[^A-Za-z0-9]+','',unique_id)
        #self.response.write(a)
        id=a+""+self.request.get('taskboard_name')
        value=ndb.Key('TaskBoard',id).get()
        #self.response.write(value)
        #self.response.write(ab)
        #self.response.write(value)
        if value != None:
            tasklist=value.task_id
                #self.response.write(taskboardlist)

            for i in tasklist:
                tasks=ndb.Key('TaskList',i).get()
                result.append(tasks)
                #self.response.write(result)

                #if tasks.task_assigned_to == "":
                #    highlightvalue=tasks.tasklist_name
                #    self.response.write(highlightvalue)
                #else:
                #    self.response.write("hello")

        else:
            self.response.write("No Taskboard has been added yet")

        if len(result) == 0:
            self.response.write("No Task has been added yet.")

        template_values={
        'result':result,
        #'highlightvalue':highlightvalue,
        'creater_address':creater_address
        }
        template = JINJA_ENVIRONMENT.get_template('AllTasks.html')
        self.response.write(template.render(template_values))
