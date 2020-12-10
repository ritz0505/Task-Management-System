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

class InsideTaskboard(webapp2.RequestHandler):
    def get(self):
        board_name=self.request.get('taskboard_name')
        #self.response.write(a)
        #if self.request.get('submitmember'):
        #self.response.write("hello")
        user = users.get_current_user()
        user_Details = ndb.Key('MyUser', user.email()).get()
        ab=user.email()
        a=re.sub('[^A-Za-z0-9]+','',ab)
        #self.response.write(a)
        unique_id=a+""+self.request.get('taskboard_name')
        #self.response.write(unique_id)
            #self.response.write(self.request.get('membername'))
        user = users.get_current_user()
        user_Details = ndb.Key('MyUser', user.email()).get()
        z=self.request.get('creater_address')
            #self.response.write(z)
        a=re.sub('[^A-Za-z0-9]+','',z)
            #self.response.write(a)
        member_name=[]
        #self.response.write(a)
        #self.response.write(unique_id)
        checking_member=ndb.Key('TaskBoard',unique_id)
        checking_member=checking_member.get()
        #self.response.write(checking_member)
        member_name=checking_member.team_member_added
        if self.request.get('membername') != "":
            if self.request.get('membername') not in member_name:
                if self.request.get('creater_address') != self.request.get('membername'):
                    unique_id=a+""+self.request.get('taskboard_name')
                    #self.response.write(unique_id)
                        #self.response.write(self.request.get('membername'))
                    if user.email() == self.request.get('creater_address'):
                        ab = ndb.Key(TaskBoard,unique_id).get()
                        self.response.write(ab)
                        ab.team_member_added.append(self.request.get('membername'))
                        ab.put()
                        var=re.sub('[^A-Za-z0-9]+','',z)
                        ma = ndb.Key(MyUser,self.request.get('membername')).get()
                        #self.response.write(ma)
                        if ma != None:
                            ma.taskboard_id.append(var+""+self.request.get('taskboard_name'))
                            user_Details.put()
                        else:
                            ma = MyUser(id=self.request.get('membername'))
                            ma.email_address = self.request.get('membername')
                            ma.taskboard_id.append(var+""+self.request.get('taskboard_name'))
                            ma.put()

                        #self.redirect('/ShowTaskboard')
                        #ma.taskboard_id.append(var+""+self.request.get('taskboard_name'))
                        #ma.put()
                    else:
                        self.response.write("Please contact admin of the taskboard to add a member.!!")
                else:
                    self.response.write("You cannot invite yourself to a taskboard.")
            else:
                self.response.write("Member you wish to add is already added to the taskboard")
        else:
            self.response.write("Member Invite Field cannot be empty.")

        template_values={
        'taskboard_name':self.request.get('taskboard_name')
        }
        template = JINJA_ENVIRONMENT.get_template('InsideTaskboard.html')
        self.response.write(template.render(template_values))
