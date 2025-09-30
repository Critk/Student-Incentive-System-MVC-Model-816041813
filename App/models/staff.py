from App.database import db
from App.models.user import User
from App.models.student import Student


class Staff(User):
    __tablename__ = "staff"
    staffID = db.Column(db.String(20), db.ForeignKey('user.user_id'), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref='staff', uselist=False)
    


    def __init__(self, staffID, password, name, email, staffRole):
        super().__init__(username=staffID, password=password)
        self.staffID = staffID
        self.name = name
        self.email = email
        self.position = staffRole


    def record_hours(self, student_id: int, hours: int, description: str):
        """Record hours for a student."""
        from App.models.records import Records

        student = Student.query.get(student_id)
        if not student:
            return None
        
        new_record = Records(
            studentID=student_id,
            description=description,
            hoursLogged=hours,
            status='Confirmed'
        )
        student.totalHours += hours
        db.session.add(new_record)
        db.session.commit()
        return new_record    


    def confirm_request(self, request_id: int, approve: bool = True):
        """Approve or reject a request."""
        from App.models.requests import Requests
        req = Requests.query.get(request_id)
        if not req:
            return False
        
        if approve:
            req.approveRequest()
        else:
            req.rejectRequest()
        db.session.commit()
        return True


    def manage_accolades(self, student_id: int):
        """Assign eligible accolades to a student."""
        from App.models.accolades import Accolades

        student = Student.query.get(student_id)
        if not student:
            return None
        for accolade in Accolades.query.all():
            if accolade.checkEligibility(student):
                accolade.assignReward(student)
        db.session.commit()
        return student.studentID

