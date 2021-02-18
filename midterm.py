# Assignment 4, Question 1
# Author: Angele Park Collin

import matplotlib.pyplot as plt

def read_csv(filename):
    '''
    Read the CSV file at the given filename
    and return the data contained within as a list of lists.
    '''
    data = []
    f = open(filename, "r")
    
    for line in f:
        line = line.strip() # gets rid of '\n'
        row = line.split(",")
        data.append(row)
    
    f.close()
    return data


def count_x_in_row(row):
    num_x = 0
    for element in row:
        if 'x' in element.lower():
            num_x += 1
    return num_x

def get_row_for_question(data, topic, question):
    for row in data:
        if 'T{}Q{}'.format(topic, question) in row[0]:
            return row
    raise ValueError("Topic and/or question not found.")

def get_num_questions_in_topic(data, topic):
    start_row = -1
    for i, row in enumerate(data):
        if 'Topic {}'.format(topic) in row[0]:
            start_row = i
        elif start_row > -1 and 'Topic ' in row[0]:
            break
    
    if start_row == -1:
        raise ValueError("Topic not found.")
    
    if i == len(data) - 1:
        i += 1
    
    return i - start_row - 1

def get_num_students(data):
    num_students = 0
    for col_index in range(1, len(data[0])):
        num_topics_left = int(data[1][col_index]) + int(data[2][col_index])
        if num_topics_left < 3:
            num_students += 1
    return num_students

def get_num_students_for_topic(data, topic):
    for row in data:
        if 'Topic {}'.format(topic) in row[0]:
            return count_x_in_row(row[1:])
    raise ValueError("Topic not found.")

def get_topics_for_student(data, student_col_index):
    topics = []
    for row in data:
        if 'Topic ' in row[0] and 'x' in row[student_col_index].lower():
            topics.append(int(row[0].split()[-1]))
    return topics


# PART 1
def plot_num_students_per_topic(data):    
    datas=[]
# 13 Topics in range 1-14
    for topics in range(1,14):
# Divide the number or students for each topic by total number of students to get the percentage for
# the number of students per topic relative to all the students 
        students_per_topic=get_num_students_for_topic(data,topics)
        total_students_took_test=get_num_students(data)
        percentages=students_per_topic/total_students_took_test
        datas.append(percentages)
# Number of labels match number of values in list data and each position i of catgories match i of data    
    categories=["Topic1", "Topic 2", "Topic 3", "Topic 4", "Topic 5", "Topic 6", "Topic 7", "Topic 8", "Topic 9", "Topic 10", "Topic 11", "Topic 12", "Topic 13"]
# Show pie and give it a title in relation to what the chart represents            
    plt.pie(datas,labels=categories)
    plt.title("Number of Students per Topic", fontsize=22)
    plt.show()


# PART 2
def get_average_of_question(data, topic, question):
# Find the number of total x's per question and then divide by total number of students for that topic
    row=get_row_for_question(data,topic,question)
    correct_answers_per_question=count_x_in_row(row)
    students_per_topic=get_num_students_for_topic(data, topic)
    average=correct_answers_per_question/students_per_topic
# Return the average number of correct answers for a given question
    return average

def get_average_of_topic(data, topic):
# Number of questions per topic   
    num_of_questions=get_num_questions_in_topic(data, topic)
    list_of_avgs=[]
# Going through each question in the topic and appending the average for each question into list
    for each_question in range(1,num_of_questions+1):
        avg_each_question=get_average_of_question(data,topic,each_question)
        list_of_avgs.append(avg_each_question)
# Take the sum of all the averages in the topic and divide by the number of questions to get the average of the topic
    avg_of_averages=(sum(list_of_avgs))/num_of_questions
        
    return avg_of_averages
    
def plot_topic_averages(data):
# Making a list from range 1-14 for the ticks    
    num_topics=list(range(1,14))
    list_of_averages=[]
# For each of the 13 topics, calculate the averages of each question in the topic then the average of averages   
    for topics in range(1,14):
        avg_for_topic=get_average_of_topic(data, topics)
        list_of_averages.append(avg_for_topic)
# Create the bar graph and number each tick according to the topic number
    plt.bar(num_topics, list_of_averages)
    plt.xticks(num_topics)
    plt.xlabel("Average Grade", fontsize=16)
    plt.ylabel("Topic Number", fontsize=16)
    plt.title("Average per topic", fontsize=22)
    plt.show()


# PART 3
def get_student_average(data, student_col_index):
# If student was given questions, set count for correct answer and total questions asked
    topics_student_was_given=get_topics_for_student(data, student_col_index)
    if len(topics_student_was_given)>0:
        correct_answers=0
        num_questions_asked=0
# For each topic in the list of topics the student was given, get the number of questions per topic        
        for topic in topics_student_was_given:
            num_questions_in_topic=get_num_questions_in_topic(data,topic)
# For each question in topic, increase count fro total questions asked and get number of x's in the
# column of the particular student to then increase count of correct answers
            for question in range(1,num_questions_in_topic+1):
                num_questions_asked+=1
                row=get_row_for_question(data,topic,question)
                result_of_question=count_x_in_row(row[student_col_index])
# Counting the number of questions student answered correctly                
                if result_of_question==1:
                    correct_answers+=1
# Calculating student average         
        student_average=correct_answers/num_questions_asked
        return student_average
# If student was given 0 questions/no topics then return None  
    elif len(topics_student_was_given)==0:
        return None

def get_student_averages(data):
# Get number of students who sat for the midterm (no None values)     
    all_students=get_num_students(data)
    list_of_averages=[]
    for each_student in range(1,all_students+1): # Starting student 1 and including 145th student
# Append the average of each student into the list to return the list of averages for each student.
        avg_each_student=get_student_average(data, each_student)
        list_of_averages.append(avg_each_student)

    return list_of_averages

def plot_student_averages(data):
# Getting the list of averages without the None value to create a histogram
    averages_without_none=[]
    all_averages=get_student_averages(data)
# Appending all values that arent None into new list
    for averages in all_averages:
        if averages != None:
            averages_without_none.append(averages)
# Setting the data to put into the histogram     
    plt.hist(averages_without_none, bins=20)
    plt.title("Average Grades")
    plt.xlabel("Percentages", fontsize=16)
    plt.ylabel("Number of Students", fontsize=16)
    increments=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    plt.xticks(increments)
    plt.show()
        
# PART 4
def get_hard_questions(data):
# First get the number of students per topic and the number of questions in each topic
    list_hard_questions=[]
    for topics in range(1,14):
        students_per_topic=get_num_students_for_topic(data, topics)
        questions_in_topic=get_num_questions_in_topic(data, topics)
# Get all the rows for each question and also get the index of the topic/question for each question    
        for rows in range(1,questions_in_topic+1):
            rows_for_questions=get_row_for_question(data,topics,rows)
            list_of_correct_answers=[]
            correct=0
            index=rows_for_questions[0]
# Count the total number of x in each row (correct answers) 
            for X in rows_for_questions:
                x_count=count_x_in_row(X)
                if x_count==1:
                    correct+=1              
# Get average for each of the 40 questions by divinding the correct answers by the amount of people who were given the question              
            avg_per_question=correct/students_per_topic
# If the average is below 0.4 then those questions were hard so return the list of hard questions with the index previously defined
            if avg_per_question<0.4:
                list_hard_questions+=[index]
    return list_hard_questions
               
            
# ADDITIONAL FUNCTIONALITY - Plotting averages of students for each grader
def list_of_graders(data):
# Create list of only the graders without any duplicates
    list_of_graders=[]
    for graders in data[3]:
        if graders not in list_of_graders:
            if graders.startswith("#"):
                list_of_graders.append(graders)
    return(list_of_graders) #['#1021', '#9130', '#5392', '#8385', '#0012']

def avg_student_per_grader(data):
# Call list of graders and create empty list for each grader
    graders=list_of_graders(data)
    grader1=[]
    grader2=[]
    grader3=[]
    grader4=[]
    grader5=[]
    total_students=get_num_students(data)
# For each student in the range of all the students
    for student in range(1,total_students+1):
# If the grader in the student column matches the grader in the grader list then append their average to the grader1 list
        if data[3][student]==graders[0]: # 1021
            student_average=get_student_average(data, student)
            grader1.append(student_average)
# If the grader matches, append the student average in grader 2 list            
        elif data[3][student]==graders[1]:# 9130
            student_average=get_student_average(data, student)
            grader2.append(student_average)
# If the grader matches, append the student average in grader 3 list                        
        elif data[3][student]==graders[2]:# 5392
            student_average=get_student_average(data, student)
            grader3.append(student_average)
# If the grader matches, append the student average in grader 4 list                       
        elif data[3][student]==graders[3]:# 8385
            student_average=get_student_average(data, student)
            grader4.append(student_average)
# If the grader matches append the student average in grader 5  list                 
        elif data[3][student]==graders[4]:# 0012
            student_average=get_student_average(data, student)
            grader5.append(student_average)
# Create new empty lists
    average_per_grader=[]
    g1=[]
    g2=[]
    g3=[]
    g4=[]
    g5=[]
# Remove None value in each graders list
    for nums in grader1:
        if nums != None:
            g1.append(nums)
    for nums in grader2:
        if nums != None:
            g2.append(nums)
    for nums in grader3:
        if nums != None:
            g3.append(nums)
    for nums in grader4:
        if nums != None:
            g4.append(nums)
    for nums in grader5:
        if nums != None:
            g5.append(nums)
            
# Append each list without None into a one list
    average_per_grader.append(g1)
    average_per_grader.append(g2)
    average_per_grader.append(g3)
    average_per_grader.append(g4)
    average_per_grader.append(g5)
    
# Return a list of lists of the averages per grader  
    return (average_per_grader)


def plot_grader_averages(data):
# Get average of averages of each grader
    list_of_averages=avg_student_per_grader(data)
    avg_per_grader=[]
    for graders in list_of_averages:
        avg=sum(graders)/len(graders)
        avg_per_grader.append(avg)
        
# Plotting the average of averages of students per grader in a scatter plot
    graders=["#1021", "#9130", "#5392", "#8385", "#0012"]
    plt.scatter(graders,avg_per_grader)
    plt.title("Student Average per Grader")
    plt.xlabel("Graders", fontsize=16)
    plt.ylabel("Student Averages", fontsize=16)
    plt.show()

   
if __name__ == '__main__':
    data = read_csv("midterm.csv")
    plot_num_students_per_topic(data)
    plot_topic_averages(data)
    plot_student_averages(data)
    plot_grader_averages(data)
    print("The hard questions were:", get_hard_questions(data)) # ['T4Q2', 'T6Q2','T6Q3','T9Q1']
