import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import re
from MyUser import MyUser
from AddTaskboard import AddTaskBoard
from TaskBoard import TaskBoard
from ShowTaskboard import ShowTaskboard
from InsideTaskboard import InsideTaskboard
#from AllTasks import showTasks
from AddFetchTask import AddFetchTask
from fetchTask import fetchTask
from TaskLists import TaskList
from datetime import datetime

JINJA_ENVIRONMENT= jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type']='text/html'
            # URL that will contain a login or logout link
            # and also a string to represent this
            url=''
            url_string=''
            name=''
            welcome='Welcome back'
            # pull the current user from the request
            url=users.create_login_url(self.request.uri)
            url_string='login'
            user = users.get_current_user()

            if user:
                template = JINJA_ENVIRONMENT.get_template('taskboardadd.html')
                self.response.write(template.render())
                url=users.create_logout_url(self.request.uri)
                url_string = 'logout'
                user_Details_Key = ndb.Key('MyUser', user.email())
                user_Details = user_Details_Key.get()
                if user_Details != None:
                     user_Details.email_address = user.email()
                     user_Details.put()
                else:
                     user_Details = MyUser(id=user.email())
                     user_Details.email_address = user.email()
                     user_Details.put()

            else:
                url=users.create_login_url(self.request.uri)
                url_string='login'

            template_values={
            'url' :url,
            'url_string' : url_string,
            'user' : user,
            'welcome':welcome
        }
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

class ClickTaskboard(webapp2.RequestHandler):
    def get(self):
        creater_address=self.request.get('creater_address')
        taskboard=self.request.get('taskboard_name')
        ab=MyUser.query().fetch()
        #self.response.write(taskboard)
        #self.response.write(creater_address)
        template_values={
        'taskboard_name':taskboard,
        'creater_address':creater_address,
        'ab':ab
        }
        template = JINJA_ENVIRONMENT.get_template('InsideTaskboard.html')
        self.response.write(template.render(template_values))

class TaskEditLink(webapp2.RequestHandler):
    def get(self):
        id=self.request.get('taskboard_name')+""+self.request.get('tasklist_name')
        data=ndb.Key('TaskList',id).get()
        task_status=data.task_status
        if task_status == "Completed":
            self.response.write("Task is already completed. You cannot edit it now.")
        else:
            taskboard_name=self.request.get('taskboard_name')
            creater_address=self.request.get('creater_address')
            tasklist_name=self.request.get('tasklist_name')
            task_assigned_to=self.request.get('task_assigned_to')
            task_due_date=self.request.get('task_due_date')
            template_values={
            'creater_address':creater_address,
            'taskboard_name':taskboard_name,
            'tasklist_name':tasklist_name,
            'task_assigned_to':task_assigned_to,
            'task_due_date':task_due_date
            }
            template = JINJA_ENVIRONMENT.get_template('TaskEditPage.html')
            self.response.write(template.render(template_values))

class EditTaskList(webapp2.RequestHandler):
    def get(self):
        completiondatetime=datetime.now()
        date=completiondatetime.strftime('%Y-%m-%d')
        date1=self.request.get('duedatenew')
        if date1 < date:
            self.response.write("Date prior to current date not allowed")
        else:
            creater_address=self.request.get('creater_address')
            taskboard_name=self.request.get('taskboard_name')
            tasklist_name=self.request.get('tasklist_name')
            task_assigned_to=self.request.get('task_assigned_to')
            task_due_date=self.request.get('task_due_date')
            template_values={
            'creater_address':creater_address,
            'taskboard_name':taskboard_name,
            'tasklist_name':tasklist_name,
            'task_assigned_to':task_assigned_to,
            'task_due_date':task_due_date
            }
            #self.response.write("hi")

            id=self.request.get('boardname')+""+self.request.get('taskname')
            #self.response.write(id)
            dbs=ndb.Key('TaskList',id).get()
            #self.response.write(dbs)
            dbs.key.delete()

            #self.response.write(self.request.get('creater_address'))
            #self.response.write(self.request.get('taskboard_name'))
            a=re.sub('[^A-Za-z0-9]+','',creater_address)
            id1=a+""+self.request.get('boardname')
            dbs1=ndb.Key('TaskBoard',id1).get()
            #self.response.write(dbs1)
            dbs1.task_id.remove(self.request.get('boardname')+""+self.request.get('taskname'))
            dbs1.put()


            data=TaskList(id=self.request.get('boardnamenew')+""+self.request.get('tasknamenew'))
            data.taskboard_name=self.request.get('boardnamenew')
            data.tasklist_name=self.request.get('tasknamenew')
            data.task_due_date=self.request.get('duedatenew')
            data.task_assigned_to=self.request.get('membernamenew')
            data.put()

            #self.response.write(self.request.get('creater_address'))
            #self.response.write(self.request.get('boardnamenew'))
            a=re.sub('[^A-Za-z0-9]+','',creater_address)
            id1=a+""+self.request.get('boardnamenew')
            #self.response.write(id1)
            taskvalue=ndb.Key(TaskBoard,id1).get()
            #self.response.write(taskvalue)
            taskvalue.task_id.append(self.request.get('boardnamenew')+""+self.request.get('tasknamenew'))
            taskvalue.put()

        template = JINJA_ENVIRONMENT.get_template('TaskEditPage.html')
        self.response.write(template.render())

class DeleteTaskClass(webapp2.RequestHandler):
    def get(self):
        creater_address=self.request.get('creater_address')
        taskboard_name=self.request.get('taskboard_name')
        tasklist_name=self.request.get('tasklist_name')
        task_assigned_to=self.request.get('task_assigned_to')
        task_due_date=self.request.get('task_due_date')
        template_values={
        'creater_address':creater_address,
        'taskboard_name':taskboard_name,
        'tasklist_name':tasklist_name,
        'task_assigned_to':task_assigned_to,
        'task_due_date':task_due_date
        }
        id=self.request.get('boardnamenew')+""+self.request.get('taskname')
        #self.response.write(id)
        dbs=ndb.Key('TaskList',id).get()
        #self.response.write(dbs)
        dbs.key.delete()

        #self.response.write(self.request.get('creater_address'))
        #self.response.write(self.request.get('taskboard_name'))
        a=re.sub('[^A-Za-z0-9]+','',creater_address)
        id1=a+""+self.request.get('boardnamenew')
        dbs1=ndb.Key('TaskBoard',id1).get()
        #self.response.write(dbs1)
        dbs1.task_id.remove(self.request.get('boardname')+""+self.request.get('taskname'))
        dbs1.put()
        self.redirect('/ShowTaskboard')
        #template = JINJA_ENVIRONMENT.get_template('TaskEditPage.html')
        #self.response.write(template.render(template_values))

class Status(webapp2.RequestHandler):
    def get(self):
        taskboard_name=self.request.get('taskboard_name')
        tasklist_name=self.request.get('tasklist_name')
        completiondatetime=datetime.now()
        date=completiondatetime.strftime('%Y-%m-%d')
        time=completiondatetime.strftime("%I:%M:%S %p")
        abc=ndb.Key(TaskList,taskboard_name+""+tasklist_name).get()
        abc.task_status='Completed'
        abc.date_completion=date
        abc.time_completion=time
        abc.put()
        #self.response.write(tasklist_name)

        template = JINJA_ENVIRONMENT.get_template('AllTasks.html')
        self.response.write(template.render())

app= webapp2.WSGIApplication([('/',MainPage),('/AddTaskBoard',AddTaskBoard),('/ShowTaskboard',ShowTaskboard),
('/ClickTaskboard',ClickTaskboard),('/InsideTaskboard',InsideTaskboard),
('/AddFetchTask',AddFetchTask),('/fetchTask',fetchTask),('/TaskEditLink',TaskEditLink),('/EditTaskList',EditTaskList),('/Status',Status),
('/DeleteTaskClass',DeleteTaskClass)],debug=True)
