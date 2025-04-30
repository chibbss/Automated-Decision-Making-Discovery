# Automated-Decision-Making-Discovery

Agentic AI Challenge Submission: Decision Maker Discovery Automation
<img width="1335" alt="Screenshot 2025-04-30 at 12 03 12" src="https://github.com/user-attachments/assets/25c87063-6902-4c0a-8e67-11ae4b8a7627" />

💡 Project Title: Agentic Decision Maker Discovery Workflow
Objective:
Automate the discovery of decision makers (CEOs, Founders, CTOs, etc.) for a list of companies, and output enriched, validated leads with personalized outreach strategies.

⚖️ Tools Used:
• CrewAI: For agentic task breakdown and execution
• Make.com: For end-to-end orchestration and automation
• Google Sheets: For data input/output
• Hunter.io / Clearbit API: For domain and email verification (optional integrations)
• Phantombuster (optional): For decision maker scraping (if available)
• OpenAI GPT-4: For parsing responses and smart outreach generation

✅ High-Level Workflow:
1. Input Capture
• A Google Sheet is used to input company names manually or via a form.
2. Company Research (CrewAI Agent)
• Agent: company_researcher
• Task: research_company_task
• Description: Gathers industry, company size, location, and business focus.
• Output: Pushed into the company_profiles sheet.
3. Decision Maker Discovery (CrewAI Agent)
• Agent: built-in tool (or human-in-the-loop if Phantombuster/Apollo is unavailable)
• Task: find_decision_makers_task
• Description: Scrapes top decision makers (CEO, CTO, Founder, VP, etc.). Extracts LinkedIn, email pattern, etc.
• Output: Added to the decision_makers_raw sheet.
4. Contact Validation (CrewAI Agent)
• Agent: data_validator
• Task: validate_contacts_task
• Description: Verifies names, roles, LinkedIn, and confirms email via pattern or validation service (Hunter.io)
• Output: Sent to verified_leads sheet
5. Outreach Strategy Generation (CrewAI Agent)
• Agent: outreach_strategist
• Task: create_outreach_strategies_task
• Description: Uses company and role data to generate a custom hook, subject line, and tone.
• Output: Logged in the connection_requests and follow_up_messages sheets
6. Make.com Automation
• Scenario is built to:
• Trigger on new company names
• Call local GPT/CrewAI instance (via HTTP module)
• Route structured output into two sheets: outreach copy and verified leads
• (Optional) Verify emails with Hunter.io
• (Optional) Report via Gmail/Slack every Friday

⚠️ Known Bottlenecks
• Ngrok/Localhost CrewAI Instance: Running GPT-based CrewAI locally via ngrok may be unstable.
• Workaround: Replace with hosted CrewAI endpoint or integrate OpenAI via API key directly into Make.com scenario.
• Missing Apollo/Phantombuster:
• Some decision maker discovery fields were left blank if no automated scraper was integrated.
• Workaround: Use Clay, LinkedIn scraping, or manual population for testing.

🔄 Testing Instructions
If someone wants to test without setting up CrewAI + ngrok:
1. Copy the Google Sheet template
2. Replace HTTP call in Make.com with a custom webhook that returns mocked CrewAI responses.
3. Continue automation with real logic (parsing, Sheets, etc.)

🔢 Deliverables:
Google Sheets DB:
company_profiles
decision_makers_raw
verified_leads
connection_requests
follow_up_messages
Make.com Scenario Link: [Insert Link Here]
Make Scenario .json File: Included in GitHub repo
GitHub Repo: https://github.com/chibbss/Automated-Decision-Making-Discovery
Loom Walkthrough: [Insert Link Here]
Google Doc: This document

✨ Notes on Agentic Design
• CrewAI agents are modular and task-specific
• Each output is designed to feed the next agent in the pipeline
• Easily swappable to integrate OpenAI GPT endpoints instead of localhost

🌟 Future Enhancements
• Add deduplication logic in Google Sheets
• Integrate directly with Loubby CRM via API
• Add lead scoring and categorization via GPT

Built by: Emmanuel Ochiba
Location: Lagos,  Nigeria


