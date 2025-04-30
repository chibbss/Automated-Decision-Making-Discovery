from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import json
from crew import DecisionMakerDiscovery
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

# FastAPI app setup
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allowing all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input Model
class CompanyInput(BaseModel):
    company_names: List[str]

# Capture the app start time
start_time = datetime.utcnow()

@app.post("/find_decision_makers")
async def find_decision_makers(company_data: CompanyInput):
    try:
        # Log the received company data for debugging
        print(f"Received list of companies: {company_data}")

        # Create the DecisionMakerDiscovery crew
        decision_maker_crew = DecisionMakerDiscovery()

        # Convert input data to a dictionary
        raw_input = company_data.dict()  # Ensure input is in the correct format

        # Log the raw input
        print(f"Passing to crew: {raw_input}")

        # Pass the data to the crew's kickoff method
        raw_output = decision_maker_crew.crew().kickoff(inputs=raw_input)

        # Convert CrewOutput-like object to dict if needed
        if hasattr(raw_output, "dict"):
            raw_output = raw_output.dict()
        elif hasattr(raw_output, "to_dict"):
            raw_output = raw_output.to_dict()

        # Handle different response formats
        if isinstance(raw_output, dict):
            if 'json_dict' in raw_output:
                return JSONResponse(content=raw_output['json_dict'], status_code=200)
            elif 'raw' in raw_output:
                try:
                    parsed = json.loads(raw_output['raw'])
                    return JSONResponse(content=parsed, status_code=200)
                except json.JSONDecodeError:
                    return JSONResponse(content=raw_output, status_code=200)

        # Fallback: try to return raw_output anyway (last resort)
        return JSONResponse(content=raw_output, status_code=200)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", tags=["Health Check"])
def health_check():
    uptime: timedelta = datetime.utcnow() - start_time
    return JSONResponse(
        content={
            "status": "ok",
            "uptime": str(uptime)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)