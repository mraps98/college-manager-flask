from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
db = SQLAlchemy(app)

enrolled_in = db.Table('enrolled_in', 
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    advisor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    courses = db.relationship('Course',secondary=enrolled_in, backref='students_enrolled', lazy='select')
    def __repr__(self):
        return '<Student %r>' % self.fname

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(40), nullable=False)
    lname = db.Column(db.String(40), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    studentsAdvised = db.relationship('Student',backref='advisor', lazy='select')
    courses = db.relationship('Course',backref='instructor',lazy='select')
    department_in_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    department_head_of_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    def __repr__(self):
        return '<Instructor %r>' % self.fname

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    instructors = db.relationship('Instructor',foreign_keys='Instructor.department_in_id', backref='department_in',lazy='select')
    head = db.relationship('Instructor', foreign_keys='Instructor.department_head_of_id', backref='department_head_of',lazy='select',uselist=False)
    courses = db.relationship('Course',backref='department',lazy='select')
    studentsMajored = db.relationship('Student',backref='major',lazy='select')
    def __repr__(self):
        return '<Department %r>' % self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False, unique=True)
    name = db.Column(db.String(40), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    def __repr__(self):
        return '<Course %r>' % self.name

# HomePage
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/resetdb")
def resetdb():
    db.drop_all()
    db.create_all()

    preet = Student(fname='Amritpreet', lname='Singh', dob='1998-10-04')
    prasansha = Student(fname='Prasansha', lname='Bhandari', dob='1997-12-01')
    faiq = Student(fname='Faiq', lname='Bin Zahid', dob='1997-11-22')
    nisha = Student(fname='Nisha', lname='Shahi', dob='1995-03-22')
    tarique = Student(fname='Tarique', lname='Chowdhury', dob='1998-10-22')

    tony = Instructor(fname='Tony', lname='Nacional', dob='1970-12-20')
    marco = Instructor(fname='Marco', lname='Niniimaki', dob='1960-12-05')
    mario = Instructor(fname='Mario', lname='Garcia', dob='1970-12-02')
    reshmi = Instructor(fname='Reshmi', lname='Mitra', dob='1985-03-10')
    xuesang = Instructor(fname='Xuesang', lname='Zhang', dob='1950-06-23')
    cs = Department(name='Computer Science')
    cy = Department(name='Cyber Security')
    cs101 = Course(code='CS101', name='Intro to Computer Science')
    cs155 = Course(code='CS155', name='Introduction to Java')
    cs201 = Course(code='CS201', name='Advanced Java')
    cs591 = Course(code='CS591', name='Advanced Artiifical Intelligence')
    cy501 = Course(code='CY501', name='Intro to CyberSecurity')
    cy520 = Course(code='CY520', name='Information Security')

    preet.courses.extend((cs591,cy501))
    prasansha.courses.extend((cs101, cs155))
    nisha.courses.extend((cy501, cy520))
    tarique.courses.append(cs201)
    faiq.courses.append(cy520)

    tony.courses.extend((cs101, cs155))
    tony.studentsAdvised.append(prasansha)

    marco.courses.append(cs201)
    marco.studentsAdvised.append(preet)

    reshmi.courses.append(cy501)
    reshmi.studentsAdvised.append(faiq)

    xuesang.courses.append(cs591)
    xuesang.studentsAdvised.append(tarique)

    mario.courses.append(cy520)
    mario.studentsAdvised.append(nisha)

    cs.studentsMajored.extend((preet, prasansha))
    cs.instructors.extend((tony, marco, xuesang))
    cs.head = marco
    cs.courses.extend((cs101,cs155,cs201, cs591))

    cy.studentsMajored.extend((faiq, nisha, tarique))
    cy.head = reshmi
    cy.instructors.extend((reshmi, mario))
    cy.courses.extend((cy501, cy520))

    db.session.add(preet)
    db.session.add(prasansha)
    db.session.add(tarique)
    db.session.add(faiq)
    db.session.add(nisha)
    db.session.add(tony)
    db.session.add(marco)
    db.session.add(mario)
    db.session.add(reshmi)
    db.session.add(xuesang)
    db.session.add(cs)
    db.session.add(cs101)
    db.session.add(cs155)
    db.session.add(cs201)
    db.session.add(cs591)
    db.session.add(cy)
    db.session.add(cy501)
    db.session.add(cy520)
    db.session.commit()
    return redirect("/")

# Student
@app.route("/student")
def getStudents():
    students = Student.query.all()
    return render_template('student/index.html',students = students)


@app.route("/student/add", methods=['GET','POST'])
def addStudent():
    if request.method=='GET':
        instructors = Instructor.query.all()
        departments = Department.query.all()
        return render_template('student/add.html', instructors=instructors, departments=departments)
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        advisor_id = request.form['advisor_id']
        major_id = request.form['major_id']

        s1 = Student(fname=fname, lname=lname, dob=dob, advisor_id=advisor_id, major_id=major_id)
        db.session.add(s1)
        db.session.commit()
        return redirect("/student")

@app.route("/student/<id>/update", methods=['GET'])
@app.route("/student/update", methods=['POST'])
def updateStudent(id=None):
    if request.method=='GET':
        if not id:
            return "No id was passed in the query string. Please go back and try again."
        instructors = Instructor.query.all()
        departments = Department.query.all()
        student = Student.query.filter_by(id=id).first_or_404()
        return render_template('/student/update.html', instructors=instructors, departments=departments, student=student)
    else:
        s1 = Student.query.filter_by(id = request.form['id']).first_or_404()
        s1.fname = request.form['fname']
        s1.lname = request.form['lname']
        s1.dob = request.form['dob']
        s1.advisor_id = request.form['advisor_id']
        s1.major_id = request.form['major_id']
        db.session.commit()
        return redirect("/student")

@app.route("/student/<id>/courses")
def getCoursesbyStudent(id):
    if not id:
        return "No id was passed in the query string. Please go back and try again."
    student = Student.query.filter_by(id=id).first_or_404()
    courses = Course.query.all()
    for course in student.courses:
        courses.remove(course)
    return render_template('student/courses.html', student=student, courses=courses)
        
@app.route("/student/enroll", methods=['POST'])
def enrollStudentInCourse():
    student = Student.query.filter_by(id=request.form['student_id']).first_or_404()
    course = Course.query.filter_by(id=request.form['course_id']).first_or_404()
    student.courses.append(course)
    db.session.commit()
    if request.form['redirect_to'] == 'student':
        return redirect("/student/"+request.form['student_id']+"/courses")
    else:
        return redirect("/course/"+request.form['course_id']+'/students')

@app.route("/student/unenroll", methods=['POST'])
def unenrollStudentFromCourse():
    student = Student.query.filter_by(id=request.form['student_id']).first_or_404()
    course = Course.query.filter_by(id=request.form['course_id']).first_or_404()
    student.courses.remove(course)
    db.session.commit()
    if request.form['redirect_to'] == 'student':
        return redirect("/student/"+request.form['student_id']+"/courses")
    else:
        return redirect("/course/"+request.form['course_id']+"/students")

# Instructor
@app.route("/instructor")
def getInstructors():
    instructors = Instructor.query.all()
    return render_template('instructor/index.html',instructors=instructors)

@app.route("/instructor/add", methods=['POST','GET'])
def addInstructor():
    if request.method=='GET':
        departments = Department.query.all()
        return render_template('instructor/add.html', departments=departments)
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        dob = request.form['dob']
        department_in_id = request.form['department_in_id']
        i1 = Instructor(fname=fname, lname=lname, dob=dob, department_in_id=department_in_id)
        db.session.add(i1)
        db.session.commit()
        return redirect("/instructor")

@app.route("/instructor/<id>/update", methods=['GET'])
@app.route("/instructor/update", methods=['POST'])
def updateInstructor(id=None):
    if request.method=='GET':
        if not id:
            return 'No id provided in paremetrs. Please go back and try again.'
        departments = Department.query.all()
        instructor = Instructor.query.filter_by(id=id).first_or_404()
        print(instructor)
        return render_template('instructor/update.html', instructor=instructor, departments=departments)
    else:
        i1 = Instructor.query.filter_by(id=request.form['id']).first_or_404()
        i1.fname = request.form['fname']
        i1.lname = request.form['lname']
        i1.dob = request.form['dob']
        i1.department_in_id = request.form['department_in_id']
        print(i1)
        db.session.commit()
        return redirect("/instructor")

@app.route("/instructor/<id>/courses")
def getCoursesByInstructor(id=None):
    if not id:
        return 'No id provided in parameters. Please go back and try again'
    else:
        instructor = Instructor.query.filter_by(id=id).first_or_404()
        return render_template('instructor/courses.html', instructor=instructor)

# Course
@app.route("/course")
def getCourses():
    courses = Course.query.all()
    return render_template('course/index.html', courses=courses)

@app.route("/course/add", methods=['GET','POST'])
def addCourse():
    if request.method == 'GET':
        instructors = Instructor.query.all()
        departments = Department.query.all()
        return render_template('course/add.html', instructors=instructors, departments=departments)
    else:
        code = request.form['code']
        name = request.form['name']
        instructor_id = request.form['instructor_id']
        department_id = request.form['department_id']

        c1 = Course(code=code, name=name, instructor_id=instructor_id, department_id=department_id)
        db.session.add(c1)
        db.session.commit()
        return redirect("/course")

@app.route("/course/<id>/update",methods=['GET'])
@app.route("/course/update", methods=['POST'])
def updateCourse(id=None):
    if request.method == 'GET':
        if not id:
            return 'No id provided in parameters. Please go back and try again'
        course = Course.query.filter_by(id=id).first_or_404()
        departments = Department.query.all()
        instructors = Instructor.query.all()
        return render_template('course/update.html', course = course, departments=departments, instructors=instructors)
    else:
        c1 = Course.query.filter_by(id=request.form['id']).first_or_404()
        c1.code = request.form['code']
        c1.name = request.form['name']
        c1.instructor_id = request.form['instructor_id']
        c1.department_id = request.form['department_id']
        db.session.commit()
        return redirect("/course")

@app.route("/course/<id>/students")
def getStudentsByCourses(id=None):
    if not id:
        return 'No id was provided in the paremeters. Please go back and try again'
    course=Course.query.filter_by(id=id).first_or_404()
    students = Student.query.all()
    for student in course.students_enrolled:
        students.remove(student)
    return render_template('course/students.html',course = course, students=students)

# Department
@app.route("/department")
def getDepartments():
    departments = Department.query.all()
    return render_template('department/index.html', departments=departments)

@app.route("/department/add", methods=['POST','GET'])
def addDepartment():
    if request.method =='GET':
        instructors = Instructor.query.all()
        return render_template('department/add.html', instructors=instructors)
    else:
        name = request.form['name']
        if request.form['head_id'] != '-1':
            head_id = request.form['head_id']
            d1 = Department(name=name, head_id=head_id)
        else:
            d1=Department(name=name)
        db.session.add(d1)
        db.session.commit()
        return redirect("/department")

@app.route("/department/<id>/update", methods=['GET'])
@app.route("/department/update", methods=['POST'])
def updateDepartment(id=None):
    if request.method =='GET':
        if not id:
            return 'No id entered in parameters. Please go back and try again'
        department = Department.query.filter_by(id=id).first_or_404()
        instructors = Instructor.query.all()
        return render_template('department/update.html', department=department, instructors=instructors)
    else:
        d1 = Department.query.filter_by(id=request.form['id']).first_or_404()
        d1.name = request.form['name']
        if request.form['head_id'] != '-1':
            d1.head = Instructor.query.filter_by(id=request.form['head_id']).first_or_404()
        db.session.commit()
        return redirect("/department")
            
@app.route('/department/<id>/instructors')
def getInstructorsByDepartment(id):
    if not id:
        return 'No id provided in parameters. Please go back and try again'
    department = Department.query.filter_by(id=id).first_or_404()
    return render_template('department/instructors.html', department=department)

@app.route('/department/makehead', methods=['POST'])
def makeHead():
    d1 = Department.query.filter_by(id=request.form['department_id']).first_or_404()
    i1 = Instructor.query.filter_by(id=request.form['instructor_id']).first_or_404()
    d1.head = i1
    db.session.commit()
    return redirect('/department/'+request.form['department_id']+'/instructors')

if __name__ == '__main__':
    app.run(debug=True)
