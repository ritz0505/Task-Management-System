import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import re
from datetime import datetime
from MyUser import MyUser
from TaskBoard import TaskBoard
from TaskLists import TaskList

JINJA_ENVIRONMENT= jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AddFetchTask(webapp2.RequestHandler):
    def get(self):
        msg=None
        taskboard_name=self.request.get('taskboard_name')
        #self.response.write(taskboard_name)
        creater_address=self.request.get('creater_address')
        #self.response.write(taskboard_creator)
        #self.response.write(taskboard_name)
        ab=MyUser.query().fetch()
        button=self.request.get('add')
        #self.response.write(button)
        if button=="add":
            completiondatetime=datetime.now()
            date=completiondatetime.strftime('%Y-%m-%d')
            date1=self.request.get('duedate')
            if self.request.get('taskname') != "":
                if date1 != "":
                    if date1 < date:
                        self.response.write("Date prior to current date not allowed")
                    else:
                        id=self.request.get('boardname')+""+self.request.get('taskname')
                        #self.response.write(id)
                        value=ndb.Key(TaskList,id).get()
                        #self.response.write(value.tasklist_name)
                        if value==None:
                            data=TaskList(id=self.request.get('boardname')+""+self.request.get('taskname'))
                            data.taskboard_name=self.request.get('boardname')
                            data.tasklist_name=self.request.get('taskname')
                            data.task_due_date=self.request.get('duedate')
                            data.task_assigned_to=self.request.get('membername')
                            data.put()

                            #self.response.write(self.request.get('creater_address'))
                            #self.response.write(self.request.get('boardname'))
                            a=re.sub('[^A-Za-z0-9]+','',creater_address)
                            id1=a+""+self.request.get('boardname')
                            #self.response.write(id1)
                            taskvalue=ndb.Key(TaskBoard,id1).get()
                            #self.response.write(taskvalue)
                            taskvalue.task_id.append(self.request.get('boardname')+""+self.request.get('taskname'))
                            taskvalue.put()

                            self.response.write("Task Name added.")
                            self.redirect('/fetchTask')

                            template_values={
                            'taskboard_name':taskboard_name,
                            'creater_address':creater_address,
                            'ab':ab,
                            'msg':msg
                            }
                            template = JINJA_ENVIRONMENT.get_template('TaskListsAddPage.html')
                            self.response.write(template.render(template_values))

                        else:
                            self.response.write("Data with same task name cannot be added! Please go back to add another name.")
                            #self.redirect('/ShowTaskboard')
                    #self.response.write("Task Added")

                else:
                    self.response.write("Date field is empty. Please go back first to add the date.")
            else:
                self.response.write("TaskName cannot be  empty. please go back to add the taskname")


        template_values={
        'taskboard_name':taskboard_name,
        'creater_address':creater_address,
        'ab':ab,
        'msg':msg
        }
        template = JINJA_ENVIRONMENT.get_template('TaskListsAddPage.html')
        self.response.write(template.render(template_values))
