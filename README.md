# Topic-Classification-ML-Job-Project
## Topic Classification

```
   For this project, I used Python and various libraries to achieve the goal of classifying sets of data based on existing classified samples. The main libraries used are csv (for handling csv read and write operations), numpy (for better data visualization and increased helper functions compared to using a regular list of data), sklearn (for the machine learning tools and algorithms), and tkinter (for the graphic user interface). 
  
   I have the program broken down into different functions that help assist in generalizing the data to a form that will work efficiently when performing machine learning. The coded csv file is sent to a python dictionary with just the title appended in front of the unit text and the corresponding topic in as well. The text is also converted to all lowercase which is better for the computer to process without any misunderstandings. The uncoded data is done with same way, except without a corresponding topic. I also copy all the values from the uncoded csv file to append it to the end of the coded csv file. Since the given file has the title and unit_text in different column indices, I accounted for program to determine with column contain those sections.
  
   For the machine learning portion, I used the TfidfVectorizer to convert the text data to numerical values that will be used to count occurrences and weigh important words with a Tfidf value. This worked a bit better compared to using CountVectorizer, which just counts the occurrence. After vectorizing the data, I perform the algorithm LinearSVC which is a supervised learning classifier. This is a subset of support vector machines, which provides borders around the data to determine which sample is within a topic’s border.
```
  
  ![application launch](https://i.imgur.com/2a0pqal.png)
## 70% Train - 30% Test Results

```
                                              precision    recall  f1-score   support

No Substantive Higher Education Information       0.93      0.87      0.90       181
                                  Academics       0.78      0.73      0.75        44
                                     Access       0.77      0.87      0.82        23
                             Accountability       0.84      0.84      0.84       128
                             Administration       0.86      0.84      0.85       118
   Adult Education/Non-Traditional Students       0.82      0.81      0.81        77
                              Affordability       0.88      0.95      0.91       225
                                  Athletics       0.91      1.00      0.95        10
                          Budgets/Resources       0.98      0.98      0.98      1240
                       Community Engagement       1.00      1.00      1.00         8
                                 Completion       0.93      0.69      0.79        39
                           Diversity/Equity       0.84      0.72      0.78        29
              Economic Outcomes and Impacts       0.75      0.81      0.78        79
                                 Enrollment       0.92      0.65      0.76        17
                                 Facilities       0.87      0.85      0.86        46
                 Faculty and Staff Concerns       0.89      0.85      0.87        48
                         Goals/Master Plans       0.63      0.73      0.68        33
                         Graduate Education       1.00      1.00      1.00         1
                          Honors and Awards       1.00      1.00      1.00         2
                Preparation and Remediation       0.77      0.80      0.78        79
                       Quality of Education       0.77      0.45      0.57        22
          Research and Faculty Publications       0.91      0.94      0.92        31
                                  Retention       0.60      0.50      0.55         6
                                     Safety       0.86      0.90      0.88        21
                               Student Debt       0.95      0.69      0.80        26
                           Student Services       1.00      1.00      1.00         8
                       System-Level Matters       0.74      0.85      0.79       150
                                 Technology       0.87      0.76      0.81        17
                          Transfer Students       0.93      0.78      0.85        18
                                    Tuition       0.94      0.96      0.95       304

                                   accuracy                           0.91      3030
                                  macro avg       0.86      0.83      0.84      3030
                               weighted avg       0.91      0.91      0.91      3030
```
