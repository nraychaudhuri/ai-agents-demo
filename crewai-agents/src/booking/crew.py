import os
import json
from datetime import datetime
from queue import Queue

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import SerperDevTool
from crewai.tools import tool
from textwrap import dedent
from simple_websocket_server import WebSocket, WebSocketServer
from typing import Any

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

manager_llm = LLM(model="deepseek/deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))


@tool("search flight")
def search_flight(origin: str, destination: str) -> str:
    """Searches for flight bewteen origin and destination locations."""
    # print(">>>>> RESPONSE FROM client ", response)
    return f"Found delta flight between {origin} and {destination}. Plenty of seats are available"


@tool("book flight")
def book_flight(origin: str, destination: str) -> str:
    """books the flight bewteen origin and destination locations."""
    # Function logic here
    return f"Flight is booked. Here is the confirmation number FXXX1234"


@tool("book hotel")
def book_hotel(destination: str) -> str:
    """Searches and books the best hotel for the given location."""
    # Function logic here
    return f"Marriot hotel is booked. Here is the confirmation number HXXX4444"


@tool("book car rental")
def book_car_rental(destination: str) -> str:
    """Searches and books the best car rental for the given location."""
    # Function logic here
    return f"Avis is booked for you. Here is the confirmation number CXXX5555"


@CrewBase
class MakeReservation:
    """Reservation crew"""

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        return inputs  # You can return the inputs or modify them as needed

    @after_kickoff
    def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result  # You can return the result or modify it as needed

    @agent
    def flight_booking_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["flight_booking_agent"],
            verbose=True,
            tools=[search_flight, book_flight],
            allow_delegation=False,
        )

    @agent
    def hotel_booking_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["hotel_booking_agent"],
            verbose=True,
            tools=[book_hotel],
            allow_delegation=False,
        )

    @agent
    def car_rental_booking_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["car_rental_booking_agent"],
            verbose=True,
            tools=[book_car_rental],
            allow_delegation=False,
        )

    def create_manager_agent(self, goal: str) -> Agent:
        # Define the manager agent
        a = Agent(
            role="Booking Manager",
            goal=goal,
            backstory="You're an experienced travel agent and manager, skilled in overseeing team of specialized agents that can book flights, hotels and car rentals. Your role is to coordinate the efforts of these agents to ensure the task provide to you is met. Make sure to share the summary all the requested booking that are made.",
            allow_delegation=True,
            llm=manager_llm,
        )
        print(">>>> manager agent ", a)
        return a

    def identify_task(self, prompt, user_name, origin, destination):
        return Task(
            description=dedent(
                f"""
				Your objective is to make book a trip for {user_name}.
				A trip might include flight, hotel and car rental. Depending
				upon the specific requirement provided by the user you find the
				best fight, hotela and car rental.
				Your final answer must be a detailed
				report of all the bookings made.

				Here is the request from user:

				{prompt}

				Traveling from: {origin}
				Traveling to: {destination}
			"""
            ),
            expected_output="List down all the bookings made for the trip",
        )

    @crew
    def crew(
        self, special_inst: str, user_name: str, origin: str, destination: str
    ) -> Crew:
        """Creates the Booking crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=[
                self.identify_task(special_inst, user_name, origin, destination)
            ],  # Automatically created by the @task decorator
            verbose=True,
            manager_agent=self.create_manager_agent(special_inst),
            process=Process.hierarchical,
        )
