from app import db, Student, Instructor, Department, Course

def initDatabase():
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