import re
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
import sqlite3
from datetime import *
import speech_recognition as sr
import os
import pandas as pd
os.chdir(os.path.dirname(sys.argv[0]))
db_path="loweshackathonfinaldb.db"
def getData():
    try:
        conn = sqlite3.connect(db_path)
        f = open("demo.csv", "w")
        dic = {}
        t = conn.cursor()
        conn.row_factory = lambda cursor, row: row[0]
        c = conn.cursor()
        f = conn.cursor()
        m = c.execute("""select User_ID from USER""").fetchall()
        for i in m:
            dic[int(i)] = {}
        n = f.execute("""select P_id from PRODUCT""").fetchall()
        for i in m:
            for j in n:
                dic[int(i)][int(j)] = 0

        l = t.execute("""select U_ID,P_id1 from ORDER1""").fetchall()
        for i, j in l:
            dic[i][j] = 1
        df = pd.DataFrame(data=dic).T
        df.to_csv("demo.csv")
    except e:
        tkinter.messagebox.showinfo("Exception",e)
    finally:
        conn.close()

mydb = sqlite3.connect(db_path)
c = mydb.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS akshay(productname varchar(20),price int,rating int)''')

mydb.commit()
def main():
    getData()
    root = Tk()
    root.title("welcome to shop")


    def register():
        r1 = Toplevel(bg='black')
        mydb.commit()

        fname = StringVar()
        lname = StringVar()
        dob = StringVar()
        gender = StringVar()
        add = StringVar()
        email = StringVar()
        passwd = StringVar()
        pno = IntVar()
        college = StringVar()

        l3 = Label(r1, text="USERNAME :", bg='red', width=15)
        l3.grid(column=0, row=0, pady=3)
        t3 = Entry(r1, textvariable=fname)
        t3.grid(column=3, row=0, pady=3)

        l5 = Label(r1, text="DATE OF BIRTH :", bg='red', width=15)
        l5.grid(column=0, row=4, pady=3)
        t5 = Entry(r1, textvariable=dob)
        t5.grid(column=3, row=4, pady=3)

        l6 = Label(r1, text="GENDER :", bg='red', width=15)
        l6.grid(column=0, row=6, pady=3)
        t6 = Entry(r1, textvariable=gender).grid(column=3, row=6, pady=3)

        l7 = Label(r1, text="ADDRESS :", bg='red', width=15).grid(column=0, row=8, pady=3)
        t7 = Entry(r1, textvariable=add).grid(column=3, row=8, pady=3)

        l8 = Label(r1, text="EMAIL :", bg='red', width=15).grid(column=0, row=10, pady=3)
        t8 = Entry(r1, textvariable=email).grid(column=3, row=10, pady=3)

        l9 = Label(r1, text="PASSWORD :", bg='red', width=15).grid(column=0, row=12, pady=3)
        t9 = Entry(r1, show='\u25CF', textvariable=passwd).grid(column=3, row=12, pady=3)

        l10 = Label(r1, text="PHONE NO. :", bg='red', width=15).grid(column=0, row=14, pady=3)
        t10 = Entry(r1, textvariable=pno).grid(column=3, row=14, pady=3)

        def insert():
            a = fname.get()
            c = dob.get()
            d = gender.get()
            e = add.get()
            f = email.get()
            g = passwd.get()
            h = pno.get()
            mydb = sqlite3.connect(db_path)
            c = mydb.cursor()
            c.execute(
                '''INSERT INTO USER(NAME,DOB,GENDER,ADDRESS,email_id,PASSWORD,PHONE_NO) VALUES('%s','%s','%s','%s','%s','%s','%d')''' % (
                a, c, d, e, f, g, h))
            c.close()
            mydb.commit()
            c.close()
            login1()
        def login2():
            r1.destroy()
            login1()
        b3 = Button(r1, text="REGISTER", command=insert, bg='red').grid(row=20, column=2, pady=3)
        b5 = Button(r1, text="LOGIN", command=login2, bg='red').grid(row=21, column=2, padx=10, pady=10)

    def login1():
        mydb = sqlite3.connect(db_path)
        c = mydb.cursor()
        top = Toplevel(bg='black')
        user = StringVar()
        pwd = StringVar()
        username = Label(top, text="USERNAME:", bd=1, relief="solid", font="arial 20", bg='red').grid(row=1, column=1,
                                                                                                      padx=10, pady=10)
        userentry = Entry(top, textvariable=user, width=25, relief="solid", font="arial 20").grid(row=1, column=2)
        password = Label(top, text="PASSWORD:", bd=1, relief="solid", font="arial 20", bg='red').grid(row=2, column=1,
                                                                                                      padx=10, pady=10)
        pwdentry = Entry(top,show='\u25CF', textvariable=pwd, width=25, relief="solid", font="arial 20").grid(row=2, column=2)

        def login():

            mydb = sqlite3.connect(db_path)
            c = mydb.cursor()
            c.execute("SELECT * FROM USER")
            e = c.fetchall()
            a = user.get()
            b = pwd.get()
            flag = True
            for i in range(0, len(e)):
                if a == e[i][2] and b == e[i][3]:
                    top.destroy()
                    root.withdraw()
                    flag = False
                    firstgui(e[i][0])
            if flag == True:
                tkinter.messagebox.showinfo("Invalid Credentials","User or Password is incorrect. Use register button if you have not registered")
            c.close()

        b1 = Button(top, text="SUBMIT", command=login, bd=8, width=20, pady=5, padx=10).grid(row=3, column=2, pady=10)


    reg = Button(root, text="REGISTER", command=register, bd=8, width=20, pady=5, padx=10).grid(row=1, column=1, pady=10)
    log = Button(root, text="LOGIN", command=login1, bd=8, width=20, pady=5, padx=10).grid(row=2, column=1, pady=10)
    exit = Button(root, text="EXIT", command=root.destroy, bd=8, width=20, pady=5, padx=10).grid(row=3, column=1, padx=10,pady=10)
    root.mainloop()
def mlmod(prodid):
    ratings=pd.read_csv("demo.csv",index_col=0)
    ratings.fillna(0, inplace=True)

    corrMatrix = ratings.corr(method='pearson').fillna(0)


    def get_similar(prodid_name):
        similar_score = corrMatrix[str(prodid_name)]
        similar_score = similar_score.sort_values(ascending=False)
        return similar_score

    similar_scores = pd.DataFrame()
    similar_scores = similar_scores.append(get_similar(prodid),ignore_index = True)

    return dict(similar_scores.sum().sort_values(ascending=False).head(5).to_dict())

def firstgui(e):
    a = StringVar()
    def recommendationpage(pid):
        top5=Toplevel()
        mydb = sqlite3.connect(db_path)
        c = mydb.cursor()

        scrollbarx = Scrollbar(top5, orient=HORIZONTAL)
        scrollbary = Scrollbar(top5, orient=VERTICAL)
        tree = ttk.Treeview(top5, column=("column1", "column2", "column3","column4"), show='headings')
        scrollbary.config(command=tree.yview)

        scrollbarx.config(command=tree.xview)


        tree.heading("#1", text="PRODUCT ID", anchor=W)
        tree.heading("#2", text="PRODUCT NAME", anchor=W)
        tree.heading("#3", text="AMOUNT", anchor=W)
        tree.heading("#4", text="PRODUCT TYPE", anchor=W)
        tree.column('#1', stretch=YES, minwidth=0, width=100)
        tree.column('#2', stretch=YES, minwidth=0, width=100)
        tree.column('#3', stretch=YES, minwidth=0, width=80)
        tree.column('#4', stretch=YES, minwidth=0, width=100)
        tree.grid(row=0, column=1)
        ak = mlmod(int(pid))
        for i in ak.keys():
            c.execute("SELECT P_id,ProductName, Amount, ProductType FROM PRODUCT WHERE P_id ='%s'"%i)
            row=c.fetchall()
            for i in row:
                tree.insert("", tk.END, values=i)
        c.close()
        mydb.commit()
        def quant1():
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            quant(e,selecteditem)
        b15 = Button(top5, text="ORDER",command = quant1, bd=8, width=20, pady=5, padx=10).grid(row=3, column=1,padx=10,pady=10)

    def quant(e,p):
        t20=Toplevel()
        k=IntVar()
        l20 = Label(t20, text="ENTER QUANTITY", bd=1, relief="solid", font="arial 20", bg='red').grid(row=1,column=1)
        e20 = Entry(t20, textvariable=k, width=25, relief="solid", font="arial 20").grid(row=1, column=2)
        def calc1():
            price = p[2]
            qty = k.get()
            t = price * qty
            t20.destroy()
            confirmorderpage(p[1],p[2],qty,t,e,p[0])
        def speak2():
            a = speak()
            txt = a.lower()
            x = re.findall(r"(?<=quantity)\D*(\d+)",txt)
            if len(x) != 0:
                k.set(x[0])
                calc1()
        b20= Button(t20, text="ORDER",command= calc1,  bd=8, width=20, pady=5, padx=10).grid(row=2, column=3, padx=10, pady=10)
        b21= Button(t20, text="SPEAK",command= speak2,  bd=8, width=20, pady=5, padx=10).grid(row=2, column=2, padx=10, pady=10)



    def viewall():
        y = IntVar()

        def finalorder(e):
            xy = y.get()
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            p = selecteditem[0]
            mydb = sqlite3.connect(db_path)
            c = mydb.cursor()
            c.execute("SELECT AMOUNT,ProductName FROM PRODUCT WHERE P_ID='%d'" % p)
            amt2 = c.fetchone()


            amt = (xy) * (amt2[0])
            t2.destroy()
            confirmorderpage(amt2[1],amt2[0],xy,amt,e,p)
            mydb.commit()
            c.close()

        mydb = sqlite3.connect(db_path)
        c = mydb.cursor()
        c.execute('''SELECT * FROM PRODUCT ''')
        g = c.fetchall()
        t2 = Toplevel()
        scrollbarx = Scrollbar(t2, orient=HORIZONTAL)
        scrollbary = Scrollbar(t2, orient=VERTICAL)
        tree = ttk.Treeview(t2, column=("column1", "column2", "column3", "column4"), show='headings')
        scrollbary.config(command=tree.yview)

        scrollbarx.config(command=tree.xview)


        tree.heading("#1", text="PRODUCT ID", anchor=W)
        tree.heading("#2", text="PRODUCT NAME", anchor=W)
        tree.heading("#3", text="PTYPE", anchor=W)
        tree.heading("#4", text="AMOUNT", anchor=W)
        tree.column('#1', stretch=YES, minwidth=0, width=100)
        tree.column('#2', stretch=YES, minwidth=0, width=100)
        tree.column('#3', stretch=YES, minwidth=0, width=100)
        tree.column('#4', stretch=YES, minwidth=0, width=100)
        tree.grid(row=0, column=1,rowspan=3)
        for row in g:
            tree.insert("", tk.END, values=row)
        c.close()
        mydb.commit()
        c.close()

        l6 = Label(t2, text="ENTER QUANTITY", bd=1, relief="solid", font="arial 20", bg='red').grid(row=0, column=2, padx=10,
                                                                                              pady=10)
        e6 = Entry(t2, textvariable=y, width=25, relief="solid", font="arial 20").grid(row=1, column=2)
        b4 = Button(t2, text="ORDER", command=lambda: finalorder(e), bd=8, width=20, pady=5, padx=10).grid(row=2,
                                                                                                           column=2,
                                                                                                           pady=10)

    def speak():
        r = sr.Recognizer()
        a = str()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            a = r.recognize_google(audio)
            return a
        except Exception:
            tkinter.messagebox.showinfo("Speech Error","Speak Clearly")
    def recom1(a):
        try:
            l = a.split()
            oo = search1(l)
            if oo != -1:
                recommendationpage( oo)
            else:
                raise Exception("not found")
        except Exception as e:
            tkinter.messagebox.showinfo("Error",e)
        
    def search1(l):
        try:
            mydb = sqlite3.connect(db_path)
        except e:
            tkinter.messagebox.showinfo("DB error","DB error")
        mydb.row_factory = lambda cursor,row: (row[0],row[1])
        c = mydb.cursor()

        c.execute("select ProductName,P_id from PRODUCT")
        d = c.fetchall()
        for k in l:
            for i,j in d:
                if k.lower()==i.lower():
                    return j

        return -1

    def myorders(f):
        t4 = Toplevel(bg='black')
        mydb = sqlite3.connect(db_path)
        c = mydb.cursor()
        c.execute(
            "select O_ID,OrderDate,ORDER1.Quantity,ORDER1.Amount,ProductName from ORDER1,PRODUCT where U_ID='%d' and P_ID1=P_id" % f)
        d = c.fetchall()
        scrollbarx = Scrollbar(t4, orient=HORIZONTAL)
        scrollbary = Scrollbar(t4, orient=VERTICAL)
        tree = ttk.Treeview(t4, column=("column1", "column2", "column3", "column4", "column5"), show='headings')
        scrollbary.config(command=tree.yview)

        scrollbarx.config(command=tree.xview)


        tree.heading("#1", text="ORDER ID", anchor=W)
        tree.heading("#2", text="ORDER DATE", anchor=W)
        tree.heading("#3", text="QUANTITY", anchor=W)
        tree.heading("#4", text="AMOUNT", anchor=W)
        tree.heading("#5", text="PRODUCT NAME", anchor=W)
        tree.column('#1', stretch=YES, minwidth=0, width=100)
        tree.column('#2', stretch=YES, minwidth=0, width=80)
        tree.column('#3', stretch=YES, minwidth=0, width=100)
        tree.column('#4', stretch=YES, minwidth=0, width=80)
        tree.column('#5', stretch=YES, minwidth=0, width=80)
        tree.grid(row=0, column=1)
        for row in d:
            tree.insert("", tk.END, values=row)
        c.close()
        mydb.commit()
        c.close()
    def logout():
        t.withdraw()
        main()
    def confirmorderpage(x,y,z,t,e,p):
        r2=Toplevel()
        l7 = Label(r2, text="PRODUCT NAME", bd=1, relief="solid", font="arial 20", bg='red').grid(row=1, column=1, padx=10)
        l8= Label(r2, text=str(x), bd=1, relief="solid", font="arial 20", bg='red').grid(row=1, column=2, padx=10)
        l9 = Label(r2, text="PRICE", bd=1, relief="solid", font="arial 20", bg='red').grid(row=2, column=1, padx=10)
        l10 = Label(r2, text=str(y), bd=1, relief="solid", font="arial 20", bg='red').grid(row=2, column=2,padx=10)
        l11 = Label(r2, text="QUANTITY", bd=1, relief="solid", font="arial 20", bg='red').grid(row=3, column=1,padx=10)
        l12 = Label(r2, text=str(z), bd=1, relief="solid", font="arial 20", bg='red').grid(row=3, column=2, padx=10)
        l13 = Label(r2, text="TOTAL", bd=1, relief="solid", font="arial 20", bg='red').grid(row=4, column=1, padx=10)
        l14 = Label(r2, text=str(t), bd=1, relief="solid", font="arial 20", bg='red').grid(row=4, column=2, padx=10)
        def conf1():
            mydb = sqlite3.connect(db_path)
            c = mydb.cursor()
            d = datetime.now().strftime("%Y-%m-%d")
            c.execute("INSERT INTO ORDER1(ORDERDATE,QUANTITY,AMOUNT,U_ID,P_ID1) VALUES('%s','%d','%d','%d','%d')" % (d,z, t, e, p))

            mydb.commit()
            mydb.close()
            r2.destroy()
        b10 = Button(r2, text="CONFIRM", command = conf1,bd=8, width=20, pady=5, padx=10).grid(row=5, column=3, pady=10)

    t = Tk()
    j=StringVar()
    def search():
        xy = j.get()
        mydb=sqlite3.connect(db_path)
        c=mydb.cursor()
        c.execute('''INSERT INTO search(pname) VALUES('%s') '''%xy)
        mydb.commit()
        c.close()
    def speak1():
        a = speak()
        print(a)
        if a!=None:
            vw = re.search(r".*view all products.*",a.lower())
            mp = re.search(r".*view my order.*",a.lower())
            if vw:
                viewall()
            elif mp:
                myorders(e)
            else:
                recom1(a)

    b2 = Button(t, text="SPEAK", command=speak1, bd=8, width=10, pady=5, padx=10).grid(row=1, column=1, padx=10, pady=10)
    b3 = Button(t, text="MYORDERS", command=lambda: myorders(e), bd=8, width=20, pady=5, padx=10).grid(row=3, column=1,
                                                                                                       pady=10)
    b4 = Button(t, text="LOGOUT", command=logout, bd=8, width=20, pady=5, padx=10).grid(row=4, column=1, pady=10)
    b6 = Button(t, text="VIEW ALL", command=viewall, bd=8, width=20, pady=5, padx=10).grid(row=2, column=1, padx=10,pady=10)

    t.mainloop()
if __name__=='__main__':
    main()
