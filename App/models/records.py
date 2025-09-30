from App.database import db

# hoursLogged

class Records(db.Model):
    __tablename__ = "records"
    record_id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    activity = db.Column(db.Text, nullable=True)
    hoursLogged = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='Pending')  # e.g., "Pending", "Approved", "Rejected"
    
    student = db.relationship('Student', backref='records', uselist=False)
    
    



    def __init__(self, studentID, description=None, hoursLogged=0, recordID=None, status='Pending'):
        self.studentID = studentID
        self.activity = description
        self.hoursLogged = hoursLogged
        self.record_id = recordID
        self.status = status


    def submitForConfirmation(self):
        """Mark record as pending confirmation."""
        self.status = "Pending"
        db.session.commit()


    def confirmHours(self):
        from App.models.student import Student
        """Confirm the hours in this record."""
        self.status = "Approved"
        student = Student.query.get(self.studentID)
        if student:
            student.totalHours += self.hoursLogged
        db.session.commit()

