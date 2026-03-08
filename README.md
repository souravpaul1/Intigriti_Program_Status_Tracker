# Intigriti Program Status Tracker

Sometimes I have multiple bugs ready to submit for a program, but the program is in **Suspended** status. Manually checking the program page again and again to see when it reopens is inefficient.

To solve this problem, I created a small **Telegram bot** that monitors program status and sends an alert when the program becomes **Open** or **Suspended**.

At the moment, the script only tracks **Open** and **Suspended** states and does not handle other statuses. (**Keep this limitation in mind**)

---

# Requirements

To run this script you need:

- A computer (**VPS recommended for 24/7 monitoring**)
- A **Telegram bot**
- Your **Intigriti Researcher API token**

---

# Setup

### 1. Create a Telegram Bot

Create a Telegram bot using **@BotFather** and obtain your **Bot Token**.

You will also need your **Chat ID** so the bot knows where to send notifications.

---

### 2. Configure `config.json`

Save the following information in `config.json`:

- Telegram **Bot Token**
- Telegram **Chat ID**
- Your **Intigriti Researcher API Token**

Example structure:
```
{
    "intigriti_api_key": "YOUR_INTIGRITI_API_KEY",
    "telegram_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID",
    "check_interval": 1
}
```
---

### 3. Add Programs to Track

Add the **UUIDs of the programs** you want to track in `programs.json`.

Example:
```
{
  "programs": [
    "program-uuid-1",
    "program-uuid-2",
    "program-uuid-3"
  ]
}
```
You can find the UUID of a program from the Intigriti API endpoint.

---

### ⚠️ Important Note About Rate Limits

This script is **not designed to track a large number of programs**.

It is recommended to track **only a few programs (around 5–6)**.  
Tracking too many programs may cause you to hit the **Intigriti API rate limits**.

---

# Running the Script

Once everything is configured:
```
python3 tracker.py
```

For continuous monitoring, it is recommended to run the script on a **VPS**.

The bot will automatically send a **Telegram alert** whenever a program status changes between:

- **Open**
- **Suspended**

---

# Why This Exists

This tool was built to avoid constantly checking program pages when you already have bugs ready to submit and are waiting for the program to reopen.

Now you can just wait for the **Telegram alert** instead.
