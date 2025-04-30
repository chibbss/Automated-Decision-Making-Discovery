from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, output_json
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

from tools.custom_tool import (
    CompanyResearchTool,
    PeopleFinderTool,
    EmailValidatorTool
)

class DecisionMakerDiscoveryReport(BaseModel):
    companies_discovered: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of companies discovered with their details."
    )
    decision_makers_found: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of decision makers with contact information."
    )
    verification_summary: Dict[str, int] = Field(
        default_factory=dict,
        description="Email verification statistics."
    )
    outreach_notes: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Personalized outreach strategies."
    )
    weekly_summary: Dict[str, int] = Field(
        default_factory=dict,
        description="Weekly processing metrics."
    )


@CrewBase
class DecisionMakerDiscovery():
    """Decision Maker Discovery Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'


    @agent
    def company_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['company_researcher'],
            tools=[CompanyResearchTool()],
            allow_delegation = False,
            verbose=True,
        )

    @agent
    def people_finder(self) -> Agent:
        return Agent(
            config=self.agents_config['people_finder'],
            tools=[PeopleFinderTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def data_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['data_validator'],
            tools=[EmailValidatorTool()],
            allow_delegation=False,
            verbose=True
        )

    @agent
    def outreach_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['outreach_strategist'],
            verbose=True
        )

    @task
    def research_company_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_company_task'],
            agent=self.company_researcher(),
        )

    @task
    def find_decision_makers_task(self) -> Task:
        return Task(
            config=self.tasks_config['find_decision_makers_task'],
            agent=self.people_finder(),
        )

    @task
    def validate_contacts_task(self) -> Task:
        return Task(
            config=self.tasks_config['validate_contacts_task'],
            agent=self.data_validator(),
        )

    @task
    def create_outreach_strategies_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_outreach_strategies_task'],
            agent=self.outreach_strategist(),
            output_json=DecisionMakerDiscoveryReport,

        )

    @crew
    def crew(self) -> Crew:
        """Creates the Decision Maker Discovery Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            full_output=True
        )