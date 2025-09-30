Flask CLI Commands for Student Incentive Program

# Initialize Database
flask init

# User Commands
## Create a User
flask user create <username> <password>
## List Users
flask user list [format]  # format: string (default) or json

# Student Commands
## Make a Request
flask student request <student_id> <record_id>
## View Logged Hours
flask student view_hours <student_id>
## View Accolades
flask student view_accolades <student_id>
## View Leaderboard
flask student view_leaderboard

# Staff Commands
## Record Hours for a Student
flask staff record_hours <staff_id> <student_id> <hours> <activity_description>
## Confirm or Reject a Request
flask staff confirm_request <staff_id> <request_id> <approve>  # approve = True/False
## Approve Request Directly
flask staff request_approve <request_id>
## Reject Request Directly
flask staff request_reject <request_id>
## Submit Record for Confirmation
flask staff record_submit <record_id>
## Confirm Hours for a Record
flask staff record_confirm <record_id>
## Assign Accolade to Student
flask staff accolade_assign <accolade_id> <student_id>
## Check Student Eligibility for Accolade
flask staff accolade_check <accolade_id> <student_id>

# Test Commands
## Run User Tests
flask test user [type]  # type: unit, int, all (default)

