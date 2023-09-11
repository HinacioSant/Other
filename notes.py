import tkinter as tk
from tkinter import font
import sqlite3
import os

# Add to the database
def input_action(input_field):
    content = input_field.get()
    print(content)
    conn = sqlite3.connect(database_file)

    cursor = conn.cursor()

    # Insert to the database
    cursor.execute('''INSERT INTO notes (body, type)
                    VALUES (?, ?)''', (content, 1))

    conn.commit()
    cursor.close()
    conn.close()

    input_field.delete(0, tk.END)
    input_field.focus_set()



def delete_all():
# Delete ALL database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute(''' DELETE FROM notes ''')
    conn.commit()
    cursor.close()
    conn.close()


def get_notes(database_file, table_name):
    # Returns a list o notes already formated
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    all = cursor.execute(f''' SELECT * FROM {table_name} ''')
    note_list = []
    for a in all:
        note_text = f"[{a[0]}] - {a[1]}"
        note_list.append(note_text)

    cursor.close()
    conn.close()
    return note_list


# function to change properties of button on hover
def change_hover(button, colorOnHover, colorOnLeave):

    # adjusting background of the widget
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(
        fg=colorOnHover))

    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(
        fg=colorOnLeave))

# Notes display


class Base_of_frame(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family="System", size=35)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Home_frame, Notes_frame):
            page_name = F
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Home_frame)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()


class Home_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')

        label = tk.Label(self, text="ᚾᛟᛏᛖᛊ", font=controller.title_font, fg="#00ff00", bg="black")
        label.pack(side="top", fill="x", pady=10)

        custom_font = font.Font(family="System", size=25)

        for i in (range(5)):
            i = tk.Label(self, text=i, font=controller.title_font, fg="#00ff00", bg="black")
            i.pack()
            change_hover(i, "#019101", "#00ff00")

        button1 = tk.Button(self, text="Notes", font=custom_font ,fg="#00ff00", bg="black", bd=0, activeforeground="#00ff00", activebackground="black", command=lambda: controller.show_frame(Notes_frame))
        button1.pack()

        change_hover(button1, "#019101", "#00ff00")

class Notes_frame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(background='black')


        custom_font = font.Font(family="System", size=25)
        notes_font = font.Font(family="System", size=15)


        button1 = tk.Button(self, text="Home", font=custom_font ,fg="#00ff00", bg="black", bd=0, activeforeground="#00ff00", activebackground="black", command=lambda: controller.show_frame(Home_frame))
        button1.pack()

        change_hover(button1, "#019101", "#00ff00")
        # Input
        input_field = tk.Entry(self, font=custom_font, fg="#00ff00", bg="black", insertbackground='#00ff00', width=17)

        note_list = get_notes(database_file, 'notes')
        for note in note_list:
            note = tk.Label(self, text=note,  font=notes_font ,fg="#00ff00", bg="black")
            note.pack()



        # Pack input
        input_field.pack(side="bottom", pady=10)

        input_field.bind('<Return>', lambda event: input_action(input_field))

        input_field.focus()



if __name__ == '__main__':
    database_file = "mydatabase.db"
    # check if file exists | create database if the file does not exists.
    if not os.path.isfile(database_file):
        # connect to the database
        conn = sqlite3.connect(database_file)

        # create a table
        conn.execute('''CREATE TABLE notes
                       (id INTEGER PRIMARY KEY,
                        body TEXT,
                        type INTEGER)''')

        # commit the changes and close the connection
        conn.commit()
        conn.close()

    app = Base_of_frame()
    app.geometry("335x560")
    app.title("ᚾᛟᛏᛖᛊ")
    app.iconbitmap("icon.ico")

    app.mainloop()
