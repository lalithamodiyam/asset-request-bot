import json
import sqlite3
import uuid

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ====== PASTE YOUR BOT TOKEN HERE ======
TOKEN = "8915476909:AAEgFutBC3mcxOACaYdNJI1mRuCPuuiX88M"

# ====== Conversation States ======p
EMPLOYEE_ID, ASSET_TYPE, ASSET_NAME, REASON = range(4)

# ====== Load HRIS JSON ======
with open("employees.json", "r") as file:
    employees = json.load(file)

# ====== SQLite Database ======
conn = sqlite3.connect("requests.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests (
    ticket_id TEXT,
    employee_id TEXT,
    employee_name TEXT,
    role TEXT,
    grade TEXT,
    asset_type TEXT,
    asset_name TEXT,
    reason TEXT,
    status TEXT
)
""")

conn.commit()

# ====== Start Command ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Asset Request Bot\n\nEnter Employee ID:"
    )
    return EMPLOYEE_ID

# ====== Employee ID ======
async def employee_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emp_id = update.message.text.strip()

    if emp_id not in employees:
        await update.message.reply_text(
            "❌ Invalid Employee ID.\nTry again:"
        )
        return EMPLOYEE_ID

    context.user_data["employee_id"] = emp_id
    context.user_data["employee"] = employees[emp_id]

    await update.message.reply_text(
        "💻 Enter Asset Type (Laptop / Software License):"
    )

    return ASSET_TYPE

# ====== Asset Type ======
async def asset_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["asset_type"] = update.message.text

    await update.message.reply_text(
        "📝 Enter Asset Name:"
    )

    return ASSET_NAME

# ====== Asset Name ======
async def asset_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["asset_name"] = update.message.text

    await update.message.reply_text(
        "📌 Enter Reason for Request:"
    )

    return REASON

# ====== Reason ======
async def reason(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["reason"] = update.message.text

    emp = context.user_data["employee"]

    ticket_id = "TKT-" + str(uuid.uuid4())[:8]

    if emp["grade"] in ["G4", "G5", "G6", "G7"]:
        status = "Approved"
    else:
        status = "Pending"

    request_json = {
        "ticket_id": ticket_id,
        "employee_id": context.user_data["employee_id"],
        "employee_name": emp["name"],
        "role": emp["role"],
        "grade": emp["grade"],
        "asset_type": context.user_data["asset_type"],
        "asset_name": context.user_data["asset_name"],
        "reason": context.user_data["reason"],
        "status": status
    }

    cursor.execute("""
    INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        ticket_id,
        context.user_data["employee_id"],
        emp["name"],
        emp["role"],
        emp["grade"],
        context.user_data["asset_type"],
        context.user_data["asset_name"],
        context.user_data["reason"],
        status
    ))

    conn.commit()

    await update.message.reply_text(
        f"✅ Request Submitted Successfully\n\n"
        f"Ticket ID: {ticket_id}\n"
        f"Status: {status}\n\n"
        f"{json.dumps(request_json, indent=2)}"
    )

    return ConversationHandler.END

# ====== Cancel ======
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Request Cancelled.")
    return ConversationHandler.END

# ====== Main ======
def main():

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMPLOYEE_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, employee_id)
            ],
            ASSET_TYPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, asset_type)
            ],
            ASSET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, asset_name)
            ],
            REASON: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, reason)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot Running...")

    app.run_polling()

if __name__ == "__main__":
    main()