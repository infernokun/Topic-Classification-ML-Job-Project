import csv
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

from tkinter import messagebox
import shutil
import tkinter as tk

import gui_funcs as gui
import os

# name of all topics (30)
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
    
    # get list of codedData's topics
    codedData['answers'] = list(codedData['answers'])

    # add dictionary string and topic to codedData
    for i in codedData['dictionary']:
        codedData['data'].append(i[0])
        codedData['answers'].append(int(i[1]))
        
    # change by to np array
    codedData['answers'] = np.array(codedData['answers'])
        
    vec = TfidfVectorizer(decode_error="ignore", sublinear_tf=True)
    
    # train the dataset with the categorized data
    vec.fit(codedData['data'])
    
    # perform a generalization of the uncoded data
    uncodedData_g = generalizeUncodedData(uncodedData['data'], uncodedData['titleText'])
    
    # perform SVC to predict the uncoded data, returns the predictions
    predictions = vectorizerSVC(codedData['data'], codedData['answers'], uncodedData_g, vec)
    
    # update status text
    status["text"] = "Done"
    
    return predictions
    
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
    gui.modifyNewFile(predictions, uncodedData, p3, codedData)  

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
    positions = {}
    newDictionary = []
    
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
                data.append(text.replace("\"", ""))
                
                answers.append(topic)
            
            else:
                count2 = 0
                for i in row:
                    positions['{}'.format(str(i))] = count2
                    count2 = count2 + 1

            count = count + 1

    # searches for dictionary.txt
    try:
        # should be in cwd
        currdir = os.getcwd()
        filename2 = currdir + "\\dictionary.txt"
        
        # open file and read each line that will be split by ~
        with open(filename2) as f:
            lines = f.readlines()
            
            # a list of the dictionary input and the corresponding topic
            for i in lines:
                newVal = i.split('~')
                newDictionary.append(newVal)
        
        f.close()
    
        # remove \n from string
        for i in range(len(newDictionary)):
            newDictionary[i][1] = newDictionary[i][1].replace("\n", "")
    except:
        print("no dictionary file")
        
    dataset = {}
    
    # dataset for data and title / text indicies
    dataset['title'] = np.array(title)
    dataset['data'] = list(data)
    dataset['answers'] = np.array(answers)
    dataset['dictionary'] = newDictionary
    dataset['positions'] = positions
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
    positions = {}
    
    # init index for title and text position
    titleIdx = 0
    textIdx = 0
    
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
                # each row contains 10 elements
                for i in range(0, len(row)-1):
                    # append with space
                    if (str(row[i]) == ""):
                        dataRow.append(str(""))
                    else:
                        dataRow.append(str(row[i].replace("\"", "")))
            else:
                # case for 0 index
                count2 = 0
                for i in row:
                    positions['{}'.format(str(i))] = count2
                    # find the title index
                    if (str(i) == "title"):
                        titleIdx = count2
                    # find the text index
                    elif (str(i) == "unit_text"):
                        textIdx = count2
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
    dataset['positions'] = positions
    #dataset['answers'] = ""
    #dataset['data_features'] = np.array(['title', 'text'])

    return dataset
    
# performs SVC on the dataset
def vectorizerSVC(data, answers, uncodedData, vec):
    
    # SVC
    clf = LinearSVC(C=5)
    clf.fit(vec.transform(data), answers)
    y_pred = clf.predict(vec.transform(uncodedData['data']))
    
    return y_pred
                                                   
# main function
if __name__ == '__main__':
    
    # start tkinter instance
    root = tk.Tk()
    gui.windowHandler(root)
 
        