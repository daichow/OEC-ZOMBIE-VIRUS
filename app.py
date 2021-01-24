import pandas as pd
import numpy as np
from collections import Counter
from pprint import pprint
import random

student_data = pd.read_excel("./OEC2021_-_School_Record_Book_.xlsx")

# this holds the records for all the students in this school
records = student_data.to_dict(orient="records")

data = pd.read_excel("./OEC2021_-_School_Record_Book_.xlsx")

classes = list(
    set(data["Period 1 Class"].tolist())
)  # here is a list of all the classes + periods taught at school

clubs = [
    "Board Game Club",
    "Football",
    "Soccer",
    "Video Game Club",
    "Band",
    "Computer Science Club",
    "Choir",
    "Basketball",
    "Badminton",
    "Baseball",
]  # here is a list of all the clubs at school. Weren't able to use it due to lack of time

schedule = dict()  # this holds the number of students in each class during each period

for period in [
    "Period 1 Class",
    "Period 2 Class",
    "Period 3 Class",
    "Period 4 Class",
    "Extracurricular Activities",
]:
    if period != "Extracurricular Activities":
        total_students = {}
        for class_name in classes:
            total_students[class_name] = {
                "num_students": Counter(data[period].tolist())[class_name],
                "students": [
                    "{} {}".format(s["First Name"], s["Last Name"])
                    for s in records
                    if s[period] == class_name
                ],
            }
        schedule[period] = total_students
    else:
        total_students = {}
        for club in clubs:
            total_students[club] = {"num_students": 0, "students": []}
        schedule[period] = total_students

# these are all of the initial zombies
initial_zombies = [
    "Florencio Braun",
    "Jory Cookie",
    "Lucas Cruikshank",
    "Lewis Dickinson",
]

zombies = []
# adding new fields to each students records for infection prediction and full name
for student in records:
    student["infection prediction period 1"] = 0
    student["infection prediction period 2"] = 0
    student["infection prediction period 3"] = 0
    student["infection prediction period 4"] = 0
    name = "{} {}".format(student["First Name"], student["Last Name"])
    student["name"] = name
    if name in initial_zombies:
        student["infection prediction period 1"] = 100
        student["infection prediction period 2"] = 100
        student["infection prediction period 3"] = 100
        student["infection prediction period 4"] = 100
        student["name"] = name
        zombies.append(student)

# data cleaning [removing None types] from student records
for period in schedule:
    if None in schedule[period]:
        del schedule[period][None]

"""
This function updates the infection prediction for each period
"""


def update_infection_prediction(period, class_students, class_zombies):
    current_period = period.replace("Class", "").rstrip().lower()
    infection_prediction = "infection prediction {}".format(current_period)
    probability_weights = []
    for student in records:
        # access the records of each student in the class
        if student["name"] in class_students:
            # update the infection prediction for current class and period

            # age based multiplier
            if student["Grade"] == 9:
                age = 14
            elif student["Grade"] == 10:
                age = 15
            elif student["Grade"] == 11:
                age = 16
            elif student["Grade"] == 12:
                age = 17

            age_based_multiplier = (1.5) ** ((age - 14) / 2)

            # health based multiplier
            if student["Health Conditions"] != None:
                health_multiplier = 1.7
            else:
                health_multiplier = 1

            student[infection_prediction] += (
                (
                    (health_multiplier * age_based_multiplier * 3 * len(class_zombies))
                    / len(class_students)
                )
            ) * 100

            if student[infection_prediction] > 100:
                student[infection_prediction] = 100
            probability_weights.append(student[infection_prediction] / 100)

    # make a zombie of three random students in the class who are most likely to be infected
    # and appended them into the total zombies in school
    for i in range(0, 3):
        z = random.choices(class_students, probability_weights)
        for student in records:
            if student["name"] == z[0]:
                zombies.append(student)


def update_apocalypse():

    for period in schedule:
        # print("STARTING A NEW PERIOD")
        for _class in schedule[period]:
            class_zombies = []
            # update what zombies are in the current class
            for zombie in zombies:
                if zombie["name"] in schedule[period][_class]["students"]:
                    class_zombies.append(zombie)
            # update infection rate if there exists zombies in the class
            # meaning the class is infected
            if len(class_zombies) != 0:
                update_infection_prediction(
                    period, schedule[period][_class]["students"], class_zombies
                )


update_apocalypse()  # START THE GENERATOR


def display_student_data(student_id):
    for student in records:
        if student["Student Number"] == student_id:
            print("*" * 30)
            print(f"STUDENT {student_id}: ")
            print("*" * 30)
            pprint(student)
            print("*" * 30)
            print("ALL TURNED ZOMBIES: ")
            print("*" * 30)
            print([z["name"] for z in zombies])


display_student_data(float(input("Please type down your student id: ")))