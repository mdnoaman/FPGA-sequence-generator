from tkinter import *
from tkinter import ttk
import serial

master = Tk()
master.title("Sequencer")

frame1 = Frame(master)
frame1.grid(row = 0, column = 0)

frame2 = Frame(master)
frame2.grid(row = 0, column = 1)

frame3 = Frame(master)
frame3.grid(row = 1, column = 0)

frame4 = Frame(master)
frame4.grid(row = 1, column = 1)

frame5 = Frame(master)
frame5.grid(row = 2, column = 0)

frame6 = Frame(master)
frame6.grid(row = 2, column = 1)


#master.configure(bg='gray')

r = 20   # number of rows
c = 8    # number of columns for 8 bit digital channels
tmbyt = 5 # time bytes   gives a max time ~ 3 hrs


# selection of port number
import serial.tools.list_ports       # search com port
ports = list(serial.tools.list_ports.comports())
print("available ports...")
for p in ports:
    print(p)
ser = serial.Serial()
i = 0  # change the number to find appropriate port number
ser.port = (p[int(i)])
#ser.port = ('COM7')
ser.open()
print("")
print("selected port..."+ser.port)




#####
tm = [0 for y in range(r)]
st = [[0 for x in range(c)] for y in range(r)]
get_bin = lambda x, n: format(x,'b').zfill(n)  # converts decimal to binary with n being number of bits

lstr = [0]
lend = [0]
lnum = [0]

lstr2 = [0]
lend2 = [0]
lnum2 = [0]



def save():
    text_tm = str(tm)
    text_st = str(st)
    text_lstr = str(lstr)
    text_lend = str(lend)
    text_lnum = str(lnum)
    text_lstr2 = str(lstr2)
    text_lend2 = str(lend2)
    text_lnum2 = str(lnum2)
    
    with open("test.txt", "w") as f:
        f.writelines(text_lstr + "\n" + text_lend + "\n" + text_lnum + "\n" + text_lstr2 + "\n" + text_lend2 + "\n" + text_lnum2 + "\n" + text_tm + "\n" + text_st)

def recall():
    with open("test.txt", "r") as f:
        f.readlines()
    print(f.seek(0))
    print(f.seek(1))
    print(f.seek(2))
    print(f.seek(3))
    print(f.seek(4))
    
       
    
def trigger():
    ser.write(bytearray([114]))  # sends 'r' for trigger
#    print("r")

def var_states():
#    Label(frame3, text="<--start").grid(row = int(loopstr.get())+1, column = c+2, sticky=W)
#    Label(frame3, text="<--end").grid(row = int(loopend.get())+1, column = c+2, sticky=W)

    for j in range(r):
        tm[j] = get_bin(int(time[j].get()),8*tmbyt)

        for i in range(c):
            st[j][i] = int(state[j][i].get())
#    print(tm)
#    print(st)
    ser.write(bytearray([119]))  # sends 'w' for handshaking
    rows = get_bin(r,16)    # converts 'rows' into binary with number of bits = 16 
    ser.write(bytearray([int(rows[0:8],2)]))  # sends 1st byte of rows
    ser.write(bytearray([int(rows[8:16],2)])) # sends 2nd byte of rows
#    print(get_bin(119,8))
#    print(rows[0:8])
#    print(rows[8:16])

    lstr[0] = get_bin(int(loopstr.get()),8)  # 1st loop start 
    lend[0] = get_bin(int(loopend.get()),8)  # 1st loop end
    lnum[0] = get_bin(int(loopnum.get()),16) # 1st number of loops
#    print(lstr)
#    print(lend)
#    print(lnum)
    ser.write(bytearray([int(lstr[0][0:8],2)]))  # sends 1st loop start step
    ser.write(bytearray([int(lend[0][0:8],2)]))  # sends 1st loop end step
    ser.write(bytearray([int(lnum[0][0:8],2)]))  # sends 1st number of loops 1st byte
    ser.write(bytearray([int(lnum[0][8:16],2)])) # sends 1st number of loops 2nd byte
    
    lstr2[0] = get_bin(int(loopstr2.get()),8)  # 2nd loop start
    lend2[0] = get_bin(int(loopend2.get()),8)  # 2nd loop end
    lnum2[0] = get_bin(int(loopnum2.get()),16) # 2nd number of loops
#    print(lstr2)
#    print(lend2)
#    print(lnum2)
    ser.write(bytearray([int(lstr2[0][0:8],2)]))  # sends 2nd loop start step
    ser.write(bytearray([int(lend2[0][0:8],2)]))  # sends 2nd loop end step
    ser.write(bytearray([int(lnum2[0][0:8],2)]))  # sends 2nd number of loops 1st byte
    ser.write(bytearray([int(lnum2[0][8:16],2)])) # sends 2nd number of loops 2nd byte



    for l in range(r):
        serst = ''
        for k in range(c):
            serst = serst + str(st[l][k])
#        print(int(serst,2))
        ser.write(bytearray([int(serst,2)])) # sends all the rows of channel states
#        print(serst)
        
        for m in range(tmbyt):
            ser.write(bytearray([int(tm[l][8*m:8*(m+1)],2)])) # sends time data
#            print( tm[l][8*m:8*(m+1)] )
    for m in range(tmbyt+round(c/8)):
        ser.write(bytearray([r]))  # sends extra bytes (full word) for finishing		
    
##### this part is for setting up the main frame with the appearance
time = [0 for y in range(r)]
for j in range(r):
    time[j] = StringVar(value = 10000000 )  # sets some default time values
    Entry(frame3,textvariable = time[j], width = 10).grid(row=j+1,column=1)

state = [[0 for x in range(c)] for y in range(r)]
for j in range(r):
    for i in range(c):
        state[j][i] = IntVar(value = ((i-j)%12)==8)  # sets some initial states
        Checkbutton(frame3,font=('times', 5, 'normal'), height = '1', width ='4', indicatoron = '0', selectcolor = '#00FF00', bg = '#006600', variable=state[j][i]).grid(row=j+1,column = i+2)
#        e = Checkbutton(frame4, variable=var1,font=('verdana', 6, 'normal'), height = '1', width ='2', indicatoron = '0', selectcolor = '#00FF00', bg = '#006600')

##### label different rows and columns
Label(frame3, text="Time-step").grid(row = 0, column = 0)
Label(frame3, text="time(10ns)").grid(row = 0, column = 1)
for j in range(r):
    time_step = "Step " + str(j)
    Label(frame3, text=time_step).grid(row = j+1, column = 0)
for j in range(c):
    Chan = "Ch" + str(j)
    Label(frame3, text=Chan).grid(row = 0, column = j+2)

        
Label(frame4, text="Loop1:").grid(row = 0, column = 0, sticky=W)
Label(frame4, text="start1").grid(row = 1, column = 0, sticky=E)
Label(frame4, text="end1").grid(row = 2, column = 0, sticky=E)
Label(frame4, text="num1").grid(row = 3, column = 0, sticky=E)

Label(frame4, text="Loop2:").grid(row = 4, column = 0, sticky=W)
Label(frame4, text="start2").grid(row = 5, column = 0, sticky=E)
Label(frame4, text="end2").grid(row = 6, column = 0, sticky=E)
Label(frame4, text="num2").grid(row = 7, column = 0, sticky=E)

loopstr = StringVar(value = 4 )  # 1 sec initial time
Entry(frame4, textvariable = loopstr, width = 6).grid(row = 1,column=1, sticky=W)

loopend = StringVar(value = 7 )  # 1 sec initial time
Entry(frame4,textvariable = loopend, width = 6).grid(row=2,column=1, sticky=W)

loopnum = StringVar(value = 4 )  # 1 sec initial time
Entry(frame4,textvariable = loopnum, width = 6).grid(row=3,column=1, sticky=W)

loopstr2 = StringVar(value = 9 )  # 1 sec initial time
Entry(frame4, textvariable = loopstr2, width = 6).grid(row = 5,column=1, sticky=W)

loopend2 = StringVar(value = 14 )  # 1 sec initial time
Entry(frame4,textvariable = loopend2, width = 6).grid(row=6,column=1, sticky=W)

loopnum2 = StringVar(value = 3 )  # 1 sec initial time
Entry(frame4,textvariable = loopnum2, width = 6).grid(row=7,column=1, sticky=W)


ttk.Button(frame4, text="load", width = 8, command = var_states).grid(row=12, column=0, columnspan=2)
ttk.Button(frame4, text="save", width = 8, command = save).grid(row=9, column=0, columnspan=2)
ttk.Button(frame4, text="recall", width = 8, command = recall).grid(row=10, column=0, columnspan=2)
ttk.Button(frame4, text="trigger", width = 8, command = trigger).grid(row=13, column=0,columnspan=2)
Label(frame4, text=" ", height = r-12).grid(row=11,column=0)
Label(frame4, text=" ").grid(row=8,column=0)

mainloop()
ser.close()    
