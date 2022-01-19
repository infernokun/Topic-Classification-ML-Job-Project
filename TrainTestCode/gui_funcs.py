import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
import main_test as m
import os

# opens dialog box to select file and set the path


def openFile(t, path):

    # get directory of the application
    currdir = os.getcwd()

    # open dialog to find file path
    fn = tk.filedialog.askopenfilename(
        initialdir=currdir,
        title=t,
        filetypes=(("CSV files", "*.csv*"), ("all files", "*.*")))

    path.config(text=fn)

# opens dialog box to select the output file location path


def saveFile(t, path):

    # get directory of the application
    currdir = os.getcwd()

    # open dialog to save file path
    fn = tk.filedialog.asksaveasfilename(
        initialdir=currdir,
        title=t,
        filetypes=(("CSV files", "*.csv*"), ("all files", "*.*")))

    # append .csv at the end
    fn = fn + ".csv"

    path.config(text=fn)

# adds the new data to the copied file


def modifyNewFile(predictions, uncodedData, p3, codedData):

    f = open("{}".format(p3), "a")

    uncodedDataElements = uncodedData['data']
    uncodedDataPositions = uncodedData['positions']
    codedDataPositions = codedData['positions']

    # for all uncoded data
    for i in range(len(uncodedDataElements)):
        firstList = uncodedDataElements[i]
        firstList[len(firstList)-1] = predictions[i]
        count = 0

        # all labels in the coded data csv
        for j in codedDataPositions:
            # all the labels in the uncoded data csv
            for k in uncodedDataPositions:
                # if the label is in the uncoded data, then write it in that position
                if str(j) in list(uncodedDataPositions.keys()):
                    if count < len(firstList):
                        f.write("\"{}\",".format(firstList[count]))
                    count = count + 1
                    break
                else:
                    # write an empty space if not
                    f.write("\"\",")
                    break
        f.write(",\n")
    print("done")
    f.write("\n")
    f.close()

# handles GUI stuff


def windowHandler(root):

    root.title("Topic Classifier")
    width = 600
    height = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height,
                                (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    # top instruction label
    instructions = tk.Label(root)
    instructions["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=18)
    instructions["font"] = ft
    instructions["fg"] = "#333333"
    instructions["justify"] = "center"
    instructions["text"] = "CSV File Selection"
    instructions.place(x=160, y=10, width=290, height=30)

    # coded data path
    path1 = tk.Label(root)
    path1["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=10)
    path1["font"] = ft
    path1["fg"] = "#333333"
    path1["justify"] = "center"
    path1["text"] = "path1"
    path1.place(x=-205, y=60, width=1000, height=30)

    # change file button for coded data
    button1 = tk.Button(root)
    button1["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    button1["font"] = ft
    button1["fg"] = "#000000"
    button1["justify"] = "center"
    button1["text"] = "Browse Training Set"
    button1.place(x=230, y=100, width=130, height=30)
    button1["command"] = lambda: openFile("Select Training Set", path1)

    # uncoded data path
    path2 = tk.Label(root)
    path2["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=10)
    path2["font"] = ft
    path2["fg"] = "#333333"
    path2["justify"] = "center"
    path2["text"] = "path2"
    path2.place(x=-205, y=180, width=1000, height=30)

    # change file button for uncoded data
    button2 = tk.Button(root)
    button2["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    button2["font"] = ft
    button2["fg"] = "#000000"
    button2["justify"] = "center"
    button2["text"] = "Browse Uncoded Set"
    button2.place(x=230, y=230, width=130, height=30)
    button2["command"] = lambda: openFile("Select Uncoded Set", path2)

    # output file location
    path3 = tk.Label(root)
    path3["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=10)
    path3["font"] = ft
    path3["fg"] = "#333333"
    path3["justify"] = "center"
    path3["text"] = "{}\\output.csv".format(os.getcwd())
    path3.place(x=-205, y=290, width=1000, height=30)

    # change output file location
    button3 = tk.Button(root)
    button3["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    button3["font"] = ft
    button3["fg"] = "#000000"
    button3["justify"] = "center"
    button3["text"] = "Output file name"
    button3.place(x=230, y=330, width=130, height=30)
    button3["command"] = lambda: saveFile("Save Output File", path3)

    # status label
    status = tk.Label(root)
    status["anchor"] = "center"
    ft = tkFont.Font(family='Times', size=30)
    status["font"] = ft
    status["fg"] = "#333333"
    status["justify"] = "center"
    status["text"] = "Status"
    status.place(x=245, y=450, width=100, height=30)

    # run application button
    runButton = tk.Button(root)
    runButton["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    runButton["font"] = ft
    runButton["fg"] = "#000000"
    runButton["justify"] = "center"
    runButton["text"] = "Run"
    runButton.place(x=260, y=400, width=70, height=30)
    runButton["command"] = lambda: m.runApplication(
        path1, path2, path3, status)

    root.mainloop()
