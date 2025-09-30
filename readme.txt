
flask init - Initialize Database

flask user create - Create a User

flask user list - List Users


Student Commands

flask student request <student_id> <record_id> - Make a Request

flask student view_hours <student_id> - View Logged Hours

flask student view_accolades <student_id> - View Accolades

flask student view_leaderboard - View Leaderboard



Staff Commands

flask staff record_hours <staff_id> <student_id> <activity_description> - Record Hours for a Student

flask staff confirm_request <staff_id> <request_id> # approve = True/False - Confirm or Reject a Request

flask staff request_approve <request_id> - Approve Request Directly

flask staff request_reject <request_id> - Reject Request Directly

flask staff record_submit <record_id> - Submit Record for Confirmation

flask staff record_confirm <record_id> - Confirm Hours for a Record

flask staff accolade_assign <accolade_id> <student_id> - Assign Accolade to Student

flask staff accolade_check <accolade_id> <student_id> - Check Student Eligibility for Accolade

