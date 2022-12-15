import customtkinter
from customtkinter import filedialog
from tkinter import *
from tkinter import ttk

import os.path, sys
from PyPDF2 import PdfReader
import logging


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
logging.basicConfig(filename="logs.txt", level=logging.INFO, format='%(asctime)s: %(message)s')

def restart_program():
    root.destroy()
    os.startfile("pdf_value_finder_gui.pyw")


def startWorking(folder_path, total_files):
    def start_file():
        curItem = file_searched_log.focus()
        if curItem == "":
            child_id = file_searched_log.get_children()[0]
            file_searched_log.focus(child_id)
            file_searched_log.selection_set(child_id)
        else:
            setting_location = file_searched_log.item(curItem)["values"]
            if setting_location[0] != "File Searched 0":
                location_fix = setting_location[2] + "/" + setting_location[0]
                location = str(location_fix).replace("/", "\\")
            else:
                location_fix = setting_location[2] + "/"
                location = str(location_fix).replace("/", "\\")
            os.startfile(location)

    def open_files():
        file_searched_log.delete(*file_searched_log.get_children())
        remaining_pdf_files.configure(text="Remaining Files: " + str(total_files))
        if str(open_files_var.get()) == "on":
            warning.place(x=145, y=170)
        else:
            warning.place_forget()

    def multiple_values():
        file_searched_log.delete(*file_searched_log.get_children())
        remaining_pdf_files.configure(text="Remaining Files: " + str(total_files))
        if str(multiple_values_var.get()) == "on":
            multiple_values_guide.place(x=180, y=220)
        else:
            multiple_values_guide.place_forget()

    def search():
        file_searched_log.configure(selectmode="none")
        search_button.configure(state="disabled")
        search_value.configure(state="disabled")
        open_file_checkbox.configure(state="disabled")
        multiple_values_checkbox.configure(state="disabled")
        if len(search_value.get()) < 1:
            search_button.configure(state="normal")
            search_value.configure(state="normal")
            open_file_checkbox.configure(state="normal")
            multiple_values_checkbox.configure(state="normal")
        else:
            root.unbind('<Return>')
            root.unbind('<Escape>')
            file_searched_log.delete(*file_searched_log.get_children())
            value_find = False
            all_pages = 0
            remaining_files = int(total_files)
            found_values = []
            count = 0
            pdf_file_count = 0
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for filename in [f for f in filenames if f.endswith(".pdf") or f.endswith(".PDF")]:
                    pdf_file_count += 1
                    status = "Not Found"
                    pdf_file = os.path.join(dirpath, filename)
                    count += 1
                    try:
                        reader = PdfReader(pdf_file)
                        pages = reader.numPages
                        extracted_text = ""
                        total_pages = 0
                        for i in range(pages):
                            total_pages += 1
                            all_pages += 1
                            page = reader.getPage(i)
                            extracted_text += str(page.extract_text())
                            try:
                                for annot in reader.getPage(i)['/Annots']:
                                    extracted_text += annot.getObject()['/Contents']
                            except:
                                # there are no annotations on this page
                                pass
                        search_text = search_value.get()
                        remaining_files -= 1
                        remaining_pdf_files.configure(text="Remaining Files: " + str(remaining_files))
                        calculate_progress = int((pdf_file_count / int(total_files)) * 100)
                        progress_bar.set(calculate_progress / 100)
                        root.update()
                        if str(multiple_values_var.get()) == "on":
                            multi_values_search = search_text.split(", ")
                            multi_values_search = [x for x in multi_values_search if x] #Remvoe empty strings
                            if len(multi_values_search) > 1:
                                for word in multi_values_search:
                                    count += 1
                                    if word in extracted_text:
                                        if str(open_files_var.get()) == "on":
                                            os.startfile(pdf_file)
                                        value_find = True
                                        status = word + " Found"
                                        file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                                 values=(
                                                                     str(filename), str(total_pages), str(dirpath),
                                                                     status), tags=('found',))
                                        file_searched_log.yview_moveto(1)
                                        root.update()
                                        found_tupple = (str(filename), str(total_pages), str(dirpath), status)
                                        found_values.append(found_tupple)
                                    else:
                                        file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                                 values=(
                                                                     str(filename), str(total_pages), str(dirpath),
                                                                     status))
                                        file_searched_log.yview_moveto(1)
                                        root.update()
                                        pass
                            else:
                                if search_text in extracted_text:
                                    if str(open_files_var.get()) == "on":
                                        os.startfile(pdf_file)
                                    value_find = True
                                    status = str(search_text) + " Found"
                                    file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                           values=(
                                                               str(filename), str(total_pages), str(dirpath),
                                                               status), tags=('found',))
                                    file_searched_log.yview_moveto(1)
                                    root.update()
                                    found_tupple = (str(filename), str(total_pages), str(dirpath), status)
                                    found_values.append(found_tupple)
                                else:
                                    file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                           values=(
                                                           str(filename), str(total_pages), str(dirpath),
                                                           status))
                                    file_searched_log.yview_moveto(1)
                                    root.update()
                                    pass
                        else:
                            if search_text in extracted_text:
                                if str(open_files_var.get()) == "on":
                                    os.startfile(pdf_file)
                                value_find = True
                                status = search_text + " Found"
                                file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                         values=(
                                                             str(filename), str(total_pages), str(dirpath),
                                                             status), tags=('found',))
                                file_searched_log.yview_moveto(1)
                                root.update()
                                found_tupple = (str(filename), str(total_pages), str(dirpath), status)
                                found_values.append(found_tupple)
                            else:
                                file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                         values=(
                                                             str(filename), str(total_pages), str(dirpath),
                                                             status))
                                file_searched_log.yview_moveto(1)
                                root.update()
                                pass
                    except Exception as e:
                        file_searched_log.insert(parent="", index='end', iid=count, text=count + 1,
                                                 values=(
                                                     str(filename), str(total_pages), str(dirpath),
                                                     "File Corrupt / Locked"), tags=('not_found',))
                        corrupt_file_tupple = (str(filename), str(total_pages), str(dirpath), "File Corrupt / Locked")
                        found_values.append(corrupt_file_tupple)
            else:
                file_searched_log.configure(selectmode="browse")
                search_button.configure(state="normal")
                search_value.configure(state="normal")
                open_file_checkbox.configure(state="normal")
                multiple_values_checkbox.configure(state="normal")
                root.bind('<Return>', lambda event: search())
                # root.bind('<Escape>', lambda event: restart_program())
                if str(open_files_var.get()) == "off":
                    open_file_button.pack(pady=10)
                else:
                    open_file_button.pack_forget()
                if value_find is False:
                    count = 0
                    file_searched_log.delete(*file_searched_log.get_children())
                    if str(multiple_values_var.get()) == "on":
                        multi_values_search = search_text.split(", ")
                        multi_values_search = [x for x in multi_values_search if x]
                        if len(multi_values_search) > 1:
                            for i in multi_values_search:
                                found_tupple = ("File Searched " + str(total_files), str(all_pages), str(folder_path),
                                                str(i) + " Not Found")
                                found_values.append(found_tupple)
                        else:
                            found_tupple = ("File Searched " + str(total_files), str(all_pages), str(folder_path),
                                            str(search_text) + " Not Found")
                            found_values.append(found_tupple)
                    else:
                        file_searched_log.insert(parent="", index='end', iid=count, text=0,
                                                 values=(
                                                     "File Searched " + str(count), str(all_pages), str(folder_path), search_text + " Not Found"), tags=('not_found',))
                    for values in found_values:
                        count += 1
                        if str(values[3]) == "File Corrupt / Locked":
                            file_searched_log.insert(parent="", index='end', iid=count, text=count,
                                                     values=(
                                                         str(values[0]), str(values[1]), str(values[2]),
                                                         str(values[3])), tags=('not_found',))
                        else:
                            file_searched_log.insert(parent="", index='end', iid=count, text=count,
                                                     values=(
                                                         str(values[0]), str(values[1]), str(values[2]),
                                                         str(values[3])), tags=('not_found'))
                else:
                    count = 0
                    file_searched_log.delete(*file_searched_log.get_children())
                    if str(multiple_values_var.get()) == "on":
                        multi_values_search = search_text.split(", ")
                        multi_values_search = [x for x in multi_values_search if x]
                        value_not_found = []
                        temp = []
                        for i in found_values:
                            if str(i[3].split(" Found")[0]) not in temp:
                                temp.append(str(i[3].split(" Found")[0]))
                        if len(multi_values_search) > 1:
                            for i in multi_values_search:
                                if i in temp:
                                    pass
                                else:
                                    if i not in value_not_found:
                                        value_not_found.append(i)

                        if len(value_not_found) > 0:
                            for i in value_not_found:
                                found_tupple = ("File Searched " + str(total_files), str(all_pages), str(folder_path), str(i) + " Not Found")
                                found_values.append(found_tupple)

                    for values in found_values:
                        count += 1
                        if str(values[3]) == "File Corrupt / Locked":
                            file_searched_log.insert(parent="", index='end', iid=count, text=count,
                                                     values=(
                                                         str(values[0]), str(values[1]), str(values[2]),
                                                         str(values[3])), tags=('not_found',))
                        elif str(values[3]).__contains__("Not Found"):
                            file_searched_log.insert(parent="", index='end', iid=count, text=count,
                                                     values=(
                                                         str(values[0]), str(values[1]), str(values[2]),
                                                         str(values[3])))
                        else:
                            file_searched_log.insert(parent="", index='end', iid=count, text=count,
                                                     values=(
                                                         str(values[0]), str(values[1]), str(values[2]),
                                                         str(values[3])), tags=('found'))



    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("820x750")

    open_files_var = customtkinter.StringVar(value="on")
    multiple_values_var = customtkinter.StringVar(value="on")

    frame2 = customtkinter.CTkFrame(master=root)
    frame2.pack(pady=10, padx=10, fill="both", expand=True)

    stored_location_label = customtkinter.CTkLabel(master=frame2, text="Folder Selected", font=("Roboto", 24))
    stored_location_label.pack(pady=0, padx=10)

    stored_location = customtkinter.CTkLabel(master=frame2, text=str(folder_path), font=("Roboto", 12))
    stored_location.pack(pady=0, padx=10)

    line_space = customtkinter.CTkLabel(master=frame2, text="", font=("Roboto", 12))
    line_space.pack(pady=0, padx=10)

    total_pdf_files = customtkinter.CTkLabel(master=frame2, text="Total PDF Files: " + '{:,}'.format(total_files), font=("Roboto", 18))
    total_pdf_files.place(x=60, y=65)

    remaining_pdf_files = customtkinter.CTkLabel(master=frame2, text="Remaining Files: " + '{:,}'.format(total_files),
                                             font=("Roboto", 18))
    remaining_pdf_files.place(x=560, y=65)

    search_value = customtkinter.CTkEntry(master=frame2, placeholder_text="Enter Value", width=400, font=("Roboto", 18))
    search_value.place(x=120, y=110)

    search_button = customtkinter.CTkButton(master=frame2, text="Search", command=search)
    search_button.place(x=550, y=110)
    root.bind('<Return>', lambda event: search())
    # root.bind('<Escape>', lambda event: restart_program())

    open_file_checkbox = customtkinter.CTkSwitch(master=frame2, text="Open File If Found", command=open_files,
                                   variable=open_files_var, onvalue="on", offvalue="off")
    open_file_checkbox.deselect()
    open_file_checkbox.place(x=280, y=150)

    warning = customtkinter.CTkLabel(master=frame2, text="!!! WARNING !!! If value present in all files it will start opening All " + str(total_files) +" files !!! Be Careful !!!", text_color="red", font=("Roboto", 12, "italic"))
    warning.place_forget()

    multiple_values_checkbox = customtkinter.CTkSwitch(master=frame2, text="Multiple Values", command=multiple_values,
                                                 variable=multiple_values_var, onvalue="on", offvalue="off")
    multiple_values_checkbox.deselect()
    multiple_values_checkbox.place(x=280, y=200)

    multiple_values_guide = customtkinter.CTkLabel(master=frame2,
                                     text="Enter Values Separated with comma + space (e.g: 12345, 45678, 34356)", text_color="green",
                                     font=("Roboto", 12))
    multiple_values_guide.place_forget()

    progress_bar = customtkinter.CTkProgressBar(root, width=800, height=18, mode='determinate', corner_radius=5)
    progress_bar.set(0)
    progress_bar.pack(pady=7)

    frame3 = customtkinter.CTkFrame(master=root)
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
        background="#2B2B2B",
        foreground="#7F7F7F",
        fieldbackground="#2B2B2B",
        rowheight=22,
    )
    style.configure('Treeview.Heading', background='black', foreground='#2FA572')
    style.map('Treeview', background=[('selected', 'light green')], foreground=[('selected', '#7F7F7F')])


    file_searched_log = ttk.Treeview(frame3, height=10, selectmode='none')
    # file_searched_log.tag_configure('found', foreground='blue', background="#7F7F7F")
    file_searched_log.tag_configure('found', foreground='white', background="#2FA572")
    file_searched_log.tag_configure('not_found', foreground='red', background="black")
    file_searched_log['columns'] = ("File Name", "Pages", "Location", "Status")
    file_searched_log.column("#0", minwidth=10, width=55)
    file_searched_log.column("File Name", width=200)
    file_searched_log.column("Pages", width=40)
    file_searched_log.column("Location", width=385)
    file_searched_log.column("Status", width=100)

    file_searched_log.heading("#0", text="S. No")
    file_searched_log.heading("File Name", text="File Name")
    file_searched_log.heading("Pages", text="Pages")
    file_searched_log.heading("Location", text="Location")
    file_searched_log.heading("Status", text="Status")

    file_searched_log.pack(side='left', fill='y')

    scrollbar = Scrollbar(frame3, orient="vertical", command=file_searched_log.yview)
    # scrollbar = customtkinter.CTkScrollbar(frame3, orientation="vertical", command=file_searched_log.yview)
    scrollbar.pack(side="right", fill="y")
    file_searched_log.configure(yscrollcommand=scrollbar.set)

    open_file_button = customtkinter.CTkButton(master=root, text="Open File", command=start_file)
    open_file_button.pack_forget()

def selectFolder():
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        file_address.configure(text="No Folder Selected", text_color="red")
    else:
        file_address.configure(text="Accessing Files...", text_color="white")
        root.update()
        total_pdf_files = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in [f for f in filenames if f.endswith(".pdf") or f.endswith(".PDF")]:
                total_pdf_files += 1
        startWorking(folder_path, total_pdf_files)


root = customtkinter.CTk()
root.title("PDF Value Finder")
root.geometry("500x200")
root.resizable(0,0)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="PDF Search Engine", font=("Roboto", 24))
label.pack(pady=12, padx=10)

file_address = customtkinter.CTkLabel(master=frame, text="")
file_address.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="Select Folder", command=selectFolder)
button.pack(pady=12, padx=10)

root.mainloop()