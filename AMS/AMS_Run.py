import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

#####Window is our Main frame of system
window = tk.Tk()
window.title("FRBAMS-Facial Recognition Based Attendance Management System")

window.geometry('1280x720')
window.configure(background='gainsboro')


####GUI for manually fill attendance

def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap('AMS.ico')
    sb.title("Enter Enrollment...")
    sb.geometry('580x320')
    sb.configure(background='gainsboro')

    def err_screen_for_subject():

        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry('300x100')
        ec.iconbitmap('AMS.ico')
        ec.title('Warning!!')
        ec.configure(background='gainsboro')
        Label(ec, text='Please enter your p_no!!!', fg='red', bg='dim gray', font=('times', 16, ' italic bold ')).pack()
        Button(ec, text='OK', command=ec_delete, fg="red", bg="dim gray", width=9, height=1, activebackground="Red",
               font=('times', 15, ' bold ')).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        ####Creatting csv of attendance

        ##Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
        # global subb
        # subb =SUB_ENTRY.get()
        # DB_table_name = str(subb + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second)
        # ???????
        global subject
        subject = SUB_ENTRY.get()
        DB_table_name = str(subject + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second)

        import pymysql.connections

        ###Connect to the database
        try:
            global cursor
            connection = pymysql.connect(host='localhost', user='root', password='', db='manually_fill_attendance')
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = "CREATE TABLE " + DB_table_name + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                         ENROLLMENT varchar(100) NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         DATE VARCHAR(20) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                             PRIMARY KEY (ID)
                             );
                        """

        try:
            cursor.execute(sql)  ##for create a table
        except Exception as ex:
            print(ex)  #

        # if subb=='':
        # ???????
        if subject == '':
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap('AMS.ico')
            MFW.title("Manually attendance of " + str(subject))
            MFW.geometry('880x470')
            MFW.configure(background='gainsboro')

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry('330x100')
                errsc2.iconbitmap('AMS.ico')
                errsc2.title('Warning!!')
                errsc2.configure(background='gainsboro')
                Label(errsc2, text='Please enter Name & Enrollment!!!', fg='red', bg='dim gray',
                      font=('times', 16, ' italic bold ')).pack()
                Button(errsc2, text='OK', command=del_errsc2, fg="red", bg="dim gray", width=9, height=1,
                       activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == '1':  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(MFW, text="Enter Enrollment", width=15, height=2, fg="black", bg="gainsboro",
                           font=('times', 15, ' italic bold '))
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(MFW, text="Enter Name", width=15, height=2, fg="black", bg="gainsboro",
                                font=('times', 15, ' italic bold '))
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(MFW, width=20, validate='key', bg="white", fg="red", font=('times', 23, ' bold '))
            ENR_ENTRY['validatecommand'] = (ENR_ENTRY.register(testVal), '%P', '%d')
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="white", fg="red", font=('times', 23, ' bold '))
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            ####get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == '':
                    err_screen1()
                elif STUDENT == '':
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    Hour, Minute, Second = time.split(":")
                    Insert_data = "INSERT INTO " + DB_table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    VALUES = (str(ENROLLMENT), str(STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv
                cursor.execute("select * from " + DB_table_name + ";")
                # ???????????
                # csv_name='C:/Users/kusha/PycharmProjects/Attendace managemnt system/Attendance/Manually Attendance/'+DB_table_name+'.csv'
                csv_name = 'D:\Attendace_management_system-master\Attendance\Manually Attendance/' + DB_table_name + '.csv'
                with open(csv_name, "w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([i[0] for i in cursor.description])  # write headers
                    csv_writer.writerows(cursor)
                    O = "CSV created Successfully"
                    Notifi.configure(text=O, bg="gainsboro", fg="white", width=33, font=('times', 19, 'bold'))
                    Notifi.place(x=180, y=380)
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + subject)
                root.configure(background='gainsboro')
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=13, height=1, fg="black", font=('times', 13, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(MFW, text="CSV created Successfully", bg="dim gray", fg="black", width=33,
                              height=2, font=('times', 19, 'bold'))

            # c1ear_enroll = tk.Button(MFW, text="Clear", command=remove_enr, fg="black", bg="deep pink", width=10,
            #                          height=1,
            #                          activebackground="Red", font=('times', 15, ' bold '))
            # c1ear_enroll.place(x=690, y=100)
            #
            # c1ear_student = tk.Button(MFW, text="Clear", command=remove_student, fg="black", bg="deep pink", width=10,
            #                           height=1,
            #                           activebackground="Red", font=('times', 15, ' bold '))
            # c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(MFW, text="Enter Data", command=enter_data_DB, fg="white", bg="dim gray", width=14,
                                 height=2,
                                 activebackground="Red", font=('times', 15, ' italic bold '))
            DATA_SUB.place(x=290, y=300)

            MAKE_CSV = tk.Button(MFW, text="Convert to CSV", command=create_csv, fg="white", bg="dim gray", width=14,
                                 height=2,
                                 activebackground="Red", font=('times', 15, 'italic bold '))
            MAKE_CSV.place(x=460, y=300)

            def attf():
                import subprocess
                # subprocess.Popen(r'explorer /select,"C:\Users\kusha\PycharmProjects\Attendace managemnt system\
                # Attendance\Manually Attendance\-------Check atttendance-------"')
                #     ????????
                subprocess.Popen(
                    r'explorer /select,"D:\Attendace_management_system-master\Attendance\TrainingImage\-------Check atttendance-------"')

            attf = tk.Button(MFW, text="Check Sheets", command=attf, fg="white", bg="dim gray", width=12, height=1,
                             activebackground="Red", font=('times', 14, 'italic bold '))
            attf.place(x=730, y=410)

            MFW.mainloop()
    SUB = tk.Label(sb, text="Enter Enrollment", width=15, height=2, fg="black", bg="gainsboro",
                   font=('times', 15, 'italic bold '))
    SUB.place(x=30, y=100)

    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(sb, width=20, validate='key', bg="white", fg="red", font=('times', 23, ' bold '))
    SUB_ENTRY['validatecommand'] = (SUB_ENTRY.register(testVal), '%P', '%d')
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(sb, text="Fill Attendance", command=fill_attendance, fg="white", bg="dim gray",
                                       width=20, height=2,
                                       activebackground="Red", font=('times', 15, ' italic bold '))
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()


##For clear textbox
def clear():
    txt.delete(first=0, last=22)


def clear1():
    txt2.delete(first=0, last=22)


def del_sc1():
    sc1.destroy()


def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='gainsboro')
    Label(sc1, text='Enrollment & Name required!!!', fg='red', bg='dim gray', font=('times', 16, ' bold ')).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="dim gray", width=9, height=1, activebackground="Red",
           font=('times', 15, ' bold ')).place(x=90, y=50)


##Error screen2
def del_sc2():
    sc2.destroy()


def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='gainsboro')
    Label(sc2, text='Please enter Enrollment!!!', fg='red', bg='dim gray', font=('times', 16, ' bold ')).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="dim gray", width=9, height=1, activebackground="Red",
           font=('times', 15, ' bold ')).place(x=90, y=50)


###For take images for datasets
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="dim gray", width=50, font=('times', 18, 'italic bold'))
            Notification.place(x=250, y=400)
        except FileExistsError as f:
            f = "Data already exists!"
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)


###for choose sub and fill attendance
def subjectchoose():
    def Fillattendances():
        # sub=tx.get()
        # ??????
        subject = tx.get()
        now = time.time()  ###For calculate seconds of video
        future = now + 20
        if time.time() < future:
            # if sub == '':
            # ????????
            if subject == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("TrainingImageLabel\Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="gainsboro", fg="black", width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=20, y=250)

                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                # ???????
                df = pd.read_csv("StudentDetails\StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name', 'Date', 'Time']
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id
                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf < 70):
                            print(conf)
                            global Subject
                            # global aa
                            # ??????????
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            # aa = df.loc[df['Enrollment'] == Id]['Name'].values
                            # ?????????
                            Subject = df.loc[df['Enrollment'] == Id]['Name'].values
                            global tt
                            # tt = str(Id) + "-" + aa
                            # ????????
                            tt = str(Id) + "-" + subject
                            En = '15624031' + str(Id)
                            # attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                            # ???????????
                            attendance.loc[len(attendance)] = [Id, subject, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                        else:
                            # Id = 'Unknown'
                            # ???????????
                            Id = subject;
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                ##Create table for Attendance
                date_for_DB = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d')
                DB_Table_name = str(subject + "_" + date_for_DB + "_Time_" + Hour + "_" + Minute + "_" + Second)
                import pymysql.connections

                ###Connect to the database
                try:
                    global cursor
                    # connection = pymysql.connect(host='localhost', user='root', password='', db='Face_reco_fill')
                    connection = pymysql.connect(host='localhost', user='root', password='', db='manually_fill_attendance')
                    cursor = connection.cursor()
                except Exception as e:
                    print(e)

                sql = "CREATE TABLE " + DB_Table_name + """
                (ID INT NOT NULL AUTO_INCREMENT,
                 ENROLLMENT varchar(100) NOT NULL,
                 NAME VARCHAR(50) NOT NULL,
                 DATE VARCHAR(20) NOT NULL,
                 TIME VARCHAR(20) NOT NULL,
                     PRIMARY KEY (ID)
                     );
                """
                ####Now enter attendance in Database
                # insert_data =  "INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES ()";
                insert_data = "INSERT INTO " + DB_Table_name + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                VALUES = (str(Id), str(subject), str(date), str(timeStamp))
                # VALUES = (str(Id), str(aa), str(date), str(timeStamp))
                # ??????????
                # VALUES = (str(id), str(subject), str(date), str(timeStamp))
                try:
                    cursor.execute(sql)  ##for create a table
                    cursor.execute(insert_data, VALUES)  ##For insert data into table
                except Exception as ex:
                    print(ex)  #

                M = 'Attendance filled Successfully'
                Notifica.configure(text=M, bg="Green", fg="white", width=33, font=('times', 15, 'bold'))
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + subject)
                root.configure(background='gainsboro')
                # cs = 'C:/Users/PycharmProjects/Attendace managemnt system/' + fileName
                # with open(cs, newline="") as file:
                #     reader = csv.reader(file)
                # ????????
                cs = 'D:\Attendace_management_system-master' + fileName
                with open(fileName) as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)

    ###windo is frame for sub chooser
    windo = tk.Tk()
    windo.iconbitmap('AMS.ico')
    windo.title("Enter Enrollment...")
    windo.geometry('580x320')
    windo.configure(background='gainsboro')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="dim gray", fg="white", width=33,
                        height=2, font=('times', 15, 'italic bold'))

    def Attf():
        import subprocess
        # subprocess.Popen(r'explorer /select,"C:\Users\PycharmProjects\Attendace managemnt system\Attendance\-------Check atttendance-------"')
        #     ????????
        subprocess.Popen(
            r'explorer /select,"D:\Attendace_management_system-master\Attendance\TrainingImage\-------Check atttendance-------"')

    attf = tk.Button(windo, text="Check Sheets", command=Attf, fg="white", bg="dim gray", width=12, height=1,
                     activebackground="Red", font=('times', 14, ' italic bold '))
    attf.place(x=430, y=255)

    sub = tk.Label(windo, text="Enter Enrollment", width=15, height=2, fg="black", bg="gainsboro",
                   font=('times', 15, ' italic bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, validate="key", bg="white", fg="red", font=('times', 23, ' bold '))
    tx['validatecommand'] = (tx.register(testVal), '%P', '%d')
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white", command=Fillattendances, bg="dim gray", width=20,
                       height=2,
                       activebackground="Red", font=('times', 15, ' italic bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()


def admin_panel():
    win = tk.Tk()
    win.iconbitmap('AMS.ico')
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='gainsboro')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'mohsin':
            if password == 'mohsin1650':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Data Details")
                root.configure(background='gainsboro')

                csv = 'D:\Attendace_management_system-master\StudentDetails\StudentDetails.csv'
                with open(csv, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="dim gray", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)

    Nt = tk.Label(win, text="Attendance filled Successfully", bg="dim gray", fg="white", width=40,
                  height=2, font=('times', 19, ' italic bold'))
    # Nt.place(x=120, y=350)

    un = tk.Label(win, text="Enter username", width=15, height=2, fg="black", bg="gainsboro",
                  font=('times', 15, ' italic bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password", width=15, height=2, fg="black", bg="gainsboro",
                  font=('times', 15, ' italic bold '))
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=20, bg="white", fg="red", font=('times', 23, ' bold '))
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white", fg="red", font=('times', 23, ' bold '))
    pw_entr.place(x=290, y=155)

    # c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="deep pink", width=10, height=1,
    #                activebackground="Red", font=('times', 15, ' bold '))
    # c0.place(x=690, y=55)


    Login = tk.Button(win, text="LogIn", fg="white", bg="dim gray", width=13,
                      height=1,
                      activebackground="Red", command=log_in, font=('times', 15, ' italic bold '))
    Login.place(x=290, y=250)
    c1 = tk.Button(win, text="LogOut", command=c11, fg="white", bg="dim gray", width=13, height=1,
                   activebackground="Red", font=('times', 15, ' italic bold '))
    c1.place(x=460, y=250)

    win.mainloop()


###For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces, Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l = 'please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="dim gray", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)
        recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q = 'Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="dim gray", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)

    # res = "Model Trained"  # +",".join(str(f) for f in Id)
    res = "Model Trained" + ",".join(str(f) for f in Id)
    Notification.configure(text=res, bg="dim gray", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faceSamples = ["TrainingImage"]
    # create empty ID list
    # Ids = ["Pno"]
    Ids = ["subject"]

    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids


window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.iconbitmap('AMS.ico')


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="Facial-Recognition-Based-Attendance-Management-System", bg="black", fg="white", width=50,
                   height=3, font=('times', 30, 'italic bold '))

message.place(x=80, y=20)

Notification = tk.Label(window, text="All things good", bg="dim gray", fg="white", width=15,
                        height=3, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enter Enrollment", width=20, height=2, fg="black", bg="gainsboro",
               font=('times', 15, ' italic bold '))
lbl.place(x=200, y=200)


def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


txt = tk.Entry(window, validate="key", width=20, fg="red", font=('times', 25, ' bold '))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name", width=20, fg="black", bg="gainsboro", height=2, font=('times', 15, ' italic bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20,  fg="red", font=('times', 25, ' bold '))
txt2.place(x=550, y=310)
#
# clearButton = tk.Button(window, text="Clear", command=clear, fg="black", bg="deep pink", width=10, height=1,
#                         activebackground="Red", font=('times', 15, ' bold '))
# clearButton.place(x=950, y=210)
#
# clearButton1 = tk.Button(window, text="Clear", command=clear1, fg="black", bg="deep pink", width=10, height=1,
#                          activebackground="Red", font=('times', 15, ' bold '))
# clearButton1.place(x=950, y=310)

AP = tk.Button(window, text="Check Registerations", command=admin_panel, fg="white", bg="dim gray", width=19, height=1,
               activebackground="Red", font=('times', 15, ' italic bold '))
AP.place(x=530, y=600)

takeImg = tk.Button(window, text="Take Images", command=take_img, fg="white", bg="dim gray", width=20, height=3,
                    activebackground="Red", font=('times', 15, ' italic bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Model", fg="white", command=trainimg, bg="dim gray", width=20, height=3,
                     activebackground="Red", font=('times', 15, 'italic  bold '))
trainImg.place(x=390, y=500)

FA = tk.Button(window, text="AutomaticAttendace", fg="white", command=subjectchoose, bg="dim gray", width=20, height=3,
               activebackground="Red", font=('times', 15, ' italic bold '))
FA.place(x=690, y=500)

quitWindow = tk.Button(window, text="Manually Fill Attendance", command=manually_fill, fg="white", bg="dim gray",
                       width=20, height=3, activebackground="Red", font=('times', 15, 'italic  bold '))
quitWindow.place(x=990, y=500)

window.mainloop()
