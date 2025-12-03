import tkinter as tk
import tkinter.font as tkFont
from tkinter import Listbox, messagebox 

#User database
users = {
    "sample": {
        "password": "123",
        "medications": [
            {
                "name": "Aspirin",
                "dosage": "100mg",
                "time": "8:00 AM",
                "symptoms": "Headache"
            }
        ]
    }
} 

current_user = None

#Main window configurations
mainWindow = tk.Tk()
mainWindow.title("MediTrack Login form")
mainWindow.geometry("350x450")
mainWindow.configure(bg = '#F0F0F0')
font1 = tkFont.Font(family = "Arial", size = 12, weight = tkFont.NORMAL)

#Dashboard Window configurations
dashboard = tk.Toplevel(mainWindow)
dashboard.title("MediTrack dashboard")
dashboard.geometry("800x450")
dashboard.configure(bg = '#F0F0F0')
dashboard.withdraw()

#Sign-in Window
signIn = tk.Toplevel(mainWindow)
signIn.title("Create new User")
signIn.geometry("350x450")
signIn.configure(bg = '#F0F0F0')
signIn.withdraw()



''' TODO: Implement history window
        CODE:
        historyWindow = tk.Toplevel(dashboard)
        historyWindow.title("Medication History")
        historyWindow.geometry("350x450")
        historyWindow.configure(bg = '#F0F0F0')
        historyWindow.withdraw() '''

label = tk.Label(mainWindow, text = "MediTrack", bg= "#F5D5F7", font = font1)
label.place(x= 125,y=0)

def login():
    global users
    global current_user
    username = userEntry.get().strip()
    password = passEntry.get().strip()
    print("attempted login:", username, password)
    
    if username in users and users[username]["password"] == password:
        current_user = username
        messagebox.showinfo(title = "Login Successful", message = f"Welcome back, {username}!")
        dashboard.deiconify()
        mainWindow.withdraw()
        updateMedListbox()
    else:
        messagebox.showinfo(title = "Login Failed", message = "Invalid username or password")
            
def signUp():
    mainWindow.withdraw()
    signIn.deiconify()
    
def createUser():   
    username = signUserEntry.get().strip()
    password = signPassEntry.get().strip()
    confirmPass = passRentry.get().strip()
    
    if username in users:
        messagebox.showinfo(title = "Sign up failed", message = "Account with this user already exists")
        
    elif password != confirmPass:
         messagebox.showinfo(title = "Invalid Password", message = "Passwords don't match")
         
    else:
        users[username] = password
        print(users)
        messagebox.showinfo(title = "User created", message = "Redirecting back to login")
        signIn.withdraw()
        mainWindow.deiconify()

#adds medication to the list if not already present
def addMedication():
    global current_user
    user_medications = users[current_user].setdefault("medications", [])

    med_input = medicationEntry.get().strip()
    dosage_input = dosageEntry.get().strip()
    time_input = timeEntry.get().strip()
    symptoms_input = symptomsEntry.get().strip()

    #input validation
    if not med_input:
        messagebox.showinfo(title="Missing input", message="Medication cannot be empty!")
        return
    
    if not dosage_input:
        messagebox.showinfo(title="Missing input", message="Please enter the dosage")
        return
    
    if not time_input:
        messagebox.showinfo(title="Missing input", message="Please enter the time to take the medication")
        return


    med_norm = med_input.casefold()

    #duplicate check
    is_duplicate = any(med.get("name", "").strip().casefold() == med_norm
                       for med in user_medications)
    
    if is_duplicate:
        messagebox.showinfo(title="Duplicate Entry", message=f"{med_input} is already in your medications!")
        return

    #add medication to the list
    new_med = ( {
        "name": med_input,
        "dosage": dosage_input,
        "time": time_input,
        "symptoms": symptoms_input
    })
    user_medications.append(new_med)
    users[current_user]["medications"] = user_medications

    #refresh listbox
    updateMedListbox()

    #clear entries
    medicationEntry.delete(0, tk.END)
    dosageEntry.delete(0, tk.END)
    timeEntry.delete(0, tk.END)
    symptomsEntry.delete(0, tk.END)

    #confirmation message
    messagebox.showinfo(title = "Medication Added", message = f"{med_input} is added to your medications!")
    print(f"[DEBUG] Current medications for {current_user}: {users[current_user]['medications']}")

#function to remove selected medication from listbox and user data
def onMedSelect(event):
    selection = medListbox.curselection()

    if selection and selection[0] != 0:
        removeMedButton.place(x=350, y=390, width=200, height=30)
    else:
        removeMedButton.place_forget()
    selection = medListbox.curselection()

    medListbox.bind('<<ListboxSelect>>', onMedSelect)


#function to confirm and remove medication
def confirmRemoveMedication():
    global current_user

    selection = medListbox.curselection()

    if not selection or selection[0] == 0:
        return
    
    med_index = selection[0] - 1
    med_name = users[current_user]["medications"][med_index]["name"]

    answer = messagebox.askyesno(title="Confirm Removal", message=f"Are you sure you want to remove {med_name}?")
    if answer:
        users[current_user]["medications"].pop(med_index)
        updateMedListbox()
        removeMedButton.place_forget()


def updateMedListbox():
    global current_user
    medListbox.delete(0, tk.END)

    medListbox.insert(tk.END, "Name | Dose | Time | Symptoms")
    medListbox.itemconfig(0, {'fg': 'white', 'bg': 'black'}) 

    user_medications = users[current_user].get("medications", [])
    for med in user_medications:
        #if symptoms is empty, display "None"
        symptoms_display = med.get("symptoms", "").strip() or "None"
        line = f"{med['name']} | {med['dosage']} | {med['time']} | {symptoms_display}"
        medListbox.insert(tk.END, line)


        
#widgets main login window
userLabel = tk.Label(mainWindow, text = "Username", bg = "#F5D5F7", font = font1)
passLabel = tk.Label(mainWindow, text = "Password", bg = "#F5D5F7", font = font1)
userEntry = tk.Entry(mainWindow)
passEntry = tk.Entry(mainWindow, show = "*")
loginButton = tk.Button(mainWindow, text = "Login", bg = "#F5D5F7", font = font1, command = login)
signUpButton = tk.Button(mainWindow, text = "Sign up", bg = "#F5D5F7", font = font1, command = signUp)

#widgets create user window
signUserEntryL = tk.Label(signIn, text = "Enter Username", bg = "#F5D5F7", font = font1)
signPassEntryL = tk.Label(signIn, text = "Enter Password", bg = "#F5D5F7", font = font1)
passRentryL = tk.Label(signIn, text = "Confirm Password", bg = "#F5D5F7", font = font1)
signUserEntry = tk.Entry(signIn)
signPassEntry = tk.Entry(signIn, show = "*")
passRentry = tk.Entry(signIn,show = "*")
createUserButton = tk.Button(signIn, text = "Create User", bg = "#F5D5F7", font = font1, command = createUser)
backButton = tk.Button(signIn, text="Go Back", bg="#F5D5F7", font=font1, command=lambda: [signIn.withdraw(), mainWindow.deiconify()])


#Widgets dashboard:

#Add Medication Button and Entries
addMedButton = tk.Button(dashboard, text="Add New Medication", bg="#F5D5F7", font=font1, command=addMedication)
medicationEntry = tk.Entry(dashboard)
medicationEntryL = tk.Label(dashboard, text = "Input Medications", bg = "#F5D5F7", font = font1)
dosageEntry = tk.Entry(dashboard)
dosageEntryL = tk.Label(dashboard, text = "Dosage", bg = "#F5D5F7", font = font1)
timeEntry = tk.Entry(dashboard)
timeEntryL = tk.Label(dashboard, text = "Take at", bg = "#F5D5F7", font = font1)
symptomsEntry = tk.Entry(dashboard)
symptomsEntryL = tk.Label(dashboard, text = "Symptoms", bg = "#F5D5F7", font = font1)

#Listbox and Scrollbar for medications
medListbox = tk.Listbox(dashboard, font=font1)
scrollbar = tk.Scrollbar(dashboard, orient=tk.VERTICAL)

medListbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=medListbox.yview)

#remove medication button appears when a medication is selected
removeMedButton = tk.Button(dashboard, text="Remove Selected Medication", font=font1, bg="#F5D5F7", command=confirmRemoveMedication)
removeMedButton.place(x=350, y=390, width=200, height=30)
removeMedButton.place_forget()


'''TODO: Implement history window and its button
historyButton = tk.Button(dashboard, text="View Medication History", bg="#F5D5F7", font=font1, command=lambda: [dashboard.withdraw(), historyWindow.deiconify()])'''


#positions for labels and buttons

#login
loginButton.place(x = 125, y = 100)
signUpButton.place(x = 125, y = 250)
userLabel.place(x=50, y=150)
userEntry.place(x=130 , y=150)
passLabel.place(x=50, y=190)
passEntry.place(x=130, y= 190)
#create
signUserEntry.place(x=195, y= 150)
signPassEntry.place(x=195, y= 190)
passRentry.place(x=195,y=230)
signUserEntryL.place(x=30, y=150) 
signPassEntryL.place(x=30, y=190)
passRentryL.place(x=30, y=230)
createUserButton.place(x = 130, y= 300)
backButton.place(x=130, y=350)
#dashboard
medicationEntryL.place(x=20, y=30)
medicationEntry.place(x=150, y=30, width=140)

dosageEntryL.place(x=20, y=80)
dosageEntry.place(x=150, y=80, width=140)

timeEntryL.place(x=20, y=130)
timeEntry.place(x=150, y=130, width=140)

symptomsEntryL.place(x=20, y=180)
symptomsEntry.place(x=150, y=180, width=140)

addMedButton.place(x=20, y=230, width=260, height=30)

medListbox.place(x=350, y=30, width=400, height=350)
scrollbar.place(x=750, y=30, width=20, height=350)

'''TODO: Implement history window layout'''

def onMedSelect(event):
    selection = medListbox.curselection()

    if selection and selection[0] != 0:
        removeMedButton.place(x=350, y=390, width=200, height=30)
    else:
        removeMedButton.place_forget()
    selection = medListbox.curselection()

medListbox.bind('<<ListboxSelect>>', onMedSelect)

def confirmRemoveMedication():
    global current_user

    selection = medListbox.curselection()

    if not selection or selection[0] == 0:
        return
    
    med_index = selection[0] - 1
    med_name = users[current_user]["medications"][med_index]["name"]

    answer = messagebox.askyesno(title="Confirm Removal", message=f"Are you sure you want to remove {med_name}?")
    if answer:
        users[current_user]["medications"].pop(med_index)
        updateMedListbox()
        removeMedButton.place_forget()

    
mainWindow.mainloop()
