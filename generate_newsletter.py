import openai
import os

# Set up OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def chatgpt_prompt(prompt):
    """Function to generate content using ChatGPT"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Generate daily content
news_summary = chatgpt_prompt("Give me a brief summary of today's most important news in bullet points.")
mental_model = chatgpt_prompt("Explain a useful mental model in one paragraph.")
interesting_fact = chatgpt_prompt("Give me a short and fascinating fact.")
quote_of_the_day = chatgpt_prompt("Give me an inspiring quote from a famous philosopher or leader.")
wellness_tip = chatgpt_prompt("Give me one simple science-backed well-being tip.")
life_pro_tip = chatgpt_prompt("Give me one practical life hack.")
brain_teaser = chatgpt_prompt("Give me a fun brain teaser with an answer.")

# Format as HTML
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
    <h2>🌍 News Summary:</h2>
    <p>{news_summary}</p>
    <h2>🧠 Mental Model:</h2>
    <p>{mental_model}</p>
    <h2>📖 Interesting Fact:</h2>
    <p>{interesting_fact}</p>
    <h2>💡 Quote of the Day:</h2>
    <p>{quote_of_the_day}</p>
    <h2>😊 Well-being Tip:</h2>
    <p>{wellness_tip}</p>
    <h2>💪 Life Tip:</h2>
    <p>{life_pro_tip}</p>
    <h2>🧩 Brain Teaser:</h2>
    <p>{brain_teaser}</p>
    <footer>Updated daily via ChatGPT AI 🚀</footer>
</body>
</html>
"""

# Save as index.html
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file generated successfully!")