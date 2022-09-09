import re
import time, datetime
from prettytable import PrettyTable

mailregex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
phoneregex = re.compile(r'^(?:\+?01)?[09]\d{10,10}$') # best regex for egytian phone numbers


#-------------------------------(edit a Project)-------------------------------#
def editProject(usr_id):
    id = input("Enter id of the project you want to edit: ")
    flag = False
    file = open("files/projects.txt", 'r')
    data = file.readlines()
    file.close()
    for line in data:
        if line.split(":")[0] == id:
            if line.split(":")[6] == usr_id:
                print(line)
                del data[data.index(line)] # delete the line and take it with new modification
                # enter here the editing method ! select a field you want to edit then enter your modification
                title = input("Enter Project title: ")
                details = input("Enter Project details: ")
                taregt  = input("Enter Project total taregt: ")
                start_date = isValidDate("Enter Project start date (date format DD-MM-YYYY like): ")
                end_date   = isValidDate("Enter Project end date (date format like DD-MM-YYYY): ")
                
                data.append(str(id)+":"+title+":"+details+":"+taregt+":"+str(start_date)+":"+str(end_date)+":"+str(usr_id))
                
                file=open("files/projects.txt", "a")
                file.writelines(data)
                file.close()

                print("Project Edited !")
                flag = True
            else:
                print("Sorry You can only edit Your own projects !")
                loginMenu(usr_id)
    file = open("files/projects.txt", 'w')
    file.writelines(data)
    file.close()
    if flag == False:
        print("Not Found !")

#-------------------------------(Search for a Project)------------------------------------------#
def SearchProject():
    # need fixing !!!
    # take care if the user entered a wrong date format then enter an appropriate one the next line will raise an error !
    # because the function isValid did not return the date if it is would not right format fromt the first time.
    date = datetime.datetime.strptime(isValidDate("Enter the date you want to see available projects within: "), '%d-%m-%Y')       
    file = open("files/projects.txt", 'r')
    data = file.readlines()
    file.close()
    flag = False
    t = PrettyTable(['ID','Title','Description','Total Taregt','Start','End','Owner ID'])
    for line in data:
        start = datetime.datetime.strptime(line.split(":")[4], '%d-%m-%Y')       
        end = datetime.datetime.strptime(line.split(":")[5], '%d-%m-%Y')       
        if start <= date <= end:
        # date in between
            lst = line.split(":")
            t.add_row(lst)
            flag = True
    if flag == False:
        print("There are no Projects available in this date !")
    else:
        print(t)

#-------------------------------(delete a project)------------------------------------------------#
def delProject(usr_id):
    id = input("Enter id of the project you want to delete: ")
    flag = False
    file = open("files/projects.txt", 'r')
    data = file.readlines()
    file.close()
    for line in data:
        if line.split(":")[0] == id:
            if line.split(":")[6] == usr_id:
                print(line)
                del data[data.index(line)] 
                print("Project Deleted !")
                flag = True
            else:
                print("Sorry You can only delete Your own projects !")
                delProject(usr_id)
    file = open("files/projects.txt", 'w')
    file.writelines(data)
    file.close()
    if flag == False:
        print("Not Found !")

#-------------------------------(View all projects)------------------------------------------------#
def getProjects():
    file = open("files/projects.txt", 'r')
    data = file.readlines()
    file.close()
    t = PrettyTable(['ID','Title','Description','Total Taregt','Start','End','Owner ID'])
    for line in data:
        lst = line.split(":")
        t.add_row(lst)
    print(t)

#-------------------------------(Create Project)---------------------------------------------------#
#---(validation function)----------------------------
def isValidDate(msg):
    date = input(msg)
    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
        return date
    except ValueError:
        #raise ValueError()
        isValidDate("Incorrect data format, should be DD-MM-YYYY: ")

## canceled function
def isValidDate2(msg):
    date = input(msg)
    if re.fullmatch(dateregex, date):
        return date
    else: isValidDate2("Enter a Valid Date: ")
#---(CreateProject)----------------------------------
def CreateProject(usr_id):
    ts = time.time()
    p_id = int(ts)
    title = input("Enter Project title: ")
    details = input("Enter Project details: ")
    taregt  = input("Enter Project total taregt: ")
    start_date = isValidDate("Enter Project start date (date format DD-MM-YYYY like): ")
    end_date   = isValidDate("Enter Project end date (date format like DD-MM-YYYY): ")
    
    print("You Have Created a Project Successfully!")
    print(f"Your data (id:{p_id} title {title} details:{details} taregt:{taregt} start date:{start_date} end date:{end_date} usr_id: {usr_id})")

    fileobject=open("files/projects.txt", "a")
    fileobject.writelines(str(p_id)+":"+title+":"+details+":"+taregt+":"+str(start_date)+":"+str(end_date)+":"+str(usr_id))
    fileobject.close()
#---------------------------(Login Menu)-----------------------------------------------------------#
def loginMenu(usr_id):
    print ('----------------------------------------')
    print (f'Welcome {mail} , You are now logged in !')
    print ('----------------------------------------')
    print ('Press 1 to View All projects')   # done
    print ('Press 2 to Create New Project')  # done
    print ('Press 3 to Delete a Project')    # done
    print ('Press 4 to Search for a Project by date') # done
    print ('Press 5 to Edit a Project')      # done but not in best way !
    print ('Press 6 to go to the Main Menu') # done
    print ('Press 0 to Exit') # done
    print ('----------------------------------------')
    while True:
        user_input = input('Enter Your selection: ')
        try:
            user_input = int(user_input)
            if user_input   == 1:
                getProjects()
                loginMenu(usr_id)
            elif user_input == 2:
                CreateProject(usr_id)
                loginMenu(usr_id)
            elif user_input == 3:
                delProject(usr_id)
                loginMenu(usr_id)
            elif user_input == 4:
                SearchProject()
                loginMenu(usr_id)
            elif user_input == 5:
                editProject(usr_id)
                loginMenu(usr_id)
            elif user_input == 6:
                MainMenu()
            elif user_input == 0:
                print("Exit Now ........ !")
                exit()
            else:
                print("Please Choose from the Menue !")
        except ValueError:
                print("Pleaes Enter a vaild Number !")

#---------------------------(Login Auth)--------------------------------------------------------------#
def isUser():
    global mail # we make it global to use it in the login menu every time
    mail = input("Enter Your Email: ")
    passwd = input("Enter Your Password: ")
    fileobject=open("files/users.txt", "r")
    data = fileobject.readlines()  # get all lines from the users file
    for line in data:        
        # extract the mail and passwd fields
        if mail == line.split(":")[2] and passwd == line.split(":")[3]: # 2.mail field # 3.passwd field
            usr_id = line.split(":")[5]
            fileobject.close()
            # here we have to pass his id to the next stage to be able to add it to the project while creating it
            loginMenu(usr_id)
    print("Wrong Email or Password !")
    isUser()

#-----------------------------------(Registeration)----------------------------------------------------#
#---(validation functions)----------------------------
def isValidEmail(msg):
    email = input(msg)
    if re.fullmatch(mailregex, email):
        return email
    else: isValidEmail("Enter a Valid email: ")
    return email
def isValidPhone(msg):
    phone = input(msg)
    if re.fullmatch(phoneregex, phone):
        return phone
    else: return isValidPhone("Enter a Valid phone number: ")

def isValidName(msg):
    name = input(msg)
    if not any(char.isdigit() for char in name):
        return name
    else:
        isValidName("Enter a Valid Name: ")
    return name 

#---(Registration functions)----------------------------
def Rgstr():
    ts = time.time()
    usr_id = int(ts)
    f_name = isValidName("Enter Your First Name: ")
    l_name = isValidName("Enter Your Last Name: ")
    email = isValidEmail("Enter Your email: ")
    passwd = input("Enter Your Password: ")
    confirmpswd = input("Enter Your Password Again: ")
    while confirmpswd != passwd:
        print("Password doesnot match !")
        passwd = input("Enter Your Password: ")
        confirmpswd = input("Please Confirm Your Password: ")

    phone = isValidPhone("Enter Your phone number: ")
    
    print("You Have Registered Successfully!")
    print(f"Your data (Name:{f_name} {l_name} Mail:{email} Password:{passwd} Phone Number:{phone} id:{usr_id}")

    fileobject=open("files/users.txt", "a")
    fileobject.writelines(f_name+":"+l_name+":"+email+":"+passwd+":"+phone+":"+str(usr_id))
    fileobject.close()

#-------------------------------(Main Menu)--------------------------------------------------------------#
def MainMenu():
    print ('----------------------------------------')
    print ('welcome to the Crowd Funding Program')
    print ('----------------------------------------')
    print ('Press 1 to Registeration')
    print ('Press 2 to Login !')
    print ('Press 0 to Exit')
    print ('----------------------------------------')
    while True:
        user_input = input('Enter Your selection: ')
        try:
            user_input = int(user_input)
            if user_input == 1:
                Rgstr()
                MainMenu()
            elif user_input == 2:
                isUser()
                MainMenu()
            elif user_input == 0:
                print("Exit Now ........ !")
                exit()
            else:
                print("Please Choose from the Menue !")
        except ValueError:
                print("Pleaes Enter a vaild Number !")

MainMenu()


######## testing area #########

#getProjects()

#delProject()

#isUser()

#CreateProject(1662135274)

