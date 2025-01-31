from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool
from researcher.tools.custom_tool import MyCustomTool

@CrewBase
class Researcher():
	"""Researcher crew"""

	@before_kickoff
	def before_kickoff_function(self, inputs):
		print(f"Before kickoff function with inputs: {inputs}")
		return inputs # You can return the inputs or modify them as needed

	@after_kickoff
	def after_kickoff_function(self, result):
		print(f"After kickoff function with result: {result}")
		return result # You can return the result or modify it as needed

	@agent
	def researcher(self) -> Agent:
		return Agent(
		config=self.agents_config['researcher'],
		verbose=True,
		tools=[MyCustomTool()]
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
		config=self.agents_config['reporting_analyst'],
		verbose=True,
		)

	# Define the manager agent
	manager = Agent(
		role="Project Manager",
		goal="Efficiently manage the crew and ensure high-quality task completion",
		backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard.",
	)

	@task
	def research_task(self) -> Task:
		return Task(
		config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
		config=self.tasks_config['reporting_task'],
		output_file='output/report.md' # This is the file that will be contain the final report.
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Researcher crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
