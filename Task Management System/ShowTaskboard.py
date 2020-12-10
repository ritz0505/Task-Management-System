import webapp2
import jinja2
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

#****************************Below code to show the taskboards name on the screen*********************************
class ShowTaskboard(webapp2.RequestHandler):
    def get(self):
        #self.response.write("hi")
        result=[]
        user = users.get_current_user()
        value=ndb.Key('MyUser',user.email()).get()
        ab=value.taskboard_id
        #self.response.write(ab)
        #self.response.write(value)
        if ab == None:
            self.response.write("No Taskboard has been added yet")

        else:

            if value != None:
                taskboardlist=value.taskboard_id
                #self.response.write(taskboardlist)

                for i in taskboardlist:
                    taskboard=ndb.Key('TaskBoard',i).get()
                    result.append(taskboard)

            else:
                self.response.write("No Taskboard has been added yet")
            #self.response.write(result)
        #abc = abc.taskboard_id
        #self.response.write(abc)
        template_values={
        'result':result
        }
        template = JINJA_ENVIRONMENT.get_template('ShowTaskboard.html')
        self.response.write(template.render(template_values))
