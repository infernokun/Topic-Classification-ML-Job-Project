# Topic-Classification-ML-Job-Project

##Topic Classification

   For this project, I used Python and various libraries to achieve the goal of classifying sets of data based on existing classified samples. The main libraries used are csv (for handling csv read and write operations), numpy (for better data visualization and increased helper functions compared to using a regular list of data), sklearn (for the machine learning tools and algorithms), and tkinter (for the graphic user interface). 
  
   I have the program broken down into different functions that help assist in generalizing the data to a form that will work efficiently when performing machine learning. The coded csv file is sent to a python dictionary with just the title appended in front of the unit text and the corresponding topic in as well. The text is also converted to all lowercase which is better for the computer to process without any misunderstandings. The uncoded data is done with same way, except without a corresponding topic. I also copy all the values from the uncoded csv file to append it to the end of the coded csv file. Since the given file has the title and unit_text in different column indices, I accounted for program to determine with column contain those sections.
  
   For the machine learning portion, I used the TfidfVectorizer to convert the text data to numerical values that will be used to count occurrences and weigh important words with a Tfidf value. This worked a bit better compared to using CountVectorizer, which just counts the occurrence. After vectorizing the data, I perform the algorithm LinearSVC which is a supervised learning classifier. This is a subset of support vector machines, which provides borders around the data to determine which sample is within a topic’s border.
  
  ![application launch](https://i.imgur.com/2a0pqal.png)
