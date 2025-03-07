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
    <style>
        body {{
            font-family: 'Helvetica', sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1, h2 {{
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        footer {{
            text-align: center;
            padding: 20px;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>🌞 Your Daily Smart Newsletter</h1>
    
    <div class="section">
        <h2>🌍 News Summary:</h2>
        <p>{news_summary}</p>
    </div>
    
    <div class="section">
        <h2>🧠 Mental Model:</h2>
        <p>{mental_model}</p>
    </div>
    
    <div class="section">
        <h2>📖 Interesting Fact:</h2>
        <p>{interesting_fact}</p>
    </div>
    
    <div class="section">
        <h2>💡 Quote of the Day:</h2>
        <p>{quote_of_the_day}</p>
    </div>
    
    <div class="section">
        <h2>😊 Well-being Tip:</h2>
        <p>{wellness_tip}</p>
    </div>
    
    <div class="section">
        <h2>💪 Life Tip:</h2>
        <p>{life_pro_tip}</p>
    </div>
    
    <div class="section">
        <h2>🧩 Brain Teaser:</h2>
        <p>{brain_teaser}</p>
    </div>
    
    <footer>Updated daily via ChatGPT AI 🚀</footer>
</body>
</html>
"""

# Save as index.html
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("HTML file generated successfully!")