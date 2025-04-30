import requests
import os
from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import re

load_dotenv()  # Load API keys from .env

# ----------------------
# TOOL 1: Clearbit Company Enrichment
# ----------------------

class CompanyResearchInput(BaseModel):
    company_name: str = Field(..., description="Company name to enrich.")

class CompanyResearchTool(BaseTool):
    name: str = "Company Research Tool"
    description: str = "Find domain, industry, size, and location using Apollo."
    args_schema: Type[BaseModel] = CompanyResearchInput

    def _run(self, company_name: str) -> dict:
        apollo_key = os.getenv("APOLLO_API_KEY")
        url = f"https://api.apollo.io/v1/companies/search"
        headers = {"Authorization": f"Bearer {apollo_key}"}

        payload = {
            "q": company_name,
            "page": 1,
            "per_page": 1
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return {"error": f"Apollo failed: {response.status_code}"}

        data = response.json()
        company_data = data.get("companies", [{}])[0]

        return {
            "company_name": company_data.get("name"),
            "domain": company_data.get("domain"),
            "industry": company_data.get("industry"),
            "location": company_data.get("location"),
            "size": company_data.get("employee_count"),
        }


# ----------------------
# TOOL 2: Enhanced Apollo.io Decision Maker Discovery
# ----------------------

from typing import List, Type
from pydantic import BaseModel, Field

import os
import requests

class PeopleFinderInput(BaseModel):
    domain: str
    target_roles: List[str]
    company_id: str = Field(None, description="Apollo company ID (optional)")
    job_seniorities: List[str] = Field(default_factory=lambda: ["Executive", "Director", "VP"])
    departments: List[str] = Field(default_factory=list)

class PeopleFinderTool(BaseTool):
    name: str = "Enhanced People Finder Tool"
    description: str = "Use Apollo.io API to find decision makers with expanded role criteria."
    args_schema: Type[BaseModel] = PeopleFinderInput

    def _run(
        self,
        domain: str,
        target_roles: List[str],
        company_id: str = None,
        job_seniorities: List[str] = None,
        departments: List[str] = None
    ) -> List[dict]:
        apollo_key = os.getenv("APOLLO_API_KEY")
        headers = {"Authorization": f"Bearer {apollo_key}"}
        leads = []
        seen = set()

        payload = {
            "q_organization_domains": domain,
            "person_titles": target_roles,
            "page": 1,
            "per_page": 10,
        }

        if company_id:
            payload["organization_ids"] = [company_id]
        if job_seniorities:
            payload["job_seniorities"] = job_seniorities
        if departments:
            payload["departments"] = departments

        response = requests.post("https://api.apollo.io/v1/mixed_people/search", headers=headers, json=payload)

        if response.status_code != 200:
            print(f"[ERROR] Apollo API call failed: {response.status_code} - {response.text}")
            return leads

        data = response.json()
        for person in data.get("people", []):
            identifier = person.get("email") or person.get("linkedin_url")
            if not identifier or identifier in seen:
                continue
            seen.add(identifier)

            if not self._is_decision_maker(person.get("title", "").lower()):
                continue

            leads.append({
                "name": f"{person.get('first_name')} {person.get('last_name')}",
                "title": person.get("title"),
                "email": person.get("email"),
                "linkedin_url": person.get("linkedin_url"),
                "location": person.get("city"),
                "company_domain": domain
            })

        return leads

    def _get_target_roles(self, company_name: str, industry: str) -> List[str]:
        base_roles = [
            "ceo", "chief executive officer",
            "cto", "chief technology officer",
            "vp engineering", "vice president engineering",
            "director engineering",
            "head of product", "vp product", "director product",
            "vp sales", "director sales",
            "vp marketing", "director marketing"
        ]

        if "tech" in industry.lower():
            base_roles.extend([
                "vp platform", "director platform",
                "vp infrastructure", "director infrastructure"
            ])

        if any(name.lower() in company_name.lower() for name in ["Google", "Stripe", "Airtable"]):
            base_roles.extend([
                "engineering manager",
                "group product manager",
                "senior staff engineer"
            ])

        return base_roles

    def _is_decision_maker(self, title: str) -> bool:
        decision_maker_keywords = [
            "ceo", "cto", "cpo", "cmo", "cio",
            "vp", "vice president",
            "director", "head of",
            "manager", "lead", "principal"
        ]
        return any(keyword in title for keyword in decision_maker_keywords)

# ----------------------
# TOOL 3: Hunter Email Verifier
# ----------------------

class EmailValidatorInput(BaseModel):
    email: str = Field(..., description="Email to validate.")

class EmailValidatorTool(BaseTool):
    name: str = "Email Validator Tool"
    description: str = "Validate emails using Apollo API."
    args_schema: Type[BaseModel] = EmailValidatorInput

    def _run(self, email: str) -> str:
        apollo_key = os.getenv("APOLLO_API_KEY")
        url = f"https://api.apollo.io/v1/email-verification"

        payload = {
            "email": email
        }

        headers = {"Authorization": f"Bearer {apollo_key}"}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            return "Verification failed"

        data = response.json()
        return data.get("result", "unknown")