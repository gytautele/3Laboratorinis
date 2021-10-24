import tkinter
import time
import sqlite3
import random
import tempfile
import win32api
import win32print

f = ''
flag = ''
flags = ''
login = sqlite3.connect("admin.db")
l = login.cursor()
c = sqlite3.connect("medicine.db")
cur = c.cursor()
columns = ('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
menu1='Main menu'
mouse1='<MouseWheel>'
query2="select *from med"
listbox1='<<ListboxSelect>>'

def open_window():
    global apt, flag
    flag = 'apt'
    apt = Tk()
    apt.title("Interface")
    Label(apt, text="EVANZ MEDICAL STORE COMPANY").grid(row=0, column=0, columnspan=3)
    Label(apt, text='*' * 80).grid(row=1, column=0, columnspan=3)
    Label(apt, text='-' * 80).grid(row=3, column=0, columnspan=3)
    Label(apt, text="Stock Maintenance", bg='green', fg='white').grid(row=2, column=0)
    Button(apt, text='New V.C.', width=25, bg='green', fg='white', command=val_cus).grid(row=4, column=0)
    Button(apt, text='Add product to Stock', bg='green', fg='white', width=25, command=stock).grid(row=5, column=0)
    Button(apt, text='Delete product from Stock', bg='red', fg='white', width=25, command=delete_stock).grid(row=6, column=0)
    Label(apt, text="Access Database", bg='blue', fg='white').grid(row=2, column=1)
    Button(apt, text='Modify', width=15, bg='blue', fg='white', command=modify).grid(row=4, column=1)
    Button(apt, text='Search', width=15, bg='blue', fg='white', command=search).grid(row=5, column=1)
    Button(apt, text='Expiry Check', bg='red', fg='white', width=15, command=exp_date).grid(row=6, column=1)
    Label(apt, text="Handle Cash Flows", bg='skyblue', fg='black').grid(row=2, column=2)
    Button(apt, text="Check Today's Revenue", bg='skyblue', fg='black', width=20, command=show_rev).grid(row=5,                                                                                                    column=2)
    Button(apt, text='Billing', width=20, bg='skyblue', fg='black', command=billing).grid(row=4, column=2)
    Button(apt, text='Logout', bg='red', fg='white', width=20, command=again).grid(row=6, column=2)
    apt.mainloop()

def delete_stock():
    global cur, c, flag, lb1, d
    apt.destroy()
    flag = 'd'
    d = Tk()
    d.title("Delete a product from Stock")
    Label(d, text='Enter Product to delete:').grid(row=0, column=0)
    Label(d, text='', width=30, bg='white').grid(row=0, column=1)
    Label(d, text='Product').grid(row=2, column=0)
    Label(d, text='Qty.  Exp.dt.     Cost                           ').grid(row=2, column=1)
    regenerate_list()
    b = Button(d, width=20, text=menu1, bg='green', fg='white', command=main_menu).grid(row=5, column=3)
    d.mainloop()

def regenerate_list():
    global lb1, d, cur, c

    def onvsb(*args):
        lb1.yview(*args)
        lb2.yview(*args)

    def onmousewheel():
        lb1.ywiew = ('scroll', event.delta, 'units')
        lb2.ywiew = ('scroll', event.delta, 'units')
        return 'break'

    cx = 0
    vsb = Scrollbar(orient='vertical', command=onvsb)
    lb1 = Listbox(d, width=25, yscrollcommand=vsb.set)
    lb2 = Listbox(d, width=30, yscrollcommand=vsb.set)
    vsb.grid(row=3, column=2, sticky=N + S)
    lb1.grid(row=3, column=0)
    lb2.grid(row=3, column=1)
    lb1.bind(mouse1, onmousewheel)
    lb2.bind(mouse1, onmousewheel)
    cur.execute(query2)
    for i in cur:
        cx += 1
        s1 = [str(i[0]), str(i[1])]
        s2 = [str(i[3]), str(i[6]), str(i[4])]
        lb1.insert(cx, '. '.join(s1))
        lb2.insert(cx, '   '.join(s2))
    c.commit()
    lb1.bind(listbox1, medicaments_delete)

def medicaments_delete(e):
    global lb1, d, cur, c, p, sl2
    p = lb1.curselection()
    print(p)
    x = 0
    sl2 = ''
    cur.execute(query2)
    for i in cur:
        print(x, p[0])
        if x == int(p[0]):
            sl2 = i[0]
            break
        x += 1
    c.commit()
    print(sl2)
    Label(d, text=' ', bg='white', width=20).grid(row=0, column=1)
    cur.execute(query2)
    for i in cur:
        if i[0] == sl2:
            Label(d, text=i[0] + '. ' + i[1], bg='white').grid(row=0, column=1)
    c.commit()
