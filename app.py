import streamlit as st
import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_community.llms import Ollama

# Set up the environment variables
os.environ["SERPER_API_KEY"] = "a267dc1a84ac133e64128608f08910cf27d4f8b1"

# Set up the LLM and the search tool
llm = Ollama(model="openhermes")
search_tool = SerperDevTool()

# Streamlit UI for user inputs
st.title("Real Estate Investment Property Finder")
st.header("Input your query")

# User input for the location
location = st.text_input("Enter the location (e.g., Sydney, Australia):", "Sydney, Australia")
property_type = st.text_input("Enter the property type you're interested in (e.g., retail, residential):", "retail")
research_goal = f"Find promising investment {property_type} properties in {location}."

# Agents and task creation based on user input
if st.button("Get Property Insights"):
    st.write(f"Researching {property_type} properties in {location}...")

    researcher = Agent(
        llm=llm,
        role="Senior Property Researcher",
        goal=research_goal,
        backstory="You are a veteran property analyst. You are looking for properties to invest in.",
        allow_delegation=False,
        tools=[search_tool],
        verbose=True,
    )

    task1 = Task(
        description=f"Search the internet and find 5 promising {property_type} investment suburbs in {location}. For each suburb, highlight the mean, low, and max prices as well as the rental yield and other useful factors.",
        expected_output=f"A detailed report of {property_type} investment opportunities in {location}.",
        agent=researcher,
        output_file="task1_output.txt",
    )

    writer = Agent(
        llm=llm,
        role="Senior Property Analyst",
        goal="Summarise property facts into a report for investors.",
        backstory="You are a real estate agent compiling property analytics into a report for potential investors.",
        allow_delegation=False,
        verbose=True,
    )

    task2 = Task(
        description="Summarise the property information into bullet points.",
        expected_output=f"A summarised list of promising {property_type} investment suburbs in {location}, prices, and features.",
        agent=writer,
        output_file="task2_output.txt",
    )

    crew = Crew(agents=[researcher, writer], tasks=[task1, task2], verbose=2)
    
    # Run the tasks
    task_output = crew.kickoff()

    # Display the output
    st.header("Results:")
    st.write("Here are the results based on your input:")
    st.text(task_output)

    st.write("Detailed suburb report saved in 'task1_output.txt'")
    st.write("Summary report saved in 'task2_output.txt'")
