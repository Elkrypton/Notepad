# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 13:53:41 28  017

@author: Mr Crypton
"""

#from Tkinter import *
import tkinter.filedialog as dial
import os
from tkinter import *
import tkinter as tk
#import pdf

filename = None 
global filenamew

root = Tk()


  # def ChangeTheme():

  #   chose = part.get()

  #   if chose == 1:
  #     content_text.configure(background='black',foreground='green')


def find_text(event=None):

    search_toplevel = Toplevel(root)
    search_toplevel.title("Find Text")
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0,column=0,sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0,column=1,padx=2,pady=2,sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel,text='Ignore Case',
                variable=ignore_case_value).grid(row=1,column=1,sticky='e',
                                                 padx=2,pady=2)

    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(search_entry_widget.get(),
            ignore_case_value.get(),content_text,search_toplevel,
                                         search_entry_widget)).grid(row=0,
                                        column=2,sticky='e' + 'w',padx=2,pady=2)

    def close_search_window():

      content_text.tag_remove('match','1.0',END)
      search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW',close_search_window)
    return "break"

    close_search_window()


def search_output(needle, if_ignore_case,content_text,search_toplevel,search_box):


    content_text.tag_remove('match','1.0',END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle, start_pos,nocase=if_ignore_case,stopindex=END)
            #print("This is the start : ", start_pos)
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos,len(needle))
            #print('This is the end pos : ', end_pos)
            content_text.tag_add('match',start_pos,end_pos)
            matches_found += 1
            start_pos = end_pos

        content_text.tag_config('match',foreground='red',background='yellow')

    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))
    
    

def open_file(event=None):

  input_file_name = dial.askopenfilename(defaultextension='.txt',
    filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

  if input_file_name:

      if input_file_name.endswith(".pdf"):
        global filename
        filename = input_file_name
        root.title("{}".format(os.path.basename(filename)))
        content_text.delete(1.0,END)
        with open(filename) as pdffile:
            content_text.insert(1.0,pdf.getTextPDF(pdffile))



  filename = input_file_name 
  root.title("{}".format(os.path.basename(filename)))
  content_text.delete(1.0,END)

  with open(filename) as _file:
      content_text.insert(1.0,_file.read())

def save(event=None):

  global filename 
  if not filename:
    save_as() 

  else:
    write_to_file(filename)
  return "break"

def save_as(event=None):

  input_file_name = dial.asksaveasfilename(defaultextension='*.txt',
    filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
  if input_file_name:
    global filename 
    filename = input_file_name 
    write_to_file(filename)

    root.title("{}".format(os.path.basename(filename)))
  return "break"

def write_to_file(filename):

  try:
    content = content_text.get(1.0,'end')
    with open(filename,'w') as the_file:
      the_file.write(content)

  except IOError:
    pass

def new_file(event=None):
  root.title("Untitled")
  global filename 
  filename = None 
  content_text.delete(1.0,END)


def on_content_changed(event=None):

  update_line_numbers()
  update_cursor_bar_info()

def show_cursor_info_bar():

  cursor_bar_checked = show_bar_info.get()

  if cursor_bar_checked:
    cursor_info_bar.pack(expand='no',fill='none',side='right',anchor='se')
  else:
    cursor_info_bar.pack_forget()

def update_cursor_bar_info(event=None):

  row,col = content_text.index(INSERT).split('.')
  line_num, col_num = str(int(row)), str(int(col) + 1)
  info_txt = "Line : {0} | Column : {1}".format(line_num,col_num)
  cursor_info_bar.config(text=info_txt)



def get_line_numbers():

  output = ''

  if show_line.get():

    row,col = content_text.index("end").split(".")
    for i in range(1, int(row)):
      output += str(i) + '\n'

  return output 

def update_line_numbers(event=None):

  line_numbers = get_line_numbers()
  line_bar.config(state='normal')
  line_bar.delete('1.0',END)
  line_bar.insert('1.0',line_numbers)
  line_bar.config(state='disabled')


def highlight_current(interval=100):

  content_text.tag_remove("active_line",1.0,'end')
  content_text.tag_add("active_line","insert linestart","insert lineend+1c")
  content_text.after(interval,toggle_highlight)
  content_text.tag_configure('active_line',background='ivory2')

def undo_highlight():

  content_text.tag_remove('active_line',1.0,'end')

def toggle_highlight(event=None):

  if to_highlight_line.get():
    highlight_current()

  else:
    undo_highlight()

def change_theme(event=None):

  selected_theme = themes_choice.get()
  fg_bg_color = color_schemes.get(selected_theme)
  fg_color,bg_color = fg_bg_color.split('.')
  content_text.config(bg=bg_color,fg=fg_color)




def cut():
      
      content_text.event_generate("<<Cut>>")

def copy():
      
      content_text.event_generate("<<Copy>>")

def paste():
      
      content_text.event_generate("<<Paste>>")

def select_all(event=None):
      
      content_text.tag_add('sel','1.0','end')
      return "break"
      
def undo():
      
      content_text.event_generate("<<Undo>>")

def redo(event=None):
      
      content_text.event_generate("<<Redo>>")
      return 'break'


shortcut_bar = Frame(root,height=25,background = "light sea green")
shortcut_bar.pack(expand='no',fill='x')
line_bar = Text(root,width=4,padx=3,background="khaki",border=1,takefocus=0,state='disabled',wrap='none')
line_bar.pack(side='left',fill='y')
content_text = Text(root ,wrap='word',undo=1)
content_text.pack(expand='yes',fill='both')


scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side="right",fill="y")
menu_bar = Menu(root,bg='black',fg='white')
file_menu = Menu(menu_bar,tearoff=0,bg='black',fg='white')
file_menu.add_command(label="New",accelerator='Ctrl+N',command=new_file)
file_menu.add_command(label="Open",accelerator="Ctrl+O",compound='left',command=open_file)
file_menu.add_command(label="Save",accelerator="Ctrl+S",command=save)
file_menu.add_command(label="Save as", accelerator="Shift+Ctrl+S",command=save_as)
file_menu.add_command(label="Exit",accelerator="Alt+F4")
menu_bar.add_cascade(label="File",menu=file_menu)
file_menu.add_separator()
content_text.bind("<Control-Y>",redo)
content_text.bind("<Control-A>",select_all)
content_text.bind("<Control-f>",find_text)
content_text.bind("<Control-F>",find_text)
content_text.bind("<Control-N>",new_file)
content_text.bind("<Control-n>",new_file)
content_text.bind("<Control-O>",open_file)
content_text.bind("<Control-o>",open_file)
content_text.bind("<Control-S>",save)
content_text.bind("<Control-s>",save)
content_text.bind("<Any-KeyPress>",on_content_changed)
content_text.bind("<Control-t>",change_theme)
content_text.bind("<Control-T>",change_theme)
cursor_info_bar = Label(content_text, text="Line : 1 | Column : 1")
#cursor_info_bar.pack(expand=NO, fill=None,side=RIGHT,anchor='se')


content_text.bind("<Control-a>",select_all)
edit_menu = Menu(menu_bar,tearoff=0,bg='black',fg='white')
edit_menu.add_command(label="Cut",accelerator="Ctrl+X",command=cut)
edit_menu.add_command(label="Copy",accelerator="Ctrl+C",command=copy)
edit_menu.add_command(label="Select all",accelerator="Ctrl+A",command=select_all)
edit_menu.add_command(label="Paste",accelerator="Ctrl+V",command=paste)
edit_menu.add_command(label="Undo",accelerator="Ctrl+Z",command=undo)
edit_menu.add_command(label="Redo",accelerator="Ctrl+Y",command=redo)
edit_menu.add_command(label="Find",accelerator="Ctrl+F")
edit_menu.add_command(label="Find",underline=0,accelerator="Ctrl+F",command = find_text)


menu_bar.add_cascade(label="Edit",menu=edit_menu)
edit_menu.add_separator()
view_menu = Menu(menu_bar,tearoff=0,bg='black',fg='white')
show_line = IntVar()
show_line.set(1)
to_highlight_line = BooleanVar()
show_bar_info = IntVar()
show_cursor = Checkbutton(view_menu)
highlight_line = Checkbutton(view_menu)
show_info = Checkbutton(view_menu)
view_menu.add_checkbutton(label="Show Line Number", variable = show_line)
#view_menu.add_checkbutton(label="Show info bar at the bottom",variable=show_info)
#view_menu.add_checkbutton(label="Highlight current line",variable=highlight_line)
view_menu.add_checkbutton(label="Show cursor location at the bottom", variable=show_bar_info,command=show_cursor_info_bar)
view_menu.add_checkbutton(label="Highlight current line",onvalue=1,offvalue=0,
  variable=to_highlight_line,command=toggle_highlight)
themes_menu = Menu(view_menu,tearoff=0,bg='black',fg='white')
view_menu.add_cascade(label="Themes", menu=themes_menu)
# default = StringVar()
# Greygrarious = StringVar()
# Aquamarine = StringVar()
# BoldBeig = StringVar()
# CobaltBlue = StringVar()
# OliveGreen = StringVar()
# NightMode = StringVar()
themes_choice = StringVar()
themes_menu.add_radiobutton(label="Default",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Greygrarious",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Aquamarine",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Bold Beig",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Cobalt Blue",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Olive Green",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Night Mode",variable=themes_choice,command=change_theme)
themes_menu.add_radiobutton(label="Green Mode",variable=themes_choice,command=change_theme)

color_schemes = {


  'Default': '#000000.#FFFFFF',
  'Greygrarious': '#83406A.#D1D4D1',
  'Aquamarine':'#5B8340.#D1E7E0',
  'Bold Beig':'#4B4620.#FFF0E1',
  'Cobalt Blue' : '#ffffBB.#3333aa',
  'Olive Green': '#D1E7E0.#5B8340',
  'Night Mode':'#FFFFFF.#000000',
  'Green Mode':'#49BD1B.#000000',

}


themes = ["Default","Greygrarious","Aquamarine","Bold Beig","Cobalt Blue","Olive green",'Night Mode']
#values = [1,2,3,4,5,6]
# for theme in themes:


#     themes_menu.add_radiobutton(label=theme,
#                                   variable = theme_choice,
#                                   value =+ 1,command=change_theme)
# background_image=tk.PhotoImage("background.jpg")
# background_label = tk.Label(content_text, image=background_image)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
menu_bar.add_cascade(label="View",menu=view_menu)
view_menu.add_separator()
help_menu = Menu(menu_bar, tearoff=0,bg='black',fg='white')
help_menu.add_command(label="Help")
help_menu.add_command(label="About")
menu_bar.add_cascade(label="Help",menu=help_menu)



root.config(menu=menu_bar)
root.geometry("10x300")
root.title("My Own Notepad")
root.mainloop()
