import csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

import shutil
import os

import gui_funcs as gui

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

    print("You chose {}".format(filename))

    """ 
    open Training set file
    grabs index of title, unit_text, and topic row names
    """
    with open(filename) as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            # not the first row which are the labels
            if idx != 0:
                header = str(row[positions['title']]).lower()
                text = str(row[positions['unit_text']]).lower()
                topic = int(row[positions['topic']])

                title.append(header)
                data.append(text.replace("\"", ""))
                answers.append(topic)

            else:
                # the titles of each row
                for idx2, rowName in enumerate(row):
                    positions['{}'.format(str(rowName))] = idx2

    dictFile = os.getcwd() + "\\Original Files\\dictionary.txt"

    with open(dictFile) as f:
        lines = f.readlines()

        for i in lines:
            newVal = i.split('~')
            newDictionary.append(newVal)

    f.close()

    for i in range(len(newDictionary)):
        newDictionary[i][1] = newDictionary[i][1].replace("\n", "")

    dataset = {}

    dataset['title'] = np.array(title)
    dataset['data'] = list(data)
    dataset['answers'] = np.array(answers)
    dataset['dictionary'] = newDictionary
    dataset['positions'] = positions
    dataset['target_subject'] = np.array(subjects)
    dataset['data_features'] = np.array(['title', 'text'])

    return dataset

# performs SVC on the dataset


def vectorizerSVC2(X_train, X_test, y_train, y_test, vec, codedData):
    # SVC
    clf = LinearSVC(C=5)
    clf.fit(vec.transform(X_train), y_train)

    y_pred = clf.predict(vec.transform(X_test))

    print(classification_report(y_test, y_pred, target_names=subjects))

    return y_pred


# main function-ok
if __name__ == '__main__':
    # start tkinter instance

    """below for display purposes"""
    filename = os.getcwd() + "\\Original Files\\Coded Data.csv"

    fileLen = len(filename)

    if fileLen > 0:
        if (filename[fileLen-4:fileLen] != ".csv"):
            print("Must be .csv file!")
        else:
            pass
            # gets full training set
            fulldata = getTrainingSet(filename)

            """
            labels = unique labels
            counts = total count of elements for label
            """

            labels, counts = np.unique(fulldata['answers'], return_counts=True)

            # Train test split for training dataset
            X_train, X_test, y_train, y_test = train_test_split(
                fulldata['data'], fulldata['answers'], test_size=0.3, random_state=0)

            y_train = list(y_train)

            # add dictionary answers
            for i in fulldata['dictionary']:
                X_train.append(i[0])
                y_train.append(int(i[1]))

            vec = TfidfVectorizer(decode_error="ignore", sublinear_tf=True)

            vec.fit(X_train)

            """ Classification Testing """
            vectorizerSVC2(X_train, X_test, y_train, y_test, vec, fulldata)
