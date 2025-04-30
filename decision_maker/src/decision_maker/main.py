#!/usr/bin/env python3

from crew import DecisionMakerDiscovery


def run():
    inputs = {
        "company_names": "Google, Airbnb"
    }

    DecisionMakerDiscovery().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()