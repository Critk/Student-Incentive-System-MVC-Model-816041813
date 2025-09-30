import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Student, Staff, Records, Accolades, Requests
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers
app = create_app()
migrate = get_migrate(app)


# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    sally = Student(studentID='sally', name='Sally Student', password='sallypass', email='sally@gmail.com', totalHours=10, incentivePoints=5)
    jones = Student(studentID='jones', name='Jones Student', password='jonespass', email = 'jones@gmail.com', totalHours=20, incentivePoints=15)
    Molly = Student(studentID='Molly', name='Molly Student', password='Mollypass', email = 'molly@gmail.com', totalHours=30, incentivePoints=25)
    dylan = Staff(staffID='dylan', name='Dylan Staff', password='dylanpass', email = 'dylanTec@gmailcom ', staffRole='Technician')
    jake = Staff(staffID='jake', name='Jake Staff', password='jakepass', email = 'jakeTec@gmailcom ', staffRole='Teacher')
    rec1 = Records(studentID='sally', description='Volunteering at local shelter', hoursLogged=5, recordID=1, status='Confirmed')
    rec2 = Records(studentID='jones', description='Community clean-up event', hoursLogged=10, recordID=2,  status='Confirmed')
    rec3 = Records(studentID='Molly', description='Tutoring younger students', hoursLogged=15, recordID=3, status='Confirmed')
    accolade1 = Accolades(rewardID=1, title='Bronze Volunteer', description='Awarded for logging 10 hours of community service', requiredHours=10)  
    accolade2 = Accolades(rewardID=2, title='Silver Volunteer', description='Awarded for logging 20 hours of community service', requiredHours=20)
    accolade3 = Accolades(rewardID=3, title='Gold Volunteer', description='Awarded for logging 30 hours of community service', requiredHours=30) 
    req1 = Requests(requestID=1, studentID='sally', status='Pending')
    req2 = Requests(requestID=2, studentID='jones', status='Pending')
    req3 = Requests(requestID=3, studentID='Molly', status='Pending') 
    db.session.add_all([sally, jones, Molly, dylan, jake, rec1, rec2, rec3, accolade1, accolade2, accolade3, req1, req2, req3])
    
    db.session.commit()
    print('database intialized')



'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands like create, list, update') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")  
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)    
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli


'''
Class Specific Commands
'''

student_request = AppGroup('student', help='Student make requests and view info')

@student_request.command("request")
@click.argument("student_id")
@click.argument("record_id", type=int)
@with_appcontext
def student_make_request(student_id, record_id):
    student = Student.query.get(student_id)
    record = Records.query.get(record_id)
    
    if not record:
        click.echo(f"Record {record_id} not found" )
        return
    req = student.make_request(record)
    if req:
        click.echo(f"Request created for {student.name} (Request ID: {req.requestID})")
    else:
        click.echo("Failed to create request")


@student_request.command("view_hours")
@click.argument("student_id")
@with_appcontext
def student_view_hours(student_id):
 
    student = Student.query.get(student_id)
    if not student:
        click.echo(f"Student {student_id} not found")
        return
    click.echo(f"{student.name} has {student.view_hours()} hours logged")


@student_request.command("view_accolades")
@click.argument("student_id")
@with_appcontext
def student_view_accolades(student_id):
    student = Student.query.get(student_id)
    if not student:
        click.echo(f"Student {student_id} not found")
        return
    accolades = student.view_accolades()
    if not accolades:
        click.echo(f"{student.name} has no accolades yet")
    else:
        click.echo(f"{student.name} has accolades: {', '.join([a.name for a in accolades])}")




@student_request.command("view_leaderboard")
@with_appcontext
def student_view_leaderboard():
    students = Student.query.order_by(Student.totalHours.desc()).all()
    click.echo("Leaderboard:")
    for s in students:
        click.echo(f"{s.name}: {s.totalHours} hours")

app.cli.add_command(student_request)

staff_comms = AppGroup('staff', help='Staff approve/reject requests')


# Staff Commands
@staff_comms.command("record_hours")
@click.argument("staff_id")
@click.argument("student_id")
@click.argument("hours", type=int)
@click.argument("activity_description")
@with_appcontext
def staff_record_hours(staff_id, student_id, hours, activity_description):

    staff = Staff.query.get(staff_id)
    if not staff:
        click.echo(f"Staff {staff_id} not found")
        return
    record = staff.record_hours(student_id, hours, activity_description)
    if record:
        click.echo(f"Recorded {hours} hours for student {student_id}")
    else:
        click.echo("Failed to record hours")



@staff_comms.command("confirm_request")
@click.argument("staff_id")
@click.argument("request_id", type=int)
@click.argument("approve", type=bool)
@with_appcontext
def staff_confirm_request(staff_id, request_id, approve):

    staff = Staff.query.get(staff_id)
    if not staff:
        click.echo(f"Staff {staff_id} not found")
        return
    success = staff.confirm_request(request_id, approve)
    click.echo("Request updated" if success else "Failed to update request")




@staff_comms.command("request_approve")
@click.argument("request_id", type=int)
@with_appcontext
def request_approve(request_id):

    req = Requests.query.get(request_id)
    if not req:
        click.echo(f"Request {request_id} not found")
        return
    if req.approveRequest():
        click.echo(f"Request {request_id} approved")
    else:
        click.echo("Failed to approve request")

@staff_comms.command("request_reject")
@click.argument("request_id", type=int)
@with_appcontext
def request_reject(request_id):
    req = Requests.query.get(request_id)
    if not req:
        click.echo(f"Request {request_id} not found")
        return
    if req.rejectRequest():
        click.echo(f"Request {request_id} rejected")
    else:
        click.echo("Failed to reject request")



# Records Commands (FOR STAFF ONLY)
@staff_comms.command("record_submit")
@click.argument("record_id", type=int)
@with_appcontext
def record_submit(record_id):
    record = Records.query.get(record_id)
    if not record:
        click.echo(f"Record {record_id} not found")
        return
    record.submitForConfirmation()
    click.echo(f"Record {record_id} submitted for confirmation")


@staff_comms.command("record_confirm")
@click.argument("record_id", type=int)
@with_appcontext
def record_confirm(record_id):
    record = Records.query.get(record_id)
    if not record:
        click.echo(f"Record {record_id} not found")
        return
    record.confirmHours()
    click.echo(f"Record {record_id} confirmed")


# Accolades Commands(FOR STAFF ONLY)
@staff_comms.command("accolade_assign")
@click.argument("accolade_id", type=int)
@click.argument("student_id")
@with_appcontext
def accolade_assign(accolade_id, student_id):
    accolade = Accolades.query.get(accolade_id)
    student = Records.query.get(student_id)
    if not accolade and not student:
        click.echo(f"Accolade {accolade_id} not found")
        return
    accolade.assignReward(student)
    click.echo(f"Accolade {accolade_id} assigned to student {student_id}")



@staff_comms.command("accolade_check")
@click.argument("accolade_id", type=int)
@click.argument("student_id")
@with_appcontext
def accolade_check(accolade_id, student_id):
    accolade = Accolades.query.get(accolade_id)
    student = Student.query.get(student_id)
    if not accolade or not student:
        click.echo("Invalid accolade or student")
        return
    eligible = accolade.checkEligibility(student)
    click.echo(f"Student {student_id} eligible for accolade {accolade_id}: {eligible}")


app.cli.add_command(staff_comms)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))




app.cli.add_command(test)




