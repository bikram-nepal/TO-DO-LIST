from tkinter import *
import speech_recognition as sr
#we will create calendar by importing tkcalendar which is a package of tkinter
from tkcalendar import *

#we will import messagebox so as to show warning or information or ask anything for confirmation

from tkinter import messagebox

import random 
# we will create a window which shows a window containing calendar
window=Tk()
theme="#0047bc"

f = open('data.txt','r')#it opens the file in read format.

tasks =f.read().split('\n')#it read the file
f.close()#it closes the file



window.title("Calendar")
window.geometry("600x400")
cal=Calendar(window, selectmode="day",year=2020,month=10,day=10)
cal.pack()

#voice command



# we will define a function to get a date from calendar
def grab_date():

    my_label9.config(text="Today's Date is :" + cal.get_date() )

my_button9=Button(window,text="Get Date",bg=theme,fg="white",font=("bold",11),command=grab_date)
my_button9.pack(pady=20)

my_label9=Label(window,text="")
my_label9.pack(pady=20)


# we will define a function which will create separete to-do list for different dates
def open_todo():
    root=Toplevel()

#we will  change root window bg colour
    root.configure(bg="white")

#we will create title
    root.title("Todo-Helper-For-You")

#we will  set window size
    root.geometry("600x400")

#we will Get date
    todo_date=cal.get_date()

    def voice():
        try:
            voice_text["text"]="Give command..."
            root.update()

            rec=sr.Recognizer()
            with sr.Microphone(device_index=1) as source:
                rec.pause_threshold = 1
                audio = rec.listen(source)

                text= rec.recognize_google(audio,language='en-in')


                if text.lower()=='add task':
                    voice_text["text"]="What task do you want to add?"
                    root.update()
                    rec.pause_threshold =1
                    task= rec.listen(source)
                    text_task= rec.recognize_google(task,language='en-in')
                    addtask_main(text_task)
                    voice_text["text"]=text_task+" added!!"

                elif text.lower()=="delete a task":
                    delete_task()
                    voice_text["text"]="Task deleted!!"

                elif text.lower()=='random task':
                    random_task()
                    voice_text["text"]="This is your random task: "
                elif text.lower()=='delete all':
                    delete_all()
                    
                elif text.lower()=='number of task':
                    num_tasks()
                    voice_text["text"]="Number is shown!!"
                elif text.lower()=='sort ascending':
                    sort_ascending()
                    voice_text["text"]="Sorted ascending!!"
                elif text.lower()=='sort descending':
                    sort_descending()
                    voice_text["text"]="Sorted descending!!"   
                elif text.lower()=="exit":
                    leave()
                else:
                    voice_text["text"]="Unmatched input command!!"
                root.update()
        except:
            voice_text["text"]='I cant hear you.'









    def update_listbox():
        if tasks:
    #  here we will first clear the current listbox
            clear_listbox()
        #we will Populate listbox by appending each task to list
            for task in tasks:
                task=task.split("%")
                if task[1]==todo_date:
                    my_listbox.insert("end"," ➡ " + task[0])
            root.update()

    def clear_listbox():
        my_listbox.delete(0, "end")
        root.update()

    def addtask_main(task):
        if task !="":
            tasks.append(task+"%"+todo_date)# we will create a tuple to create a to-do task
            string = '\n'.join(tasks)
            f = open('data.txt','w')
            f.write(string)
            f.close()

            update_listbox()
            root.update()   
        else:
            messagebox.showwarning("Note!", "Please enter a task")# it shows warning 
            # it will clear the textbox to avoid adding the same task twice accidentally
        text_input.delete(0, "end")

        root.update()

    def add_task(event=None):
         # here "event=None" is added  so that enter key can add task without clicking the button
         # we will get input from user
        task = text_input.get()
        addtask_main(task)
            # Ensure user has enetered a task
        root.update()
    root.bind('<Return>', add_task)# bind return key to add_task so that enter key can add task without clicking the button

        


    def num_tasks():# defining a function to show number of tasks
        num_tasks=0
        try:
            for task in tasks:
                task=task.split("%")

                if task[1]==todo_date:
                    num_tasks +=1
        except:
            num_tasks=0

        msg = "There are {} tasks in the list".format(num_tasks)
        label_display["text"]=msg
        root.update()



    def delete_task():# defining a function to delete a task

        #No, we will Get the text of the currently selected item
        task = my_listbox.get("active")[3:]
        # Confirm task is in list
        for i in tasks:
            j=i.split("%")
            if j[0]==task:
                confirm_del = messagebox.askyesno("Confirm Deletion","Are you sure you want to delete task:   ** {} ** ?".format(task))
                if confirm_del:# tkmessageBox.askyesno  and returns boolean value
                    tasks.remove(i)
        string = '\n'.join(tasks)
        f = open('data.txt','w')
        f.write(string)
        f.close()

        update_listbox()
        root.update()

# we will sort the given tasks in ascending and descending order as per alphabetical order
    def sort_ascending():
        if len(tasks)>=1:
            tasks.sort()
            update_listbox()
        else:
            messagebox.showinfo("Information","There are no tasks in to-do list.")
        root.update()



    def sort_descending():
        if len(tasks)>=1:
            tasks.sort()# sorting the array
            tasks.reverse()#reversing the array
            update_listbox()# it updates the listbox
        else:
            messagebox.showinfo("Information","There are no tasks in to-do list.")

        root.update()



    def random_task():# it helps in selecting a random tasks
        if len(tasks)>=1:
            task = random.choice(tasks)
            # Update display label
            label_display["text"]=task.split("%")[0]
        else:
            messagebox.showinfo("Info","There are no tasks in to-do list.")
        root.update()
            

    def delete_all():
        # As list is being changed, it needs to be global.
        global tasks
        confirm_del = messagebox.askyesno("Delete All Confirmation", "Are you sure you want to delete all tasks?")
        print(int(confirm_del))
        if int(confirm_del)==1:
        # Clear the tasks list.
            tasks = ["None%None"]
            clear_listbox()
            voice_text["text"]="All tasks are deleted!!"
            root.update()

        string = '\n'.join(tasks)
        f = open('data.txt','w')
        f.write(string)
        f.close()

        update_listbox()
        root.update()



    def leave():
        root.quit()
        

    root.bind('<Return>', add_task)

    # Create title in root widget of GUI with white background
    label_title =Label(root, text="Today's-To-Do-List",font=("bold",11), bg="white")
    label_title.grid(row= 0, column=0 )
    #it will create a empty level which adds some spaces

    label_display =Label(root, text="", bg="white",font=("bold",11))
    label_display.grid(row=0 , column=1 )

#now we will take an entry in listbox
    text_input =Entry(root, width = 50)
    text_input.grid(row=1 , column=1 )

# we will create different buttons to perform different tasks

    button_add_task =Button(root, text="Add Task",bg=theme,fg="white",font=("bold",11),width=20, command=add_task)
    button_add_task.grid(row= 1, column=0 )


    button_num_tasks =Button(root, text="Number of Tasks",bg=theme,fg="white", font=("bold",11),width=20,command=num_tasks)
    button_num_tasks.grid(row=3 , column= 0)

    button_delete_task =Button(root, text="Delete A  Task", bg=theme,fg="white",font=("bold",11),width=20, command=delete_task)
    button_delete_task.grid(row=4 , column=0 )
    


    button_delete_all =Button(root, text="Delete All ", bg=theme,fg="white",font=("bold",11),width=20, command=delete_all)
    button_delete_all.grid(row=5 , column= 0)

    button_sort_ascending =Button(root, text="Sort  Ascending", bg=theme,fg="white",font=("bold",11),width=20, command=sort_ascending)
    button_sort_ascending.grid(row=6 , column=0 )

    button_sort_descending =Button(root, text="Sort  Descending", bg=theme,fg="white",font=("bold",11),width=20, command=sort_descending)
    button_sort_descending.grid(row=7 , column=0 )

    button_random_task = Button(root, text=" Random Task", bg=theme,fg="white", font=("bold",11),width=20,command=random_task)
    button_random_task.grid(row=8 , column=0 )

    button_voice = Button(root, text="Voice command", bg=theme,fg="white", font=("bold",11),width=20,command=voice)
    button_voice.grid(row=9, column=0 )

    button_quit_program =Button(root, text="Exit", bg=theme,fg="white",font=("bold",11),width=20, command=leave)
    button_quit_program.grid(row=10 , column=0 )

    #we will create a listbox to display our tasks

    my_listbox= Listbox(root,width=40,fg=theme,font=("bold",11))
    my_listbox.grid(row=2 , column=1, rowspan=7,padx=5, )

    voice_text=Label(root, text="", bg="white",font=("bold",11))
    voice_text.grid(row=10, column=1)


    # we will create a function to show all the tasks in listbox

    def show_listbox():
        global tasks
        for task in tasks:
            task=task.split("%")
            if task[1]==todo_date:
                my_listbox.insert("end"," ➡ " + task[0])
    #Populate listbox at program start for future file io functionality
    show_listbox()


view_button=Button(window,text="View To-Do",bg=theme,fg="white",font=("bold",12),width=16,height=2,command=open_todo)
view_button.pack(pady=20)
window.mainloop()


    # Start the main events loop

