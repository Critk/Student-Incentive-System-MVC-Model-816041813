from App.database import db
from App.models.student import Student

class Accolades(db.Model):
    __tablename__ = "accolades"
    rewardID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    requiredHours = db.Column(db.Integer, default=0)


    def __init__(self, rewardID, title, description=None, requiredHours=0):
        self.title = title
        self.rewardID = rewardID
        self.description = description
        self.requiredHours = requiredHours


    def checkEligibility(self, student):
        """Check if a student is eligible for this accolade."""
        return student.totalHours >= self.requiredHours
    

    def assignReward(self, student_id: int):
        """Assign this accolade to the student if eligible."""
        student = Student.query.get(student_id)
        if student and self.checkEligibility(student):
            if self not in student.accolades:
                student.accolades.append(self)
            db.session.commit()