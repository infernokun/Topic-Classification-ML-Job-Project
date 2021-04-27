import tkinter as tk
from tkinter import filedialog
import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.metrics import classification_report, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm  
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
import tkinter.font as tkFont
from tkinter import messagebox
import shutil



# name of all topics
subjects = ["No Substantive Higher Education Information",
"Academics",
"Access",
"Accountability",
"Administration",
"Adult Education/Non-Traditional Students",
"Affordability",
"Athletics",
"Budgets/Resources",
"Community Engagement",
"Completion",
"Diversity/Equity",
"Economic Outcomes and Impacts",
"Enrollment",
"Facilities",
"Faculty and Staff Concerns",
"Goals/Master Plans",
"Graduate Education",
"Honors and Awards",
"International Students",
"Preparation and Remediation",
"Quality of Education",
"Research and Faculty Publications",
"Retention",
"Safety",
"Student Debt",
"Student Services",
"System-Level Matters",
"Technology",
"Transfer Students",
"Tuition"]

# generalizes the data to a vectorizable format and returns it
def generalizeUncodedData(uncodedData_data, uncodedData_titleText):
    
    data = []
    count = 0
    
    # for all the data rows
    for i in uncodedData_data:
        # grab a row
        row = uncodedData_data[count]
        
        # append the title in front of the text
        
        fullText = row[uncodedData_titleText[0]] + " " + row[uncodedData_titleText[1]]

        data.append(fullText)
        
        count = count + 1
    
    dataset = {}
    dataset['data'] = np.array(data)
    
    return dataset

# applies TfidfVectorizer to the sets of text
def applyML(codedData, uncodedData, status):
        
    vec = TfidfVectorizer(stop_words="english", decode_error="ignore", sublinear_tf=True)
    
    # train the dataset with the categorized data
    vec.fit(codedData['data'])
    
    # perform a generalization of the uncoded data
    uncodedData_g = generalizeUncodedData(uncodedData['data'], uncodedData['titleText'])
    
    # perform SVC to predict the uncoded data, returns the predictions
    predictions = vectorizerSVC(codedData['data'], codedData['answers'], uncodedData_g, vec)
    
    # update status text
    status["text"] = "Done"
    
    return predictions

# opens dialog box to select file and set the path
def openFile(t, path):
    # get directory of the application
    currdir = os.getcwd()
    
    # open dialog to find file path
    fn = tk.filedialog.askopenfilename(
        initialdir = currdir,
        title = t,
        filetypes = (("CSV files", "*.csv*"), ("all files", "*.*")))

    path.config(text=fn)
   
# opens dialog box to select the output file location path
def saveFile(t, path):
    # get directory of the application
    currdir = os.getcwd()
    
    # open dialog to save file path
    fn = tk.filedialog.asksaveasfilename(
        initialdir = currdir,
        title = t,
        filetypes = (("CSV files", "*.csv*"), ("all files", "*.*")))
    
    # append .csv at the end
    fn = fn + ".csv"
    print (fn)
    
    path.config(text=fn)

# handles GUI stuff
def windowHandler(root):
    root.title("Topic Classifier")
    width=600
    height=600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
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
    button1["command"] = lambda:openFile("Select Training Set", path1)
    
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
    button2["command"] = lambda:openFile("Select Uncoded Set", path2)
    
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
    button3["command"] = lambda:saveFile("Save Output File", path3)
    
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
    runButton["command"] = lambda:runApplication(path1, path2, path3, status)

    root.mainloop()
    
# run application when button is pressed
def runApplication(p1, p2, p3, status):
    # change status text
    status["text"] = "Running"
    
    # check files for correct format and file extension asnd returns the uncoded dataset and coded dataset
    dataSets = fileCheck(p1, p2, p3)
    
    codedData = dataSets[0]
    uncodedData = dataSets[1]
    
    # apply ML algorithm and return the predictions
    predictions = applyML(codedData, uncodedData, status)
    
    # modify file with new results
    modifyNewFile(predictions, uncodedData['data'], p3)

# adds the new data to the copied file
def modifyNewFile(predictions, uncodedData, p3):
    #p3_path = p3["text"]
    f = open("testthing2.csv", "a")
    print("opened")
    
    f.write("{},{},{},{},{},{},{},{},{},{},{},,\n".format("unit_id", "doc_number", "title", "year", "state", "page_count", "org_type", "figure", "unit_text", "unit_length", "topic"))
    
    for i in range(len(uncodedData)):
        # the row
        firstList = uncodedData[i]
        
        # the len of the row -1 is the topic
        firstList[len(firstList)-1] = predictions[i]
        
        for i in range(len(firstList)):
            if i == 8:
                f.write("\"{}\",".format(firstList[i].replace("\"", "")))
            else:
                f.write("\"{}\",".format(firstList[i]))
        f.write(",\n")
    print("done")
    f.write("\n")
    f.close()
    

# checks the file extension and label contents
def fileCheck(p1, p2, p3):
    # paths for the gui labels
    p1_path = p1["text"]
    p2_path = p2["text"]
    p3_path = p3["text"]
    
    # if file extentions are not .csv
    if (p1_path[len(p1_path)-4:len(p1_path)] != ".csv" or p2_path[len(p2_path)-4:len(p2_path)] != ".csv"):
        print("Must be .csv file!")
        messagebox.showerror('error', 'Make sure both files are CSV!')
    else:
        # throws error if the csv file is not in the supported format
        try:
            # puts data in lists
            codedData = getTrainingSet(p1_path)
            uncodedData = getUncodedData(p2_path)
            
            # make a copy of the original file to append the results
            original = p1_path
            target = p3_path
            shutil.copyfile(original, target)
            
            dataSets = []
            dataSets.append(codedData)
            dataSets.append(uncodedData)
            
            return dataSets
        except:
            messagebox.showerror('error', 'File not in the correct format')     

# converts CSV data from CODED DATA to list format, returns dataset
def getTrainingSet(filename):
    count = 0

    # creates a data list which is a list of the attribues
    # the answers list is the categorized answer
    data = []
    answers = []
    title = []

    print("You chose {}".format(filename))
    
    """ open Training set file
        2 - title of the element
        9 - text of the element
        11 - classified topic number of the element """
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            # not the first row which are the labels
            if count != 0:
                header = str(row[2]).lower()
                text = str(row[9]).lower()
                topic = int(row[11])
                
                title.append(header)
                
                # append the title in front of the text
                data.append(header + " " + text)
                
                answers.append(topic)

            count = count + 1

    dataset = {}
    
    dataset['title'] = np.array(title)
    dataset['data'] = list(data)
    dataset['answers'] = np.array(answers)
    dataset['target_subject'] = np.array(subjects)
    dataset['data_features'] = np.array(['title', 'text'])

    return dataset

# function to obtain uncoded data from csv
def getUncodedData(filename):
    count = 0

    # creates a data list which is a list of the attribues
    # the answers list is the categorized answer
    data = []
    titleText = []
    
    # init index for title and text position
    titleIdx = 0
    textIdx = 0

    print("You chose {}".format(filename))
    
    """ open Training set file
        2 - title of the element
        9 - text of the element
        11 - classified topic number of the element """
    # open the csv file
    with open(filename, errors='ignore') as file:
        reader = csv.reader(file)
        for row in reader:
            # a list for each row
            dataRow = []
            # case for row indicies not 0
            if count != 0:
                # each row contrains 10 elements
                for i in range(0, len(row)-1):
                    # append with space
                    if (str(row[i]) == ""):
                        dataRow.append(str(""))
                    else:
                        dataRow.append(str(row[i]))
            else:
                # case for 0 index
                count2 = 0
                for i in row:
                    # find the title index
                    if (str(i) == "title"):
                        titleIdx = count2
                        print(str(i), titleIdx)
                    # find the text index
                    elif (str(i) == "unit_text"):
                        textIdx = count2
                        print(str(i), textIdx)
                    count2 = count2 + 1
                titleText.append(titleIdx)
                titleText.append(textIdx)
                            
            # don't make list for first row
            if (len(dataRow) != 0):
                data.append(dataRow)
            count = count + 1

    dataset = {}
    
    # dataset for data and title / text indicies
    
    dataset['data'] = data
    dataset['titleText'] = titleText
    #dataset['answers'] = ""
    #dataset['data_features'] = np.array(['title', 'text'])

    return dataset
    
# performs SVC on the dataset
def vectorizerSVC(data, answers, uncodedData, vec):
    # SVC
    clf = LinearSVC(C=11)
    clf.fit(vec.transform(data), answers)
    y_pred = clf.predict(vec.transform(uncodedData['data']))
    
    print(y_pred)
    
    return y_pred

def vectorizerSVC2(X_train, X_test, y_train, y_test, vec):
    # SVC
    clf = LinearSVC(C=11)
    clf.fit(vec.transform(X_train), y_train)
    y_pred = clf.predict(vec.transform(X_test))
    print(y_pred)
    print(classification_report(y_test, y_pred))
                                                                       
# main function
if __name__ == '__main__':
    # start tkinter instance
    
    root = tk.Tk()
    windowHandler(root)
    root.withdraw()
    
    """
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()"""
    
    """below for display purposes"""
    
    filename = "C:\\Users\\sasuk\\Desktop\\Programming\\Python\\topic_classifier\\Original Files\\Coded Data.csv"
    
    filename2 = "C:\\Users\\sasuk\\Desktop\\Programming\\Python\\topic_classifier\\Original Files\\Uncoded Data-CA Legislation.csv"
    
    filename3 = "C:\\Users\\sasuk\\Desktop\\Programming\\Python\\topic_classifier\\Original Files\\Uncoded Data-CA Bureaucracy.csv"
    
    root = tk.Tk()
    
    """Legislation.csv"""
    path1 = tk.Label(root)
    path1["text"] = filename
    path2 = tk.Label(root)
    path2["text"] = filename2
    path3 = tk.Label(root)
    path3["text"] = "output.csv"
    
    dataDict1 = fileCheck(path1, path2, path3)
    uncodedDataDict = dataDict1[1]
    titleText1 = uncodedDataDict['titleText']
    data1 = uncodedDataDict['data']
    
    uncodedData_g1 = generalizeUncodedData(data1, titleText1)
    
    codedData = dataDict1[0]
    uncodedData = dataDict1[1]
    
    predictions1 = applyML(codedData, uncodedData, path3)
    
    labels, counts = np.unique(predictions1, return_counts=True)
    
    modifyNewFile(predictions1, uncodedData['data'], path3)
    
    
    """Bureaucracy.csv"""
    path2 = tk.Label(root)
    path2["text"] = filename3
    path3 = tk.Label(root)
    path3["text"] = "output2.csv"
    
    dataDict2 = fileCheck(path1, path2, path3)
    uncodedDataDict2 = dataDict2[1]
    test8 = uncodedDataDict2['titleText']
    data2 = uncodedDataDict2['data']
    
    test10 = generalizeUncodedData(data2, test8)
    
    codedData = dataDict2[0]
    uncodedData = dataDict2[1]
    
    predictions2 = applyML(codedData, uncodedData, path3)
    
    labels2, counts2 = np.unique(predictions2, return_counts=True)
    
    modifyNewFile(predictions2, uncodedData['data'], path3)
    
    
    """Testing stuff"""
    file_len = len(filename)

    if file_len > 0:
        if (filename[file_len-4:file_len] != ".csv"):
            print("Must be .csv file!")
        else:
            
            # gets full training set
            fulldata = getTrainingSet(filename)

            
            """
            labels = unique labels
            counts = total count of elements for label
            """
            
            labels, counts = np.unique(fulldata['answers'], return_counts=True)
            
            print(labels)
            print(counts)
            
            X_train, X_test, y_train, y_test = train_test_split(fulldata['data'], fulldata['answers'], test_size=0.2, random_state=1)
        
            vec = TfidfVectorizer(stop_words="english", decode_error="ignore", sublinear_tf=True)
            vec.fit(X_train)
            
            test_val = X_test[0]
            
            """ Classification Testing """
            #vectorizerPipeline(X_train, X_test, y_train, y_test, test_val)
            #vectorizerKNN(X_train, X_test, y_train, y_test, vec, test_val)
            #vectorizerNB(X_train, X_test, y_train, y_test, vec, test_val)
            #vectorizerDT(X_train, X_test, y_train, y_test, vec, test_val)
            #vectorizerRF(X_train, X_test, y_train, y_test, vec, test_val)
            #vectorizerSVM(X_train, X_test, y_train, y_test, vec, test_val)
            #y_pred = vectorizerSVC(X_train, y_train, X_test, vec)
            vectorizerSVC2(X_train, X_test, y_train, y_test, vec)
 
        