from tkinter import *
  
root = Tk()
  
root.geometry( "200x200" )

options = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
  
clicked = StringVar()
  
clicked.set("Monday")
  
drop = OptionMenu( root , clicked , *options )
drop.pack()

v = Scrollbar(root, orient='vertical')
t = Text(root, width = 15, height = 15, wrap = NONE, yscrollcommand = v.set)
for i in range(20):
    t.insert(END,"this is some text\n")
t.pack(side=TOP, fill=X)
v.config(command=t.yview)
# Create Label
label = Label( root , text = " " )
label.pack()
  
# Execute tkinter
root.mainloop()