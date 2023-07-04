from hapi import *
import tkinter
import numpy as np
import matplotlib.pyplot as plt

#右クリックのメニュー
def make_menu(w):
    global the_menu
    the_menu = tkinter.Menu(w, tearoff=0)
    the_menu.add_command(label="cut")
    the_menu.add_command(label="copy")
    the_menu.add_command(label="paste")

def show_menu(e):
    w = e.widget
    the_menu.entryconfigure("cut", command=lambda: w.event_generate("<<Cut>>"))
    the_menu.entryconfigure("copy", command=lambda: w.event_generate("<<Copy>>"))
    the_menu.entryconfigure("paste", command=lambda: w.event_generate("<<Paste>>"))
    the_menu.tk.call("tk_popup", the_menu, e.x_root, e.y_root)
#右クリック

def ButtonEvent(event):
    # パラメータを指定
    # --- ここから ---

    # スペクトルの範囲
    #spectrum_begin = EditBox_begin.get()
    spectrum_begin = int(EditBox_begin.get())
    #spectrum_end = EditBox_end.get()
    spectrum_end = int(EditBox_end.get())

    # HITRAN のパラメータ
    name = EditBox_gasname.get()
    #moleculeID = EditBox_id.get()
    moleculeID = int(EditBox_id.get())#NO:8 NO2:10 N2O:4 NH3:11 H20:1 CO2:2
    #isotopologueID = EditBox_isotope.get()
    isotopologueID = int(EditBox_isotope.get())

    # --- ここまで ---

    db_begin('data')

    fetch(name, moleculeID, isotopologueID, spectrum_begin, spectrum_end)

    # 取得したテーブルから、必要な情報を取得
    nu, sw = getColumns(name, ['nu', 'sw']) # 波長, 線強度
    nu = np.array(nu)
    sw = np.array(sw)

    # 振動準位の上下を取得
    global_upper_quanta, global_lower_quanta = getColumns(name, ['global_upper_quanta','global_lower_quanta'])

    # 回転準位の上下を取得
    local_upper_quanta, local_lower_quanta = getColumns(name, ['local_upper_quanta','local_lower_quanta'])

    #以下、グラフ作成
    fig = plt.figure(figsize=(6, 4))
    ax1 = fig.add_subplot(1, 1, 1)
    #ax1.scatter(nu,sw, label="line strength)
    #ax1.plot(nu,sw, label="line strength")
    ax1.plot(nu,sw)
    ax1.set_xlabel("k 1/cm")
    ax1.set_ylabel("line strength")
    ax1.grid(which="both")
    plt.show()

root = tkinter.Tk()
root.title("Hitran")
root.geometry("400x200")

#右クリック
make_menu(root)
root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_menu)
#右クリック

Button = tkinter.Button(text='plot', width = 10)
Button.bind("<Button-1>",ButtonEvent)#左クリック（<Button-1>）されると，ButtonEvent関数を呼び出すようにバインド
Button.place(x=290, y=70)

Button2 = tkinter.Button(text='exit', command=root.quit, width = 10)
Button2.place(x=290, y=110)

# チェックボックスの各項目の初期値
Static_begin = tkinter.Label(text='spectrum begin (1/cm)')
Static_begin.pack()
Static_begin.place(x=20, y=70)

Static_begin_2 = tkinter.Label(text='molecule ID: NO: 8,  NO2: 10, N2O: 4, NH3:11, H20: 1, CO2: 2')
Static_begin_2.pack()
Static_begin_2.place(x=20, y=20)

Static_end = tkinter.Label(text='spectrum end (1/cm)')
Static_end.pack()
Static_end.place(x=20, y=90)

Static_gasname = tkinter.Label(text='gas name')
Static_gasname.pack()
Static_gasname.place(x=20, y=110)

Static_id = tkinter.Label(text='molecule ID')
Static_id.pack()
Static_id.place(x=20, y=130)

Static_isotope = tkinter.Label(text='isotopologue ID')
Static_isotope.pack()
Static_isotope.place(x=20, y=150)

EditBox_begin = tkinter.Entry(width=10)
EditBox_begin.insert(tkinter.END,"1600")
EditBox_begin.place(x=180, y=70)

EditBox_end = tkinter.Entry(width=10)
EditBox_end.insert(tkinter.END,"2000")
EditBox_end.place(x=180, y=90)

EditBox_gasname = tkinter.Entry(width=10)
EditBox_gasname.insert(tkinter.END,"N2O")
EditBox_gasname.place(x=180, y=110)

EditBox_id = tkinter.Entry(width=10)
EditBox_id.insert(tkinter.END,"4")
EditBox_id.place(x=180, y=130)

EditBox_isotope = tkinter.Entry(width=10)
EditBox_isotope.insert(tkinter.END,"1")
EditBox_isotope.place(x=180, y=150)

root.mainloop()
