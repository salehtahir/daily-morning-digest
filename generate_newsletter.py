import requests
import feedparser
import random

# Fetch news (Google RSS)
def get_news():
    rss_url = "https://news.google.com/rss"
    feed = feedparser.parse(rss_url)
    return "".join(f"<li>{entry.title}</li>" for entry in feed.entries[:3])

# Fetch a random Wikipedia fact
def get_wikipedia_summary():
    url = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
    response = requests.get(url).json()
    return response.get("extract", "No fact available today.")

# Random thought
def get_quote():
    quotes = [
        "The best way to predict the future is to create it.",
        "Do what you can, with what you have, where you are."
    ]
    return random.choice(quotes)

# Generate HTML content
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Smart Newsletter</title>
</head>
<body>
    <h1>🌞 Your Daily Smart Newsletter</h1>
    <h2>🌍 News:</h2>
    <ul>{get_news()}</ul>
    <h2>📖 Interesting Fact:</h2>
    <p>{get_wikipedia_summary()}</p>
    <h2>💡 Thought of the Day:</h2>
    <p>{get_quote()}</p>
    <footer>Updated daily via automation 🚀</footer>
</body>
</html>
"""

# Save as index.html
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file generated successfully!")