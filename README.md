# Tutor-Agent
LLM powered tutor to help you study and track progress on the material you are studying. 

The reason I am making this is because I am studying machine learning and I want an AI agent that can help me learn. It is written in Python, using LangChain, and the OpenAI API.

Core functionality of the agent: 
- Test the users knowlwdge based off their own set of notes by asking them questions on the contents of these notes.
- Grade their answers on each set of questions it gives them, log the users grade and the date the questions were answered.
- Display what grades the user has been getting on each topic.
- Schedule what topics I should learn each day so that I study each topic at specific time intervals.
- Let the user specify which topics are most important so the sytem proritises these topics in the schedule.
- Let the user specify how much time he wants to spend studying today, the agent then automatically starts the study session.

