from app import db, Student, Instructor, Department, Course

def initDatabase():
    db.drop_all()
    db.create_all()

    preet = Student(fname='Amritpreet', lname='Singh', dob='1998-10-04')
    prasansha = Student(fname='Prasansha', lname='Bhandari', dob='1997-12-01')
    tony = Instructor(fname='Tony', lname='Nacional', dob='1970-12-20')
    marco = Instructor(fname='Marco', lname='Niniimaki', dob='1960-12-05')
    cs = Department(name='Computer Science')
    cs101 = Course(code='CS101', name='Intro to Computer Science')
    cs155 = Course(code='CS155', name='Introduction to Java')
    cs201 = Course(code='CS201', name='Advanced Java')

    preet.courses.append(cs201)

    prasansha.courses.extend((cs101, cs155))

    tony.courses.extend((cs101, cs155))
    tony.studentsAdvised.append(prasansha)

    marco.courses.append(cs201)
    marco.studentsAdvised.append(preet)

    cs.studentsMajored.extend((preet, prasansha))
    cs.instructors.extend((tony, marco))
    cs.head = marco
    cs.courses.extend((cs101,cs155,cs201))



    db.session.add(preet)
    db.session.add(prasansha)
    db.session.add(tony)
    db.session.add(marco)
    db.session.add(cs)
    db.session.add(cs101)
    db.session.add(cs155)
    db.session.add(cs201)
    db.session.commit()