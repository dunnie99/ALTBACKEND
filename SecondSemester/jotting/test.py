
def myMapping(name, age, gender):
    return {
        "name": name,
        "age": age,
        "gender": gender
    }






class Person:

    num_of_students = 0
    def __init__(self, name, age, gender, grade):  # The __init__ function is a constructor. It is called when you create an object.

        self.name = name
        self.age = age
        self.gender = gender
        self.grade = grade

        Student.num_of_students =+1
    
    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")
    
    def get_student_details(self):
        return f"{self.name} is {self.age} years old and is in grade {self.grade}."

student1 = Person("Dunnie", 25, "female")
student2 = Person("Vincente", 26, "male")
print(student1.say_hello())
