import feedparser
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

# Load environment variables from .env file
load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# --- Configuration ---
RSS_FEEDS = [
    "https://krebsonsecurity.com/feed/",
    "https://www.bleepingcomputer.com/feed/",
    "https://threatpost.com/feed/",
    "https://www.schneier.com/blog/atom.xml",
    # Add more cybersecurity RSS feeds here
]
NEWS_KEYWORDS = ["cybersecurity", "cyber attack", "data breach", "ransomware", "phishing",
                 "malware", "vulnerability", "exploit", "zero-day", "security breach",
                 "cybercrime", "hack", "threat actor", "APT", "MFA", "patch", "AI security"]
SUMMARY_LENGTH = 150 # Max tokens for AI summary
# For scheduling, 09:00 refers to 9 AM in your local system's timezone.
SCHEDULE_TIME = "09:00" # E.g., "09:00" for 9:00 AM, "14:30" for 2:30 PM

# --- AI Integration ---
def summarize_text_with_ai(text):
    if not OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY not set. AI summarization skipped.")
        return f"AI summarization skipped (API key not set). Original text (first 200 chars): {text[:200]}..."

    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Using the recommended gpt-4o-mini model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity news summarizer. Provide a concise summary of the given text, focusing on key threats, vulnerabilities, and significant developments. Keep it to around 100-150 words."},
                {"role": "user", "content": f"Summarize the following cybersecurity article:\n\n{text}"}
            ],
            max_tokens=SUMMARY_LENGTH,
            temperature=0.7 # Adjust for creativity vs. focus (0.0-1.0)
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing with AI: {e}")
        return f"AI summarization failed. Original text (first 200 chars): {text[:200]}..."

# --- News Fetching and Filtering ---
def fetch_news():
    all_articles = []
    print("Fetching news from RSS feeds...")
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = entry.title if hasattr(entry, 'title') else 'No Title'
                link = entry.link.strip() if hasattr(entry, 'link') else '#' # Ensure link is stripped
                summary = entry.summary if hasattr(entry, 'summary') else ''
                published = entry.published if hasattr(entry, 'published') else 'No Date'

                # Basic keyword filtering for relevance
                if any(keyword.lower() in title.lower() or keyword.lower() in summary.lower() for keyword in NEWS_KEYWORDS):
                    all_articles.append({
                        'title': title,
                        'link': link,
                        'summary': summary, # This is the raw summary, will be AI summarized later
                        'published': published
                    })
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}")
    print(f"Found {len(all_articles)} potentially relevant articles.")
    return all_articles

def extract_full_text(url):
    # Define a common User-Agent string to mimic a web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    try:
        # Pass the headers to the requests.get() call
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to find common content containers
        paragraphs = soup.find_all(['p', 'div', 'article', 'main'])
        full_text = ' '.join([p.get_text() for p in paragraphs if p.get_text()])

        # Simple cleanup
        full_text = ' '.join(full_text.split()) # Remove extra whitespace
        return full_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching full text from {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing HTML from {url}: {e}")
        return None

# --- Email Sending ---
def send_email(subject, body, recipient_email):
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        print("Email credentials (SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL) not fully set. Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    try:
        # For Gmail, use 'smtp.gmail.com' and port 587
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() # Enable TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        print(f"Email sent successfully to {recipient_email}!")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print("Please check your SENDER_EMAIL, SENDER_PASSWORD (App Password for Gmail!), and RECIPIENT_EMAIL in the .env file.")
        print("Ensure less secure app access is off for your Gmail, and 2FA with an App Password is used.")

# --- Main Agent Logic ---
def run_cybersecurity_agent():
    print("Running cybersecurity news agent...")
    news_articles = fetch_news()

    if not news_articles:
        print("No new articles found or an error occurred during fetching. Skipping email.")
        return

    processed_articles = []
    for article in news_articles:
        print(f"Processing: {article['title']}")
        full_article_text = extract_full_text(article['link'])
        
        # Use a fallback if full text extraction fails
        text_to_summarize = full_article_text if full_article_text else article['summary']

        summary = summarize_text_with_ai(text_to_summarize)
        
        # Simple keyword extraction (can be improved with NLTK/SpaCy for robustness)
        # Using a set for keywords from summary to avoid duplicates and ensure relevance
        found_keywords = {kw for kw in NEWS_KEYWORDS if kw.lower() in summary.lower()}
        
        processed_articles.append({
            'title': article['title'],
            'link': article['link'],
            'summary': summary,
            'keywords': list(found_keywords) if found_keywords else ['General Cybersecurity'], # Convert set to list
            'published': article['published']
        })
        # Optional: Add a small delay between AI calls to avoid hitting rate limits too fast
        # time.sleep(0.5)

    email_body_html = f"""
    <html>
    <head></head>
    <body>
        <h2>Latest Cybersecurity News Updates ({time.strftime('%Y-%m-%d %H:%M ADT', time.localtime())})</h2>
        <p>Here's a digest of the latest in the cybersecurity industry:</p>
        <ul>
    """

    for article in processed_articles:
        email_body_html += f"""
            <li>
                <h3><a href="{article['link']}">{article['title']}</a></h3>
                <p><strong>Summary:</strong> {article['summary']}</p>
                <p><strong>Keywords:</strong> {', '.join(article['keywords'])}</p>
                <p><small>Published: {article['published']}</small></p>
            </li>
            <hr>
        """

    email_body_html += """
        </ul>
        <p>Stay secure!</p>
        <p>This email was generated by your Cybersecurity News AI Agent.</p>
    </body>
    </html>
    """

    send_email("Your Daily Cybersecurity News Digest", email_body_html, RECIPIENT_EMAIL)
    print("Cybersecurity news agent run complete.")

# --- Scheduling ---
if __name__ == "__main__":
    # Perform an initial run when the script starts
    run_cybersecurity_agent()
    print(f"Initial run complete. Scheduling agent to run daily at {SCHEDULE_TIME} (your local time)...")

    # Schedule subsequent runs
    schedule.every().day.at(SCHEDULE_TIME).do(run_cybersecurity_agent)

    while True:
        schedule.run_pending()
        time.sleep(1) # Wait 1 second before checking for pending jobs