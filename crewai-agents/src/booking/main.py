#!/usr/bin/env python
import sys
import warnings
import threading
import time
from researcher.crew import Researcher
from booking.crew import MakeReservation
from booking.crew import run_server

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    prompt = (
        "Book my trip between columbus, OH and New york city. Book only flight and hotel for me. No car rental"
    )

    inputs = {
        "origin": "Columbus, OH",
        "destination": "New York, NY",
        "user_name": "Nilanjan",
    }
    MakeReservation().crew(prompt, "Nilanjan", "Columbus, OH", "New York, NY").kickoff()


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        Researcher().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Researcher().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        Researcher().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
