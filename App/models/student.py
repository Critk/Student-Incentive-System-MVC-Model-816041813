from App.database import db
from App.models.user import User
from App.models.records import Records



class Student(User):
    __tablename__ = "student"
    studentID = db.Column(db.String(20), db.ForeignKey('user.user_id'), primary_key=True)  # e.g., roll number
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    totalHours = db.Column(db.Integer, default=0)
    incentivePoints = db.Column(db.Integer, default=0)

    user = db.relationship('User', backref='student', uselist=False)
    

    

    def __init__(self, studentID, name, password, email, totalHours=0, incentivePoints=0 ):
        super().__init__(username=studentID, password=password)
        self.studentID = studentID
        self.name = name
        self.email = email
        self.totalHours = totalHours
        self.incentivePoints = incentivePoints


    def make_request(self, record):
        """Create a new request based on a specific record."""
        from App.models.requests import Requests
        records = Records.query.get(record)
        if not records:
            return None
        
        new_request = Requests(
            requestID=None,
            studentID=self.studentID,
            status="Pending"
        )

        db.session.add(new_request)
        db.session.commit()
        return new_request

    def view_hours(self):
        """Return total hours logged."""
        return self.totalHours

    def view_accolades(self):
        """Return list of accolades the student has earned."""
        from App.models.accolades import Accolades
        return [a for a in self.accolades if a.checkEligibility(self)]

    def view_leaderboard(self):
        """Return top students by totalHours."""
        return Student.query.order_by(Student.totalHours.desc()).all()   


    
       
        
