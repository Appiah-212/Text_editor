from tkinter import*

import tkinter.filedialog 
import os

import tkinter.messagebox 


def Cut(on_content_changed=None):
    text.event_generate("<<Cut>>")
       
    
def Copy(on_content_changed=None):
    text.event_generate("<<Copy>>")
    

def Paste(event=None):
    text.event_generate("<<Paste>>")
    on_content_changed()
    
    

def Undo(event=None):
    text.event_generate("<<Undo>>")
    on_content_changed()
    
    

def Redo(event=None):
    text.event_generate("<<Redo>>")
    on_content_changed()
    

def Find(event=None):
    find_text=Toplevel(root)
    find_text.title("Find")
    find_text.geometry("320x100")
    find_text.iconbitmap(bitmap='Love_text.ico')
    find_text.transient(root)
    find_text.resizable(width=0,height=0)
    
    Label(find_text,text="Find All:",font=('Verdana',10,'')).grid()
    entry=Entry(find_text,width=25,font=('Verdana',10,''))
    entry.grid(row=0,column=1,pady=5,sticky='we')
    entry.focus_set()
    ignore_case_value=IntVar()
    Checkbutton(find_text,text="ignore case",variable=ignore_case_value).grid(row=1,column=1,pady=4,sticky='we')    
    Button(find_text,text="Find",font=('Verdana',10,''),command=lambda: search(entry.get(),ignore_case_value.get(),text,find_text,entry)).grid(row=0,column=2,sticky='w',padx=3,pady=3)
    
def search(myword,ignore_case,text,find_text,search_box):
    text.tag_remove('match','1.0',END)
    matches_found=0
    if myword:
       start_position='1.0'
       while True:
        start_position=text.search(myword,start_position,nocase=ignore_case,stopindex=END)
        if not start_position:
            break
        end_position='{}+{}c'.format(start_position,len(myword))
        text.tag_add('match',start_position,end_position)
        matches_found+=1
        start_position=end_position
       text.tag_config('match',background='#AACCDD',foreground='red')
    search_box.focus_set()   
    find_text.title('{} matches found'.format(matches_found))


file_name=None

def open_file(event=None):
    input_file_name=tkinter.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All file types","*.*"),("Text documents",".txt")])
    if input_file_name:
        global file_name
        file_name=input_file_name
        root.title('{}-{}'.format(os.path.basename(file_name),"LoveText"))
        text.delete(1.0,END)
        with open(file_name) as file:
              text.insert(1.0, file.read())
    on_content_changed()          
              

             

def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
        return "break"


def save_as(event=None):
    input_file_name=tkinter.filedialog.asksaveasfilename(defaultextension= ".txt", filetypes=[("All files", "*.*"),("Text documents", ".txt")])
    if input_file_name:
        global file_name
        file_name=input_file_name
        write_to_file(file_name)
        root.title('{}-{}'.format(os.path.basename(file_name), "LoveText"))
    return "break"                  

def write_to_file(event=None):
    try:
        content= text.get(1.0,END)
        with open(file_name,'w') as _file:
            _file.write(content)
    except IOError:
        pass
    


def new_file(event=None):
    root.title("Untitled")
    global file_name
    file_name=None
    text.delete(1.0, END)
    on_content_changed()
    

    



def Help_messagebox(event=None):
    tkinter.messagebox.showinfo("Help:","Call for more info",icon='question')
    showinfo_text=Text(font='blue')
    
    



def About_messagebox(event=None):
    tkinter.messagebox.showinfo("About:", "{}{}".format("LoveText", "\nPython text editor developed by Kubiman"))
    


def exit_messagebox(event=None):
    if tkinter.messagebox.askokcancel("Quit?","Do you want to really quit?"):
        root.destroy()


def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root,event.y_root,0)




def select_all(event=None):
    text.tag_add(SEL,1.0,END)
    return "break"



def on_content_changed(event=None):
    update_line_number()
    update_status_bar()



def get_line_numbers():
    output= ''
    if show_line_number.get():
        row,col=text.index("end").split('.')
        for i in range(1,int(row)):
            output+= str(i)+'\n'
    return output


def update_line_number(event=None):
    line_numbers= get_line_numbers()
    line_number_bar.config(state="normal")
    line_number_bar.delete('1.0',"end")
    line_number_bar.insert('1.0',line_numbers)
    line_number_bar.config(state="disabled")



def show_status_bar():
    show_status_bar_checked=stat_bar.get()
    if show_status_bar_checked:
        status_bar.pack(side=BOTTOM,fill=X)

    else:
        status_bar.pack_forget()


def update_status_bar(event=None):
    row,col=text.index("insert").split('.')
    line_num,col_num=str(int(row)),str(int(col)+1)
    infotext='Line: {0} | Column: {1}'.format(line_num,col_num)
    status_bar.config(text=infotext)


def change_theme(event=None):
    selected_theme=theme_choice.get()
    fg_bg_colors=color_chooser.get(selected_theme)
    foreground_color,background_color=fg_bg_colors.split('.')
    text.config(bg=background_color,fg=foreground_color)



def highlight_line(interval=100):
    text.tag_remove("active_line",1.0,END)
    text.tag_add("active_line","insert linestart","insert lineend+1c")
    text.after(interval,toggle_highlight)

def undo_highlight():
    text.tag_remove("active_line",1.0,END)
    



def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()

    else:
        undo_highlight()

    text.tag_configure('active_line', background='ivory2')  

    

    
    
     
root=Tk()



newImage=PhotoImage(file="New_icon.png")
copyImage=PhotoImage(file="Copy_icon.png")
openImage=PhotoImage(file="Open_folder.png")
saveImage=PhotoImage(file="Save_icon.png")
saveasImage=PhotoImage(file="Save_as_icon.png")
exitImage=PhotoImage(file="Exit_icon.png")
undoImage=PhotoImage(file="Undo_icon.png")
redoImage=PhotoImage(file="Redo_icon.png")
cutImage=PhotoImage(file="Cut_icon.png")
pasteImage=PhotoImage(file="Paste_icon.png")
findImage=PhotoImage(file="Find_icon.png")


shortcut_bar=Frame(root,height=30,bg="white")
icons=('new_file','open_file','save','Cut','Copy','Paste','Undo','Redo','Find')
for icon in (icons):
    toolbar_icon=PhotoImage(file='icons/{}.png'.format(icon))
    cmd=eval(icon)
    toolbar=Button(shortcut_bar,image=toolbar_icon,relief=FLAT,command=cmd)
    toolbar.image=toolbar_icon
    toolbar.pack(side=LEFT)
shortcut_bar.pack(expand='no',fill=X,padx=4)

line_number_bar=Text(root,width=3,padx=3,takefocus=0,border=0,background='#AACCDD',state='disabled',wrap=NONE)
line_number_bar.pack(side=LEFT,fill=Y)


text=Text(root,wrap=WORD,undo=1,background='white',selectbackground='#AACCDD',cursor='heart',state=NORMAL)
text.pack(fill=BOTH,side=TOP,expand='yes')



scroll_bar=Scrollbar(text)
text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.configure(command=text.yview)
scroll_bar.pack(fill=Y,side=RIGHT)

status_bar=Label(text,text='Line: 1  | Column: 1',font=('Verdana',10,''),anchor='ne')
status_bar.pack(side=BOTTOM,fill=X)

color_chooser={
'Default': '#000000.#FFFFFF',
'Greygarious':'#83406A.#D1D4D1',
'Aquamarine': '#5B8340.#D1E7E0',
'Bold Beige': '#4B4620.#FFF0E1',
'Cobalt Blue':'#ffffBB.#3333aa',
'Olive Green': '#D1E7E0.#5B8340',
'Night Mode': '#FFFFFF.#000000'
}






                   





menu=Menu(root)

File_menu=Menu(menu,tearoff=0)
Edit_menu=Menu(menu,tearoff=0)
View_menu=Menu(menu,tearoff=0)
Help_menu=Menu(menu,tearoff=0)
Themes_menu=Menu(menu,tearoff=0)


menu.add_cascade(label="File",menu=File_menu)
menu.add_cascade(label="Edit",menu=Edit_menu)
menu.add_cascade(label="View",menu=View_menu)
menu.add_cascade(label="Help",menu=Help_menu)



File_menu.add_command(label="New",accelerator='Ctrl+N',image=newImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=new_file)
File_menu.add_command(label="Open",accelerator='Ctrl+O',image=openImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=open_file)
File_menu.add_command(label="Save",accelerator='Ctrl+S',image=saveImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=save)
File_menu.add_command(label="Save as",accelerator='Shift+Ctrl+S',image=saveasImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=save_as)
File_menu.add_separator()
File_menu.add_command(label="Exit",accelerator='Alt+F4',image=exitImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=exit_messagebox)

Edit_menu.add_command(label="Undo",accelerator='Ctrl+Z',image=undoImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Undo)
Edit_menu.add_command(label="Redo",accelerator='Ctrl+Y',image=redoImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Redo)
Edit_menu.add_separator()
Edit_menu.add_command(label="Cut",accelerator='Ctrl+X',image=cutImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Cut)
Edit_menu.add_command(label="Copy",accelerator='Ctrl+C',image=copyImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Copy)
Edit_menu.add_command(label="Paste",accelerator='Ctrl+V',image=pasteImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Paste)
Edit_menu.add_command(label="Find",accelerator='Ctrl+F',image=findImage,underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Find)
Edit_menu.add_separator()
Edit_menu.add_command(label="Select All",accelerator='Ctrl+A',underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=select_all)


show_line_number=IntVar()
show_line_number.set(0)
View_menu.add_checkbutton(label="Show Line Number",variable=show_line_number,font=('Verdana',10,''),activebackground='light blue',activeforeground='black')


stat_bar=IntVar()
stat_bar.set(1)
View_menu.add_checkbutton(label="Show Status Bar",variable=stat_bar,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=show_status_bar)

to_highlight_line=BooleanVar()
View_menu.add_checkbutton(label="Highlight Current Line",variable=to_highlight_line,onvalue=1,offvalue=0,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=toggle_highlight)



theme_choice=StringVar()
theme_choice.set("1.Default")
View_menu.add_cascade(label="Themes",menu=Themes_menu,font=('Verdana',10,''),activebackground='light blue',activeforeground='black')

for k in sorted(color_chooser):
    Themes_menu.add_radiobutton(label=k,variable=theme_choice,command=change_theme,font=('Verdana',10,''),activebackground='light blue',activeforeground='black')


Help_menu.add_command(label="About",underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=About_messagebox)
Help_menu.add_separator()
Help_menu.add_command(label="Help",accelerator='F1',underline=0,foreground='black',compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=Help_messagebox)

text.bind('<Control-F>',Find)
text.bind('<Control-f>',Find)
text.bind('<Control-N>',new_file)
text.bind('<Control-n>',new_file)
text.bind('<Control-O>',open_file)
text.bind('<Control-o>',open_file)
text.bind('<Control-S>',save)
text.bind('<Control-s>',save)
text.bind('<Shift-Control-S>',save_as)
text.bind('<Shift-Control-s>',save_as)
text.bind('<Alt-F4>',exit_messagebox)
text.bind('<Control-Y>',Redo)
text.bind('<Control-y>',Redo)
text.bind('<KeyPress-F1>',Help_messagebox)
text.bind('<Control-A>',select_all)
text.bind('<Control-a>',select_all)
text.bind('<Any-KeyPress>',on_content_changed)
text.bind('<Control-V>',Paste)
text.bind('<Control-v>',Paste)










popup_menu=Menu(text,tearoff=0)
for i in('Cut','Copy','Paste','Undo','Redo'):
    cmd=eval(i)
    popup_menu.add_command(label=i,compound=LEFT,font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label="Select All",font=('Verdana',10,''),activebackground='light blue',activeforeground='black',command=select_all)
text.bind('<Button-3>',show_popup_menu)



root.geometry("600x400")
root.wm_iconbitmap(bitmap='Love_text.ico')
root.title("LoveText")

root.config(menu=menu)
mainloop()

