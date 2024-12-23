import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileReadTool

# Environment Variables - Replace these with your actual API keys
serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    raise ValueError("Please set the SERPER_API_KEY environment variable")

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Tools
# Tools
search_tool = SerperDevTool()
file_reader = FileReadTool()

# Input Repository URL
repo_url = input("Enter the GitHub repository URL: ")

# Agents
repository_analyst = Agent(
    role="Repository Analyst",
    goal="Analyze GitHub repositories and document insights.",
    backstory="Expert in code analysis and repository breakdowns.",
    tools=[search_tool, file_reader],
    verbose=True
)

tutorial_writer = Agent(
    role="Tutorial Writer",
    goal="Write structured tutorials for repositories.",
    backstory="Technical writer skilled at simplifying complex concepts.",
    tools=[],
    verbose=True
)

seo_specialist = Agent(
    role="SEO Specialist",
    goal="Optimize tutorial content for SEO without changing the technical focus.",
    backstory="SEO expert focused on enhancing readability without sacrificing technical accuracy.",
    tools=[search_tool],
    verbose=True
)

blog_post_creator = Agent(
    role="Blog Post Creator",
    goal="Adapt tutorials into engaging, SEO-compliant blog posts with a focus on the repository's purpose and features.",
    backstory="Creative writer with experience in blog formatting without losing technical details.",
    tools=[],
    verbose=True
)

# Tasks
analyze_repository_task = Task(
    description=f"Analyze the repository at {repo_url} to extract structure, features, and purpose.",
    expected_output="Detailed insights into the repository, including code snippets.",
    agent=repository_analyst,
)

write_tutorial_task = Task(
    description="Draft a step-by-step tutorial based on the repository analysis. Ensure examples highlight repository usage.",
    expected_output="A markdown-formatted tutorial with setup and usage details.",
    agent=tutorial_writer,
)

seo_optimization_task = Task(
    description="Optimize the tutorial for SEO by adding keywords, headings, and metadata, ensuring no technical details are lost.",
    expected_output="An SEO-optimized tutorial ready for publishing, preserving technical accuracy.",
    agent=seo_specialist,
)

format_blog_post_task = Task(
    description="Adapt the tutorial into an SEO-friendly blog post with repository-focused narratives and examples.",
    expected_output="A markdown-formatted blog post, ready for publishing, that highlights the repository’s features and use cases.",
    agent=blog_post_creator,
)

# Crew
crew = Crew(
    agents=[repository_analyst, tutorial_writer, seo_specialist, blog_post_creator],
    tasks=[
        analyze_repository_task,
        write_tutorial_task,
        seo_optimization_task,
        format_blog_post_task,
    ],
    process=Process.sequential
)

# Kickoff
result = crew.kickoff(inputs={"repo_url": repo_url})
print(result)
