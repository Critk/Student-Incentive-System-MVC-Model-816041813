from App.database import db


class Requests(db.Model):
    __tablename__ = "requests"
    requestID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey('student.studentID'), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # e.g., "Pending", "Approved", "Rejected"


    student = db.relationship('Student', backref='requests', uselist=False)
    

    def __init__(self, requestID, studentID, status="Pending"):
        self.requestID = requestID
        self.studentID = studentID
        self.status = status


    def approveRequest(self):
        """Approve the request and update student's total hours."""
        if self.status != 'Pending':
            return False  # Only pending requests can be approved
        
        self.status = 'Approved'
        self.student.totalHours += int(self.description)  # Assuming description holds hours for simplicity
        db.session.commit()
        return True
    

    def rejectRequest(self):
        """Reject the request."""
        if self.status != 'Pending':
            return False  # Only pending requests can be rejected
        
        self.status = 'Rejected'
        db.session.commit()
        return True
    

    