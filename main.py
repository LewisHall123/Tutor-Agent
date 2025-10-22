
from agents import agent1, agent2, agent3  
from Load_docs import load_documents, create_faiss_index, read_file
from config import INDEX_PATH, NOTES_DIR, TOPICS_DIR

# Load text files into a list, once you run this code once, you can comment it out.
docs = load_documents(NOTES_DIR)

# Function to create the FAISS index, once you run this code once, you can comment it out.
create_faiss_index(docs, INDEX_PATH, embeddings_model=None)

# Read in a .txt file contaning the topics the student is studying to be used as part of the first prompt.
with open(TOPICS_DIR) as f:
    Prompt1 = f.read()

# Get agent to think of four quesitons for the student
Question_generator = agent1.invoke( {"messages": [{"role": "user", 
                                  "content": Prompt1}]})

# Print the four questions the agent made for the student
Questions_for_student = Question_generator['messages'][-1].content
print("Answer these questions as best you can: \n\n", Questions_for_student)

# Save the sudents answers to the questions.
Student_answers = ""
for i in range(4):
    answer = input(f"Question {i+1}/4: ")
    Student_answers += answer + " "  

# Assemble a prompt contaning the questions to the student, and the student's answers.
Prompt2 = "Questions the student was asked: " + Questions_for_student + "/n" + "Answers the student gave: " + Student_answers

# Get the agent to mark the questions
Marking_of_questions = agent2.invoke( {"messages": [{"role": "user", 
                                  "content": Prompt2}]})
Students_marks_for_questions = Marking_of_questions['messages'][-1].content

# Prompt containing: the questions, students answers, and the marks for his answers.
Prompt3 = Prompt2 + "The feedback the student got: " + Students_marks_for_questions

Update_progress_report = agent3.invoke( {"messages": [{"role": "user", 
                                  "content": Prompt3}]})

# Confirm the progress report was updated
print(Update_progress_report['messages'][-1].content)


