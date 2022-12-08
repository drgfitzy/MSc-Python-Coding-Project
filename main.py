import matplotlib
#matplotlib qt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from tkinter import *
from tkinter import ttk, filedialog
from tkinter import messagebox as mb
from json import JSONDecodeError


window = Tk()
window.geometry("1200x650")
window.title("Summative Assessment")
options = []


# function that allows user to select either a csv or json file format
def file_select():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a file",
                                          filetype=(("csv_files", "*.csv"), ("json_files", "*.json"),
                                                    ("All Files", "*.*")))
    file_label["text"] = filename

    options.insert(0, filename)

    if filename.endswith(".csv"):
        convert_button["state"] = NORMAL
        convert_menu.set(filename)
        file_label2["text"] = filename

    if filename.endswith(".json"):
        load_files_button["state"] = NORMAL
        # file = os.path.basename(filename)  # TODO


# Function to clear Table Data table
def clear_data():
    table.delete(*table.get_children())


# Function to clear Stats Data table
def clear_stats_table_data():
    stats_table.delete(*stats_table.get_children())


# Function to clear Merge Data table
def clear_merge_table_data():
    merge_table.delete(*merge_table.get_children())


# Function to add file directories to combobox list
def combobox_update():
    convert_menu["values"] = options
    return None


# Function to add combobox selection to file_label 2
def csv_selected(event):
    global filename
    file_label2.configure(text=convert_clicked.get())


# Function to add to lists for violations and inspection comboboxes in Merge Data
def clean_combobox_update():
    merge_menu_first["values"] = file_options
    merge_menu_second["values"] = file_options2


# Passes violation file directory to label
def json_selected(event):
    violation_file_label.configure(text=merge_clicked_first.get())


# Passes inspection file directory to label
def json_selected2(event):
    inspection_file_label.configure(text=merge_clicked_second.get())


# Activates buttons post JSON conversion or loading
def activate_buttons():
    clean_button["state"] = NORMAL
    graph_data_button["state"] = NORMAL
    merge_button["state"] = NORMAL
    stats_button["state"] = NORMAL


# Converts CSV to JSON and saves to same directory, also uploads dataset to Data Table
def json_conversion():  # TODO
    global df2, file_path
    file_path = file_label2["text"]
    try:
        csv_filename = r"{}".format(file_path)
        df = pd.read_csv(csv_filename)
        file = os.path.basename(f"{csv_filename}.json")
        df.to_json(file)
        df.to_json(f"{file_path}.json")
        df2 = pd.read_json(f"{file_path}.json")
        file_options.insert(0, f"{file_path}.json")
        file_options2.insert(0, f"{file_path}.json")
        clear_data()
        tabulate_treeview(df2, table)
        mb.showinfo("Success",
                    f"json file for {file} successfully created in directory and uploaded to Table Data window")
        activate_buttons()
        return df2
    except FileNotFoundError:
        mb.showerror("Information", "No file selected. Please upload a csv file")


# inserts each list into a ttk treeview.
def tabulate_treeview(dataframe, treeview):
    treeview["column"] = list(dataframe.columns)
    treeview["show"] = "headings"
    for column in treeview["columns"]:
        treeview.heading(column, text=column)  # let the column heading = column name
    df_rows = dataframe.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        treeview.insert("", "end", values=row)


# loads converted json files into the table data window
def load_json_file():
    global df3
    global df2

    file_label["text"] = filename
    file = os.path.basename(filename)
    # file_path = os.path.basename(filename)

    if df2 is not None:
        try:
            with open(filename) as fp:
                df2 = pd.read_json(fp)
            file_options.insert(0, f"{filename}")
            file_options2.insert(0, f"{filename}")
            clear_data()
            tabulate_treeview(df2, table)

            mb.showinfo("Success", f"{os.path.basename(filename)} successfully loaded")
            activate_buttons()
            return df2
        except NameError:
            mb.showerror("Information", "Please ensure you have selected a .json file to load")
        except JSONDecodeError:
            mb.showerror("Information", "Please ensure you are loading a .json file")
        except FileNotFoundError:
            mb.showerror("Information", "Please ensure you have selected a .json file to load")
        except ValueError:
            mb.showerror("Information", "Please ensure you have selected a .json file to load")
        return df2
    elif df3 is not None:
        try:
            with open(filename) as fp:

                df3 = pd.read_json(fp)

            file_options.insert(0, f"{filename}")
            file_options2.insert(0, f"{filename}")
            clear_data()
            tabulate_treeview(df3, table)
            mb.showinfo("Success", f"{os.path.basename(filename)} successfully loaded")
            activate_buttons()
            return df3
        except NameError:
            mb.showerror("Information", "Please ensure you have selected a .json file to load")
        except JSONDecodeError:
            mb.showerror("Information", "Please ensure you are loading a .json file")
        except FileNotFoundError:
            mb.showerror("Information", "Please ensure you have selected a .json file to load")
        except ValueError:
            mb.showerror("Information", "Please ensure you have selected a .json file to load")
        return df3


# filters the raw data set to exclude the specified components and extract seating data into a new column
def filter_data():
    global df2, df3, file_path
    file_path = file_label["text"]

    if "INACTIVE" in df2.values and "PE DESCRIPTION" in df2.columns:
        clear_data()
        try:
            df3 = df2[df2["PROGRAM STATUS"] != "INACTIVE"]
            df3[['SEATS']] = df3["PE DESCRIPTION"].str.extract(
                "(\\(\d+-\d+\\)| \\(\d-\d,\d+ SF\\) | \\(\d+ \\+ \\)|\\(\d,\d+\\+ SF\\))",
                expand=True)
            tabulate_treeview(df3, table)
            mb.showinfo("Success", f"Data successfully cleaned and {os.path.basename(filename)}-clean.json file saved")
            df3.to_json(f"{file_path}-clean.json")
            file_options.insert(0, f"{file_path}-clean.json")
            file_options2.insert(0, f"{file_path}-clean.json")
            return df3

        except AttributeError:
            mb.showerror("Information", "Data has already been cleaned")
        except KeyError:
            mb.showerror("Information", "This file cannot be filtered")
        except FileNotFoundError:
            mb.showerror("Information", f"No such file found")
        return df3
    elif "PE DESCRIPTION" in df2.columns:
        clear_data()
        df3 = df2
        try:
            df3[['SEATS']] = df3["PE DESCRIPTION"].str.extract(
                "(\\(\d+-\d+\\)| \\(\d-\d,\d+ SF\\) | \\(\d+ \\+ \\)|\\(\d,\d+\\+ SF\\))",
                expand=True)
            tabulate_treeview(df3, table)
            mb.showinfo("Success", "Data successfully cleaned")
            df3.to_json(f"{file_path}-clean.json")
            file_options.insert(0, f"{file_path}-clean.json")
            file_options2.insert(0, f"{file_path}-clean.json")
            return df3
        except AttributeError:
            mb.showerror("Information", "Data has already been cleaned")
        except KeyError:
            mb.showerror("Information", "This file cannot be filtered")
            return None
        except FileNotFoundError:
            mb.showerror("Information", f"No such file found")
            return None
    else:
        mb.showinfo("Incompatible file", "Data not suitable for cleaning, please select a different file")


# groups the dataframes by different columns 
def group_dataframe(dataframe, string1, string2):
    global df4
    grouped_df = dataframe.groupby(string1)
    grouped_list = grouped_df.groups.keys()
    grouped_list_mean = grouped_df["SCORE"].mean()
    grouped_list_median = grouped_df["SCORE"].median()
    grouped_list_mode = grouped_df["SCORE"].apply(lambda x: x.mode().iloc[0])

    data = {string2: tuple(grouped_list), "Mean": grouped_list_mean,
            "Median": grouped_list_median, "Mode": grouped_list_mode}
    df4 = pd.DataFrame(data)
    return df4


# Displays Mena/Median/Mode data for Seating and Zip Codes for Inspections Dataset
def radio_clicked(value):
    # global file_path
    global filename, df3, df4
    file_label["text"] = filename
    clear_stats_table_data()

    if value == 1:
        try:
            if filename.endswith("-clean.json"):
                with open(filename) as fp:
                    df3 = pd.read_json(fp)
                    group_dataframe(df3, "SEATS", "Seats")
                    tabulate_treeview(df4, stats_table)
            else:
                group_dataframe(df3, "SEATS", "Seats")
                tabulate_treeview(df4, stats_table)

        except KeyError:
            mb.showerror("Incorrect file", "Please use cleaned inspections data")
        except AttributeError:
            mb.showerror("Incorrect file", "Please use cleaned inspections data")
        except NameError:
            mb.showerror("Information", "Please clean data before stats analysis")

    elif value == 2:
        try:
            if filename.endswith("-clean.json"):
                with open(filename) as fp:
                    df3 = pd.read_json(fp)
                    group_dataframe(df3, "Zip Codes", "Zip Codes")
                    tabulate_treeview(df4, stats_table)
            else:
                group_dataframe(df3, "Zip Codes", "Zip Codes")
                tabulate_treeview(df4, stats_table)
        except KeyError:
            mb.showerror("Incorrect file", "Please use cleaned inspections data")
        except AttributeError:
            mb.showerror("Incorrect file", "Please use cleaned inspections data")
        except NameError:
            mb.showerror("Information", "Please clean data before stats analysis")


# Converts violations data to a histogram
def graph_data():
    global df2
    global df3

    if "VIOLATION CODE" in df2.columns:
        try:
            grouped_df = df2.groupby("VIOLATION CODE")
            grouped_list = grouped_df.groups.keys()
            data = {"violation codes": grouped_list, "Number of establishments": grouped_df["VIOLATION CODE"].count()}
            df4_violations = pd.DataFrame(data)
            df4_violations.plot(kind="bar", x="violation codes", y="Number of establishments",
                                title="Number of violations by violation category")
            plt.show().figure("Violations Graph")
        except AttributeError:
            mb.showinfo("Information", "Graph loaded successfully")
    else:
        mb.showerror("information", "Please load the violations dataset")


# Merges violations and inspections dataset
def merge_data():
    global merged_df
    clear_merge_table_data()

    file_path_first = violation_file_label["text"]
    file_path_second = inspection_file_label["text"]
    try:
        with open(file_path_first) as first:
            data1 = json.load(first)
        df_merge1 = pd.DataFrame(data1)

        with open(file_path_second) as second:
            data2 = json.load(second)
        df_merge2 = pd.DataFrame(data2)

        grouped_df1 = df_merge1.groupby("SERIAL NUMBER")
        grouped_list = grouped_df1.groups.keys()
        new_data1 = {"Serial Number": tuple(grouped_list), "Number of violations": grouped_df1["SERIAL NUMBER"].count()}
        df_violations = pd.DataFrame(new_data1)
        grouped_df2 = df_merge2[["SERIAL NUMBER", "Zip Codes"]]
        new_data2 = {"Serial Number": grouped_df2["SERIAL NUMBER"], "Zip Codes": grouped_df2["Zip Codes"]}
        df_zip_codes = pd.DataFrame(new_data2)
        df_zip_codes_filtered = df_zip_codes[df_zip_codes["Zip Codes"] != "NaN"]
        merged_df = pd.merge(df_violations, df_zip_codes_filtered).dropna()

        tabulate_treeview(merged_df, merge_table)
        mb.showinfo("Success", "Data Merged Successfully")
        correlate_button["state"] = NORMAL
    except KeyError:
        mb.showerror("Information", "Please ensure the correct files are selected for data merge")
    except FileNotFoundError():
        mb.showerror("File Error", "Please ensure you select both files for merge")


# Pop up window displaying corrlation data from merged dataset
def popup_corr_window():
    global merged_df
    popup = Toplevel()
    popup.title("Correlation Data")
    popup_table_frame = Frame(popup, height=300, width=400, bg="white")
    popup_table_frame.pack_propagate(False)
    popup_table_frame.pack(side=LEFT, padx=10, )
    popup_table = ttk.Treeview(popup_table_frame, height=10, selectmode="extended")
    popup_table.pack()
    popup_label = Label(popup)
    popup_label.place(x=100, y=200)
    correlation_data = merged_df.corr()
    tabulate_treeview(correlation_data, popup_table)

    if correlation_data.lt(0).any().any():
        popup_label["text"] = "There is no correlation observed"
    else:
        popup_label["text"] = "Correlation observed"


##################GUI########################

# GUI interface grouped into 4 areas for flow and ease of use
group1 = LabelFrame(window, height=120, width=350, text="1. Select File").grid(row=0, column=0, padx=20, pady=15)
group2 = LabelFrame(window, height=280, width=350, text="2. Data conversion/upload")
group2.place(x=20, y=150)
group3 = LabelFrame(window, height=195, width=350, text="3. Data clean")
group3.place(x=20, y=445)
group4 = LabelFrame(window, height=625, width=780, text="4. Data visuals")
group4.place(x=400, y=15)

# upload button and label in group 1
upload_button = Button(group1, text="Select File", height=1, width=15,
                       command=lambda: file_select())
upload_button.place(x=245, y=100)

# convert button and label in group 2
convert_label = Label(group2, text="From menu, select a csv file to convert to .json").place(x=10, y=20)
convert_button = Button(group2, text="Convert CSV", height=1, width=15, state=DISABLED,
                        command=lambda: json_conversion())
convert_button.place(x=215, y=57)

or_label = Label(group2, text="---------------------------or-------------------------------").place(x=20, y=120)

# load json files button and label in group 2
load_label = Label(group2, text="Load a selected .json file into Table Data window").place(x=10, y=170)
load_files_button = Button(group2, text="Load JSON", height=1, width=15, state=DISABLED,
                           command=lambda: load_json_file())
load_files_button.place(x=215, y=220)

# Combobox to store file directories of those files selected by the user
convert_clicked = StringVar()
convert_menu = ttk.Combobox(window, values=options, postcommand=combobox_update, textvariable=convert_clicked, width=25)
convert_menu.place(x=35, y=225)
convert_menu.set("Select file")
convert_menu.bind("<<ComboboxSelected>>", csv_selected)

# clean button and label in group 3
clean_label = Label(group3, text="Clean Inspection.json or Inventory.json file:").place(x=20, y=10)
clean_button = Button(group3, text="Clean Data", height=1, width=15, state=DISABLED, command=lambda: filter_data())
clean_button.place(x=215, y=40)
or_label2 = Label(group3, text="---------------------------or-------------------------------").place(x=20, y=70)

# graph violations button and label in group 3
graph_label = Label(group3, text="Graph violations.json data").place(x=20, y=100)
graph_data_button = Button(group3, text="Graph Violations", height=1, width=15, state=DISABLED,
                           command=lambda: graph_data())
graph_data_button.place(x=215, y=130)

# Data visuals tabs for either graph or table in group 4 -tab control
tab_control = ttk.Notebook(window)
tab_control.place(x=425, y=50)
tab1 = ttk.Frame(tab_control, width=520, height=500)
tab3 = ttk.Frame(tab_control, width=520, height=500)
tab4 = ttk.Frame(tab_control, width=520, height=500)
tab1.pack(fill="both", expand=1)
tab3.pack(fill="both", expand=1)
tab4.pack(fill="both", expand=1)

tab_control.add(tab1, text="Table Data")
tab_control.add(tab3, text="Stats Data")
tab_control.add(tab4, text="Merge Data")

# Data visuals save and load data buttons in group 4
file_label = Label(group1, text="No file selected. Please upload a csv or json file", wraplength=300, justify=LEFT)
file_label.place(x=25, y=40)

# file label for json conversions
file_label2 = Label(tab1, text="No file selected")
file_label2.place(x=10, y=10)

#  Table Data tab
table_frame = Frame(tab1, height=470, width=700, bg="white")
table_frame.pack_propagate(False)
table_frame.pack(side=LEFT, padx=10, )
table = ttk.Treeview(table_frame, height=21, selectmode="extended")
table.pack()

# Merge Data tab
group5 = LabelFrame(tab4, height=225, width=170, text="Violation File").place(x=2, y=22)
group6 = LabelFrame(tab4, height=225, width=170, text="Inspection File").place(x=2, y=250)
merge_table_frame = Frame(tab4, height=475, width=545, bg="white")
merge_table_frame.pack_propagate(False)
merge_table_frame.pack(side=RIGHT, padx=10, pady=27)
merge_table = ttk.Treeview(merge_table_frame, height=20, selectmode="extended")
merge_table.pack()
file_options = []
file_options2 = []
file1_merge_label = Label(tab4, text="Select Violations file:")
file1_merge_label.place(x=5, y=50)
file2_merge_label = Label(tab4, text="Select Inspections file:")
file2_merge_label.place(x=5, y=290)
violation_file_label = Label(tab4, text="No file selected", wraplength=150, justify=LEFT)
violation_file_label.place(x=5, y=125)
inspection_file_label = Label(tab4, text="No file selected", wraplength=150, justify=LEFT)
inspection_file_label.place(x=5, y=370)
instruction_label = Label(tab4,
                          text="Please convert both inspection and violations files to .json then select each from the dropdown menus below")
instruction_label.place(x=100, y=5)
merge_clicked_first = StringVar()
merge_clicked_second = StringVar()

# clean_clicked.set("JSON")
merge_menu_first = ttk.Combobox(tab4, value=file_options, postcommand=clean_combobox_update,
                                textvariable=merge_clicked_first)
merge_menu_first.place(x=20, y=90)
merge_menu_first.set("Select file")
merge_menu_first.bind("<<ComboboxSelected>>", json_selected)
merge_menu_second = ttk.Combobox(tab4, value=file_options2, postcommand=clean_combobox_update,
                                 textvariable=merge_clicked_second)
merge_menu_second.place(x=20, y=330)
merge_menu_second.set("Select file")
merge_menu_second.bind("<<ComboboxSelected>>", json_selected2)

merge_button = Button(tab4, text="Merge Data", state=DISABLED, command=lambda: merge_data())
merge_button.place(x=5, y=490)
correlate_button = Button(tab4, text="Correlate Data", state=DISABLED, command=lambda: popup_corr_window())
correlate_button.place(x=85, y=490)

# vertical scroll bar for merge table
merge_table_scroll_bar_vert = Scrollbar(merge_table_frame)
merge_table_scroll_bar_vert.pack(side=RIGHT, fill=Y)
merge_table_scroll_bar_vert.config(command=merge_table.yview)

# hotizontal scroll bar for merge table
merge_table_scroll_bar_horiz = Scrollbar(merge_table_frame, orient=HORIZONTAL)
merge_table_scroll_bar_horiz.pack(side=BOTTOM, fill=X)
merge_table_scroll_bar_horiz.config(command=merge_table.xview)

# verticle scroll bar for table tab
table_scroll_bar_vert = Scrollbar(tab1)
table_scroll_bar_vert.pack(side=RIGHT, fill=Y)
table_scroll_bar_vert.config(command=table.yview)

# hotizontal scroll bar for table tab
table_scroll_bar_horiz = Scrollbar(table_frame, orient=HORIZONTAL)
table_scroll_bar_horiz.pack(side=BOTTOM, fill=X)
table_scroll_bar_horiz.config(command=table.xview)

# verticle scroll bar for stats table
stats_scroll_bar_vert = Scrollbar(tab3)
stats_scroll_bar_vert.pack(side=RIGHT, fill=Y)
stats_scroll_bar_vert.config(command=table.yview)

# radio buttons for stats tab
r = IntVar()
r.set(1)
rad1 = Radiobutton(tab3, text="Seats", variable=r, value=1, command=lambda: radio_clicked(r.get(), ))
rad1.place(x=200, y=10)
rad2 = Radiobutton(tab3, text="ZipCode", variable=r, value=2, command=lambda: radio_clicked(r.get()))
rad2.place(x=300, y=10)

# Stats Data Tab components
stats_button = Button(tab3, text="Show Stats", height=1, width=15, state=DISABLED,
                      command=lambda: radio_clicked(r.get()))
stats_button.place(x=50, y=10)

stats_frame = Frame(tab3, height=450, width=700, bg="white")
stats_frame.pack_propagate(False)
stats_frame.pack(side=LEFT, padx=10)

stats_table = ttk.Treeview(stats_frame, height=20, selectmode="extended")
stats_table.pack()

# verticle scroll bar for stats table tab
stats_table_scroll_bar_vert = Scrollbar(stats_frame)
stats_table_scroll_bar_vert.pack(side=RIGHT, fill=Y)
stats_table_scroll_bar_vert.config(command=stats_table.yview)

# hotizontal scroll bar for table tab
stats_table_scroll_bar_horiz = Scrollbar(stats_frame, orient=HORIZONTAL)
stats_table_scroll_bar_horiz.pack(side=BOTTOM, fill=X)
stats_table_scroll_bar_horiz.config(command=stats_table.xview)

mainloop()