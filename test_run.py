import pymongo
import impclasses as imp
from bson.objectid import ObjectId

myDB = pymongo.MongoClient("mongodb://localhost:27017/")

classroomPlusDB = myDB["classroomPlus"]


usersDB = classroomPlusDB["users"]
classesDB = classroomPlusDB["classes"]
#################################################################
def authuser(userName,password):

    auth_query = {'user_name':userName}

    required = list(usersDB.find(auth_query))

    if len(required) == 0:
        print("No Username Matched")
        return False
    elif len(required) == 1:
        if required[0]['password']==password:
            print("Password Match")
            return True
        else:
            print("Password Not Match")
            return False
    else:
        print("Multiple Users have same UserNames")
        return False

################################################################

def profile(userName):

    profile_query = {'user_name':userName}
    required = list(usersDB.find(profile_query))
    print("Your Profile")
    print(required[0])

################################################################

def teachermenu(userName):

    while True:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("Menu")
        print("1) View Profile")
        print("2) Create a Class")
        print("3) View Created Classes")
        print("4) Delete a Class")
        print("5) Logout")
        choice=int(input("Select your Choice :"))

        if choice==1:
            #user profile VERIFIED
            profile(userName)
            continue

        elif choice==2:
            #Create a classroom VERIFIED
            id_query = {'user_name':userName}
            required = list(usersDB.find(id_query))
            userID = required[0]['_id']
            classes_created = required[0]['classes']

            class_subject = input("Enter Subject of the Classroom :")
            class_code = 0
            while True:
                class_code = input("Enter Code of the Classroom")
                code_query = {'class_code':class_code}
                code_required = list(classesDB.find(code_query))
                if len(code_required)==0:
                    print("Code Accepted")
                    break
                else:
                    print("Class Code Already in Use")
                    continue

            class_data={
            'class_code':class_code,
            'subject':class_subject,
            'teacherID':userID,
            'studentsIDs':[]
            }

            insert_class = classesDB.insert_one(class_data)
            classroom_code = class_code

            classes_created.append(classroom_code)
            newclasses = {"$set":{'classes':classes_created}}
            usersDB.update_one(id_query,newclasses)

            print("Updated Profile")
            profile(userName)
            continue

        elif choice == 3:
            #list of classes created VERIFIED
            id_query = {'user_name':userName}
            required = list(usersDB.find(id_query))
            classes_created = required[0]['classes']

            print("List of Classes Created")
            for i in classes_created:
                print(i)
            continue

        elif choice == 4:
            #delete a created class
            id_query = {'user_name':userName}
            required = list(usersDB.find(id_query))
            userID = required[0]['_id']
            classes_created = required[0]['classes']


            class_code = input("Enter Subject Code of the Classroom which you want to delete :")

            if class_code in classes_created:

                print("You have permissions to Delete the classroom")

                code_query = {'class_code':class_code}
                code_required = list(classesDB.find(code_query))

                deleteclass=classes_created.index(class_code)
                del classes_created[deleteclass]
                newclasses = {"$set":{'classes':classes_created}}
                usersDB.update_one(id_query,newclasses)
                print("Current Profile Updated")
                profile(userName)

                studentslist = code_required[0]["studentsIDs"]
                #We need to delete this class code from all the students in studentslist

                for i in range(len(studentslist)):
                    current_student = studentslist[i]
                    student_query = {'_id':current_student}
                    update_student = list(usersDB.find(student_query))
                    curr_student_classes_joined=update_student[0]["classes"]
                    remove_class=0
                    for j in range(len(curr_student_classes_joined)):
                        if curr_student_classes_joined[j]==class_code:
                            remove_class=j
                            break
                    del curr_student_classes_joined[remove_class]

                    newclasses_joined_query = {"$set":{'classes':curr_student_classes_joined}}
                    usersDB.update_one(student_query,newclasses_joined_query)



                    print("Updated for Student")
                emptyStudents={"$set":{'studentsIDs':[]}}
                classDB.update_one(code_query,emptyStudents)
                print("All Students Profile is Updated")
                continue
            else:
                print("You haven't Created that Classroom to Delete")
                continue

            #####################################
            ######################################
        elif choice ==5:
            print("Logout")
            break
        else:
            print("Invalid Choice")
            print("TryAgain!!!1")
            continue









################################################################
#Working VERIFIED

def studentmenu(userName):

    while True:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("Menu")
        print("1) View Profile")
        print("2) Join a Class")
        print("3) View Joined Classes")
        print("4) Leave a Class")
        print("5) Logout")
        choice=int(input("Select your Choice :"))

        if choice == 1:
            #View Profile VERIFIED
            profile(userName)
            continue

        elif choice == 2:
            #Join a Class VERIFIED
            id_query = {'user_name':userName}
            required = list(usersDB.find(id_query))
            userID = required[0]['_id']
            classes_joined = required[0]['classes']

            class_code = input("Enter Code of the Classroom you want to join :")
            class_query = {'class_code':class_code}
            class_required=list(classesDB.find(class_query))

            if len(class_required)==0:
                print("Class Code Doesn't exist")
                continue
            elif len(class_required)==1:

                print("Classroom Found!!")

                studentslist = class_required[0]["studentsIDs"]
                studentslist.append(userID)
                new_student = {"$set":{'studentsIDs':studentslist}}
                classesDB.update_one(class_query,new_student)
                print("Updated Class Database")

                classes_joined.append(class_code)
                new_class = {"$set":{'classes':classes_joined}}
                usersDB.update_one(id_query,new_class)
                print("Updated User Profile")
                profile(userName)
                continue

            else:
                print("Multiple Classes With Same Class Code Error")
                continue

        elif choice == 3:
            #list of classes Joined VERIFIED
            id_query = {'user_name':userName}
            required = list(usersDB.find(id_query))
            classes_joined = required[0]['classes']

            print("List of Classes Joined")
            for i in classes_joined:
                print(i)
            continue

        elif choice == 4:
            #Leave a joined Class VERIFIED
            id_query = {'user_name':userName}
            required = list(usersDB.find(id_query))
            userID = required[0]['_id']
            classes_joined = required[0]['classes']

            class_code = input("Enter Code of the Classroom you want to leave :")
            if class_code in classes_joined:

                class_query = {'class_code':class_code}
                class_required=list(classesDB.find(class_query))

                studentslist = class_required[0]["studentsIDs"]
                removeid=0
                for i in range(len(studentslist)):
                    if userID == studentslist[i]:
                        removeid=i
                        break
                del studentslist[removeid]

                new_student = {"$set":{'studentsIDs':studentslist}}
                classesDB.update_one(class_query,new_student)
                print("Updated Class Database")

                removeclass=classes_joined.index(class_code)
                del classes_joined[removeclass]

                new_class = {"$set":{'classes':classes_joined}}
                usersDB.update_one(id_query,new_class)
                print("Updated User Profile")
                profile(userName)
                continue

            else:
                print("You haven't Joined that Classroom to leave")
                continue

        elif choice ==5:
            #Logging Out VERIFIED
            print("Logging Out")
            break
        else:
            #For invalid selected choices VERIFIED
            print("Invalid Choice")
            continue


################################################################
#Working VERIFIED
def menu():

    while True:
        print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("Menu")
        print("1) Login")
        print("2) Signup")
        print("3) Exit")
        choice=int(input("Select your Choice :"))
        if choice==1:
            #Login Module
            userName = input("Enter UserName :")
            password = input("Enter password :")
            auth = authuser(userName,password)
            if auth==True:
                #user loggedin
                print("Login Success!!!")
                role_query = { 'user_name' : userName}
                required = list(usersDB.find(role_query))
                print(required)
                userrole = required[0]['role']
                if userrole == 'student':
                    studentmenu(userName)
                else:
                    teachermenu(userName)
                continue

            else:
                #Login Failed
                print("TryAgain!!!!")
                continue


        elif choice==2:
            #Signup Module
            userName = input("Enter UserName :")
            password = input("Enter Password :")
            role = input("Enter your role student or teacher :")
            age = int(input("Enter Your Age :"))
            location = input("Enter your Location :")
            allusers = list(usersDB.find())
            match=False
            for i in range(len(allusers)):
                if userName == allusers[i]['user_name']:
                    match=True
                    break
            if match == True:
                print("UserName Already in Use")
                print("TryAgain!!!")
                continue
            else:
                curr_user_data={
                    'user_name':userName,
                    'password':password,
                    'age':age,
                    'role':role,
                    'classes':[],
                    'location': location
                }
                print("signing up......")
                usersDB.insert_one(curr_user_data)
                print("signup successful")
                print("Now Login With Your Credentials")
                continue

        elif choice==3:
            #Exit Module
            print("Exiting.....")
            break


        else:
            #For invalid selected choices
            print("Invalid Choice")
            continue

#####################################################################################

#Running The Application
menu()
