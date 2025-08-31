**AI Cybersecurity News Agent 🤖📰**
An intelligent Python agent that automatically fetches, summarizes, and emails daily cybersecurity news using RSS feeds and OpenAI's GPT-4o-mini.

**✨ Features**
**Automated News Fetching:** Gathers the latest cybersecurity articles from a configurable list of RSS feeds (e.g., KrebsOnSecurity, BleepingComputer, Threatpost).

**Intelligent Summarization:** Leverages OpenAI's powerful gpt-4o-mini model to provide concise, focused summaries of each article, highlighting key threats, vulnerabilities, and developments.

**Full Text Extraction:** Attempts to extract the full content of articles from their URLs for more comprehensive summarization, with fallback to RSS summaries if full text isn't available.

**Keyword Filtering:** Filters articles based on a predefined list of cybersecurity-related keywords to ensure relevance.

**Daily Email Digests:** Compiles the summarized articles into a well-formatted HTML email and sends it to your specified recipient daily.

**Scheduled Execution:** Runs automatically at a set time each day, keeping you updated without manual intervention.

**Easy Configuration:** All sensitive information (API keys, emails) is managed securely via environment variables (.env file).

**🚀 How It Works**
**RSS Feed Parsing:** The agent first fetches the latest entries from configured RSS feeds.

**Keyword Filtering:** It filters these entries, keeping only those whose titles or summaries contain relevant cybersecurity keywords.

**Full Text Retrieval:** For each relevant article, it attempts to visit the original URL and extract the full article text using BeautifulSoup4. A User-Agent header is used to mimic a browser, helping bypass basic bot detection.

**AI Summarization:** The extracted (or fallback) text is then sent to OpenAI's gpt-4o-mini model, which generates a concise summary focusing on cybersecurity aspects.

**Email Compilation:** All summarized articles are formatted into a clean, readable HTML email.

**Email Delivery:** The compiled email is sent to your designated recipient via SMTP.

**Scheduling:** After the initial run, the agent enters a loop, checking every second for the next scheduled run (e.g., daily at 9:00 AM local time).

**🛠️ Setup and Installation**
Follow these steps to get your AI Cybersecurity News Agent up and running on your local machine.

**Prerequisites**
**Python 3.10+ (Recommended:** Use the latest Python 3.x version)

**OpenAI API Key:** Obtain one from OpenAI.

**Gmail Account (or other SMTP-compatible email service):** If using Gmail, you'll need to generate a Google App Password as standard password login is often blocked for security.

**Generate App Password for Gmail:**

Go to your Google Account settings.

Navigate to "Security" -> "How you sign in to Google" -> "2-Step Verification" (ensure it's ON).

Scroll down to "App passwords" and click it.

Select "Mail" as the app and "Other (Custom name)" for the device. Give it a name like "CyberNewsAgent" and click "Generate."

Copy the generated 16-character password (this is your SENDER_PASSWORD).

**Step-by-Step Installation**
**Clone the Repository:**
Open your PowerShell (or Git Bash/Terminal) and clone this repository to your desired location:

git clone https://github.com/your-username/ai-cybersecurity-news-agent.git
cd ai-cybersecurity-news-agent

(Replace your-username with your actual GitHub username and ai-cybersecurity-news-agent if you used a different repository name).

**Create a Virtual Environment:**
It's best practice to install dependencies in a virtual environment to avoid conflicts with other Python projects.

python -m venv venv

**Activate the Virtual Environment:**

**On Windows (PowerShell):**

.\venv\Scripts\Activate.ps1

**On macOS/Linux (Bash/Zsh):**

source venv/bin/activate

Your prompt should now show (venv) at the beginning, indicating the virtual environment is active.

**Install Dependencies:**
**First, generate the requirements.txt file from your active virtual environment, then install from it:**

pip freeze > requirements.txt
pip install -r requirements.txt

After generating and installing, remember to commit requirements.txt to your GitHub repository.

**Configure Environment Variables (.env file):**
Create a new file named .env in the root of your ai-cybersecurity-news-agent directory (where agent.py is located).
**Add the following lines to this .env file, replacing the placeholder values with your actual credentials:**

SENDER_EMAIL=your_sending_email@gmail.com
SENDER_PASSWORD=your_gmail_app_password # Use the generated App Password, NOT your regular Gmail password
RECIPIENT_EMAIL=your_receiving_email@example.com
OPENAI_API_KEY=your_openai_api_key_here

Important: The .env file is intentionally excluded from version control by .gitignore for security reasons. Never commit your .env file to GitHub!

**Adjust PowerShell Execution Policy (Windows Only, if needed):**
If you encounter an error like "cannot be loaded because running scripts is disabled on this system," you might need to change your PowerShell Execution Policy.

Open PowerShell as Administrator.

**Run:**

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

Type Y and press Enter when prompted.

Close the Administrator PowerShell and return to your regular PowerShell window.

🏃 Usage
Once all setup steps are complete, you can run your AI agent.

Ensure your virtual environment is active ((venv) in your prompt) and you are in the ai-cybersecurity-news-agent directory.

**Run the script:**

python agent.py

**What to Expect:**

**The script will perform an immediate run upon execution:**

It will print status messages to your console (fetching, processing, errors, email sent).

You should receive an email digest of the latest cybersecurity news.

After the initial run, the script will enter a scheduling loop, and you will see a message indicating the next scheduled run time (e.g., Initial run complete. Scheduling agent to run daily at 09:00 (your local time)...).

The PowerShell window (or terminal) must remain open for the agent to run at its scheduled time daily. If you close the window, the script will stop, and you'll need to restart it.

Restarting the Agent
If you close the PowerShell window or your computer restarts, simply follow these steps to bring the agent back online:

Open a new PowerShell window.

cd C:\dev\cybersecurity_news_agent

.\venv\Scripts\Activate.ps1

python agent.py

**⚙️ Customization**
**You can easily customize the agent's behavior by modifying the agent.py file:**

**RSS Feeds (RSS_FEEDS):** Add or remove URLs of cybersecurity RSS feeds to tailor your news sources.

**Keywords (NEWS_KEYWORDS):** Adjust the list of keywords to fine-tune what articles are considered "relevant."

**Summary Length (SUMMARY_LENGTH):** Control the maximum token length of the AI-generated summaries.

**Schedule Time (SCHEDULE_TIME):** Change the time (e.g., "14:30" for 2:30 PM) when the daily email is sent. This time is relative to your local system's timezone.

**AI Model (model="gpt-4o-mini"):** While gpt-4o-mini is efficient and cost-effective, you can experiment with other OpenAI models if desired (e.g., gpt-3.5-turbo, gpt-4o), but be mindful of costs and rate limits.

**⚠️ Troubleshooting**
**403 Client Error:** Forbidden during text fetching: This usually means the website is blocking automated requests. The current code includes a User-Agent header to help mitigate this. If it persists for specific sites, they might have more advanced bot detection.

**Failed to send email:**

Double-check SENDER_EMAIL, SENDER_PASSWORD (ensure it's an App Password for Gmail), and RECIPIENT_EMAIL in your .env file.

Ensure your sending email account allows "less secure app access" (though Google App Passwords bypass this).

Verify your internet connection.

OPENAI_API_KEY not set: Make sure your OPENAI_API_KEY is correctly defined in the .env file and that there are no leading/trailing spaces.

**No email received / No relevant articles found:**

Check your spam folder.

Verify your RSS_FEEDS are correct and active.

Review your NEWS_KEYWORDS – they might be too restrictive, or there might genuinely be no relevant news in the past 24 hours.

**🤝 Contributing**
Feel free to fork this repository, open issues, and submit pull requests if you have suggestions for improvements, bug fixes, or new features!

**📄 License**
This project is licensed under the MIT License - see the LICENSE file for details.
