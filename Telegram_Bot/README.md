Asset Request Bot (Telegram-Based Slot Filling System)
🧠 Project Title & Problem Statement
Project Title: Asset Request Bot using Telegram (Slot-Filling Conversational Agent)
Problem Statement:
Employees in an organization often request assets like laptops or software licenses through manual processes, which are slow and error-prone. This project solves this by building a Telegram-based chatbot that collects asset request details through step-by-step conversation (slot filling), validates employee data using a mock HRIS JSON, and automatically generates a structured ticket stored in a database.

👥 Team Members
Nikitha – Database Design and Logic
Ashwini – Developer and Documentation
Madhusudhan Reddy – Backend Development
Lalitha – Testing and Validation

🚀 Features Implemented
Telegram bot-based conversational interface
Slot-filling workflow (Employee ID → Asset Type → Asset Name → Reason)
HRIS validation using JSON file
Automatic ticket ID generation using UUID
Role-based approval logic (based on employee grade)
SQLite database storage for all requests
Structured JSON output for each request
Cancel conversation support

🏗️ Architecture Overview
User (Telegram Chat)
Sends messages to bot step-by-step
Telegram Bot (Python - python-telegram-bot)
Handles conversation flow using ConversationHandler
HRIS Layer (employees.json)
Validates Employee ID and fetches employee details
Business Logic Layer
Checks grade for approval rules
Generates ticket ID
Database Layer (SQLite)
Stores all asset requests
Response Layer
Sends confirmation + structured JSON back to user

🛠️ Tools & Technologies Used
Python 3
python-telegram-bot library
SQLite (Database)
JSON (Mock HRIS Data)
UUID (Ticket generation)
Telegram Bot API

⚙️ Setup Instructions
Install dependencies:
pip install python-telegram-bot
Create employees.json file and add HR data.
Add your bot token in the code:
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
Ensure SQLite database file will be created automatically:
requests.db

▶️ Run Instructions
Run the bot using:
python bot.py
Then open Telegram and start chatting with your bot using:
/start

📥 Sample Input & Output
▶️ Input Flow:
Employee ID → E101  
Asset Type → Laptop  
Asset Name → Dell Latitude  
Reason → For project development

📤 Output:
{
    "ticket_id": "TKT-8f3a91bc",
    "employee_id": "E101",
    "employee_name": "Rahul Sharma",
    "role": "Developer",
    "grade": "G5",
    "asset_type": "Laptop",
    "asset_name": "Dell Latitude",
    "reason": "For project development",
    "status": "Approved"
}

🤖 AI Capability Demonstrated
Slot-filling conversational AI flow
Context-aware data collection
Structured output generation (JSON)
Rule-based decision making (approval system)
Validation using external knowledge base (HRIS JSON)

⚠️ Assumptions & Limitations
Assumptions:
Employee data is preloaded in JSON format
Grades G4–G7 are auto-approved

Limitations:
No real authentication system
Single database (SQLite) used
No admin dashboard for approvals
Bot works only on Telegram platform

🎥 Demo Video Link
https://drive.google.com/file/d/1aNvtHAa4lr4HDnCq0pHgVvjjCQBQgwNr/view?usp=sharing
