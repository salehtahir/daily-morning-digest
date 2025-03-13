import openai
import os
import time
from datetime import datetime
import pytz
import json
import random
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def chatgpt_prompt(prompt, category, max_retries=3, delay=2):
    """Enhanced ChatGPT prompt function with date awareness"""
    today = datetime.now().strftime("%B %d, %Y")
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                print(f"Waiting {delay * attempt} seconds before retry...")
                time.sleep(delay * attempt)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are generating unique content for {category} on {today}. Never repeat content from previous days."},
                    {"role": "user", "content": f"For {today}: {prompt}"}
                ],
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit reached. Attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    return "Content temporarily unavailable due to rate limits."
            else:
                print(f"Error: {e}")
                return "Content temporarily unavailable."

def get_news_headlines():
    """Fetch current general world news headlines using ChatGPT"""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""Provide the 5 most significant general world news headlines from {today}.
        
        For each news item, provide:
        HEADLINE: [Clear, impactful headline]
        SOURCE: [Name of the news source, e.g., Reuters, AP, BBC, etc.]
        DATE: [Publication date in MM/DD/YYYY format]
        SUMMARY: [A detailed 4-5 sentence summary covering:
        - What happened (key events)
        - When it happened (specific timing)
        - Who is involved
        - Why it's significant
        - What are the implications]

        Prioritize these categories:
        1. Breaking news and urgent developments
        2. Major political events and decisions
        3. High-impact global events
        4. Critical economic developments
        5. Significant social and cultural events
        6. Natural disasters and environmental news

        Format each news item exactly as shown above with HEADLINE:, SOURCE:, DATE:, and SUMMARY:
        Separate each news item with three hyphens (---)"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a senior news curator for {today}. Focus on verified, significant world developments with real impact. Include accurate source information and publication dates. Never repeat news from previous days."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        # Parse the response into news items
        news_text = response.choices[0].message.content
        news_items = news_text.split('---')
        
        formatted_news = ""
        for item in news_items:
            if not item.strip():
                continue
                
            # Extract headline, source, date and summary
            headline_parts = item.split('HEADLINE:', 1)
            if len(headline_parts) > 1:
                headline_text = headline_parts[1].split('SOURCE:', 1)[0].strip()
                
                # Extract source
                source_text = ""
                if 'SOURCE:' in item:
                    source_parts = item.split('SOURCE:', 1)[1]
                    if 'DATE:' in source_parts:
                        source_text = source_parts.split('DATE:', 1)[0].strip()
                
                # Extract date
                date_text = ""
                if 'DATE:' in item:
                    date_parts = item.split('DATE:', 1)[1]
                    if 'SUMMARY:' in date_parts:
                        date_text = date_parts.split('SUMMARY:', 1)[0].strip()
                
                # Extract summary
                summary_text = item.split('SUMMARY:', 1)[1].strip() if 'SUMMARY:' in item else ""
                
                # Format as HTML
                formatted_news += f"""
                <div class="news-item">
                    <h3 class="news-headline">{headline_text}</h3>
                    <div class="news-metadata">
                        <span class="news-source">Source: {source_text}</span>
                        <span class="news-date">Published: {date_text}</span>
                    </div>
                    <p class="news-summary">{summary_text}</p>
                </div>
                """
        
        return formatted_news
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "Unable to fetch news headlines at this time."

def get_breakthrough_news():
    """Fetch breakthrough news in technology, AI, and significant medical advances"""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""Provide the 3 most significant breakthrough news from {today} with a strong focus on technology and AI.
        
        For each breakthrough, provide:
        HEADLINE: [Clear, impactful headline about the breakthrough]
        SOURCE: [Name of the news source, e.g., TechCrunch, Nature, MIT Technology Review, etc.]
        DATE: [Publication date in MM/DD/YYYY format]
        SUMMARY: [A detailed 4-5 sentence summary covering:
        - What the breakthrough is
        - Who made it (researchers, company, etc.)
        - Why it's significant
        - Practical real-world applications
        - Potential industry impact]

        Prioritize these categories in this exact order:
        1. Artificial Intelligence advances and applications
        2. Technology developments and innovations
        3. Startup/Business tech innovations
        4. Medical/Healthcare breakthroughs (ONLY if truly revolutionary or game-changing)

        At least 2 of the 3 items MUST be about AI or technology. Include medical breakthroughs only if they represent a major leap forward or paradigm shift in healthcare.

        For each breakthrough, include:
        - Practical real-world applications
        - Market impact and business implications
        - Timeline for implementation when available
        - Expert opinions if relevant

        Format each breakthrough exactly as shown above with HEADLINE:, SOURCE:, DATE:, and SUMMARY:
        Separate each item with three hyphens (---)"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a technology and AI news curator for {today}. Strongly prioritize AI and technology news over other categories. Only include medical breakthroughs if they are truly revolutionary. Focus on verified, significant breakthroughs with real-world impact. Include accurate source information and publication dates. Never repeat news from previous days."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800
        )
        
        # Parse the response into news items
        news_text = response.choices[0].message.content
        news_items = news_text.split('---')
        
        formatted_news = ""
        for item in news_items:
            if not item.strip():
                continue
                
            # Extract headline, source, date and summary
            headline_parts = item.split('HEADLINE:', 1)
            if len(headline_parts) > 1:
                headline_text = headline_parts[1].split('SOURCE:', 1)[0].strip()
                
                # Extract source
                source_text = ""
                if 'SOURCE:' in item:
                    source_parts = item.split('SOURCE:', 1)[1]
                    if 'DATE:' in source_parts:
                        source_text = source_parts.split('DATE:', 1)[0].strip()
                
                # Extract date
                date_text = ""
                if 'DATE:' in item:
                    date_parts = item.split('DATE:', 1)[1]
                    if 'SUMMARY:' in date_parts:
                        date_text = date_parts.split('SUMMARY:', 1)[0].strip()
                
                # Extract summary
                summary_text = item.split('SUMMARY:', 1)[1].strip() if 'SUMMARY:' in item else ""
                
                # Format as HTML
                formatted_news += f"""
                <div class="breakthrough-item">
                    <h3 class="breakthrough-headline">{headline_text}</h3>
                    <div class="news-metadata">
                        <span class="news-source">Source: {source_text}</span>
                        <span class="news-date">Published: {date_text}</span>
                    </div>
                    <p class="breakthrough-summary">{summary_text}</p>
                </div>
                """
        
        return formatted_news
    except Exception as e:
        print(f"Error fetching breakthrough news: {e}")
        return "Unable to fetch breakthrough news at this time."

def get_philosophical_insight():
    """Get a thought-provoking philosophical concept or insight"""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""For {today}'s philosophical insight, share a different concept than previous days.
        Choose randomly from these categories:
        1. Ancient Philosophy (Greek, Eastern, etc.)
        2. Modern Philosophy
        3. Ethical Dilemmas
        4. Existential Questions
        5. Metaphysics
        6. Epistemology
        7. Philosophy of Mind
        8. Social Philosophy
        
        Format as:
        [CONCEPT NAME OR QUESTION]
        
        [3-4 sentences explaining the concept and its implications]
        
        Think About: [One thought-provoking question for personal reflection]"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a philosophical thinker sharing today's ({today}) insight. Never repeat content from previous days."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching philosophical insight: {e}")
        return "Unable to generate philosophical insight at this time."

def get_wellbeing_tip():
    """Get daily affirmation and positive psychology tip"""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""For {today}'s well-being tip, provide both:

        1. A powerful one-line daily affirmation that:
        - Is present-tense and positive
        - Feels personal and actionable
        - Promotes emotional well-being
        - Is simple to remember and repeat

        2. A science-backed positive psychology tip that:
        - Can be implemented in 2-5 minutes
        - Is based on research findings
        - Includes brief explanation of why it works
        - Has a practical, immediate application
        - Mentions the research/study source briefly

        Format as:
        Today's Affirmation:
        [One-line powerful affirmation]

        Quick Well-being Boost:
        [Concise, science-backed tip with brief explanation of benefits]"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a positive psychology expert creating well-being content for {today}. Focus on practical, science-based strategies that can be implemented immediately. Never repeat tips from previous days."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching well-being tip: {e}")
        return "Unable to generate well-being tip at this time."

def get_quote_of_day():
    """Get an inspiring quote from any notable figure"""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""For {today}'s quote, share an inspiring or thought-provoking quote from any of these categories:

        1. Historical Figures
        - Leaders and changemakers
        - Scientists and innovators
        - Artists and writers

        2. Modern Thought Leaders
        - Entrepreneurs and business leaders
        - Tech innovators
        - Contemporary thinkers

        3. Cultural Icons
        - Artists and musicians
        - Writers and poets
        - Filmmakers and creators

        4. Contemporary Voices
        - Modern philosophers
        - Industry leaders
        - Social innovators

        The quote should:
        - Be powerful and meaningful
        - Include the speaker's name and brief context
        - Be relevant to modern life
        - Inspire action or deep thought
        - Not be overused or cliché

        Format as:
        [The quote itself]

        — [Speaker's name], [Brief context about who they are or when/where quote was said]

        [One sentence about why this quote is particularly relevant or powerful]"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are curating today's ({today}) inspiring quote. Choose something meaningful and relevant that hasn't been overused. Never repeat quotes from previous days."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Unable to generate quote at this time."

def get_interesting_fact():
    """Get a fascinating historical or cultural fact"""
    try:
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""For {today}'s interesting fact, share a fascinating story from one of these categories:

        1. Historical Turning Points & Lesser-Known Details
        - Pivotal moments in history with surprising details
        - Lesser-known aspects of famous historical events
        - Personal stories of historical figures
        - Unexpected connections between historical events

        2. Cultural Heritage & Traditions
        - Origins of cultural practices
        - Evolution of social customs
        - Fascinating traditional knowledge
        - Cross-cultural connections

        3. Innovation & Discovery Stories
        - Personal struggles behind great discoveries
        - Unexpected origins of modern inventions
        - Serendipitous moments in science
        - Historical figures who shaped modern life

        4. Art & Literature History
        - Stories behind masterpieces
        - Authors' and artists' hidden experiences
        - Unexpected influences on cultural works
        - Historical context of creative works

        Format the fact as a brief, engaging narrative (3-4 sentences) that:
        - Starts with a hook
        - Includes human elements or personal details
        - Reveals something surprising
        - Connects to broader historical or cultural significance
        - Makes readers think "I never knew that!"

        Make it feel like sharing an interesting story rather than just stating a fact."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a masterful storyteller sharing fascinating historical and cultural insights for {today}. Focus on the human elements and surprising details that make history come alive. Never repeat stories from previous days."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error fetching interesting fact: {e}")
        return "Unable to generate interesting fact at this time."

def get_greeting():
    """Get time-appropriate greeting based on EST"""
    hour = datetime.now(pytz.timezone('America/New_York')).hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

# Get current date in different formats
current_date = datetime.now(pytz.timezone('America/New_York'))
formatted_date = current_date.strftime("%B %d, %Y")

# Generate content
print(f"Generating newsletter content for {formatted_date}...")
news_summary = get_news_headlines()
breakthrough_news = get_breakthrough_news()
philosophical_insight = get_philosophical_insight()
wellbeing_tip = get_wellbeing_tip()
quote_of_the_day = get_quote_of_day()

interesting_fact = get_interesting_fact()
# life_pro_tip = chatgpt_prompt("Share one practical productivity or personal finance tip...", "Life Pro Tip")
brain_teaser = chatgpt_prompt(
    "Create a short, clever riddle with its answer. Ensure it's original and different from previous days. Separate the riddle and answer with '||'",
    "Brain Teaser"
)

# Split brain teaser into question and answer
teaser_parts = brain_teaser.split("||")
teaser_question = teaser_parts[0].strip()
teaser_answer = teaser_parts[1].strip() if len(teaser_parts) > 1 else "Answer coming soon!"

# Format as HTML with improved styling
greeting = get_greeting()
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Morning Digest - {formatted_date}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-color: #0071e3;
            --primary-light: #47a9ff;
            --secondary-color: #86868b;
            --background-color: #f5f5f7;
            --card-background: #ffffff;
            --text-primary: #1d1d1f;
            --text-secondary: #86868b;
            --accent-green: #00c16e;
            --accent-purple: #8e44ad;
            --accent-orange: #ff9500;
            --accent-red: #ff3b30;
            --accent-yellow: #ffcc00;
            --border-radius: 16px;
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
            --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
            --transition-speed: 0.3s;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'San Francisco', 'Helvetica Neue', sans-serif;
            line-height: 1.5;
            background-color: var(--background-color);
            color: var(--text-primary);
            padding: 0;
            margin: 0;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(180deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            position: relative;
            z-index: 10;
        }}

        .date {{
            color: var(--secondary-color);
            font-size: 0.95rem;
            font-weight: 500;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }}

        .section {{
            background: var(--card-background);
            padding: 30px;
            border-radius: var(--border-radius);
            margin-bottom: 24px;
            box-shadow: var(--shadow-md);
            transition: all var(--transition-speed) ease;
            border: 1px solid rgba(0,0,0,0.04);
            overflow: hidden;
        }}

        .section:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }}

        h1 {{
            color: var(--text-primary);
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }}

        h2 {{
            color: var(--text-primary);
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            letter-spacing: -0.3px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        h2::after {{
            content: "";
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.02) 100%);
            margin-left: 1rem;
        }}

        .news-item, .breakthrough-item {{
            margin-bottom: 2rem;
            padding: 1.5rem;
            background: rgba(255,255,255,0.5);
            border-radius: calc(var(--border-radius) - 4px);
            box-shadow: var(--shadow-sm);
            transition: all var(--transition-speed) ease;
            border: 1px solid rgba(0,0,0,0.03);
        }}

        .news-item:last-child, .breakthrough-item:last-child {{
            margin-bottom: 0;
        }}

        .news-item:hover, .breakthrough-item:hover {{
            background: rgba(255,255,255,0.9);
            box-shadow: var(--shadow-md);
        }}

        .breakthrough-item {{
            border-left: 4px solid var(--accent-green);
        }}

        .news-headline, .breakthrough-headline {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            line-height: 1.3;
            letter-spacing: -0.3px;
        }}

        .news-headline {{
            color: var(--text-primary);
        }}

        .breakthrough-headline {{
            color: var(--accent-green);
        }}

        .news-metadata {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            border-bottom: 1px solid rgba(0,0,0,0.05);
            padding-bottom: 0.75rem;
        }}

        .news-source, .news-date {{
            font-style: normal;
            font-weight: 500;
        }}

        .news-source {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .news-source::before {{
            content: "📰";
            font-size: 0.9rem;
        }}

        .news-date {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .news-date::before {{
            content: "🕒";
            font-size: 0.9rem;
        }}

        .news-summary, .breakthrough-summary {{
            font-size: 1rem;
            line-height: 1.6;
            color: var(--text-primary);
            margin: 0;
        }}

        .greeting {{
            font-size: 1.2rem;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
            font-weight: 600;
            letter-spacing: -0.3px;
        }}

        .newsletter-title {{
            font-size: 2.2rem;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        .reveal-button {{
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 18px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 500;
            margin: 1rem 0;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .reveal-button:hover {{
            background-color: var(--primary-light);
            transform: translateY(-2px);
        }}

        .reveal-button::after {{
            content: "→";
            font-size: 1rem;
            transition: transform 0.2s ease;
        }}

        .reveal-button:hover::after {{
            transform: translateX(3px);
        }}

        .answer {{
            display: none;
            margin-top: 1rem;
            padding: 1.5rem;
            background: rgba(0, 113, 227, 0.05);
            border-radius: 12px;
            opacity: 0;
            transition: all 0.4s ease;
            border-left: 3px solid var(--primary-color);
        }}

        .answer.visible {{
            opacity: 1;
        }}

        footer {{
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            font-size: 0.9rem;
            background: linear-gradient(0deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 100%);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}

        footer a {{
            color: var(--primary-color);
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        footer a:hover {{
            color: var(--primary-light);
            text-decoration: underline;
        }}

        .timestamp {{
            margin-top: 0.5rem;
            font-size: 0.8rem;
            opacity: 0.8;
        }}

        /* Section-specific styling */
        .section[data-section="headlines"] h2 {{
            color: var(--text-primary);
        }}

        .section[data-section="breakthroughs"] h2 {{
            color: var(--accent-green);
        }}

        .section[data-section="philosophy"] h2 {{
            color: var(--accent-purple);
        }}

        .section[data-section="fact"] h2 {{
            color: var(--accent-orange);
        }}

        .section[data-section="quote"] h2 {{
            color: var(--primary-color);
        }}

        .section[data-section="wellbeing"] h2 {{
            color: var(--accent-red);
        }}

        .section[data-section="teaser"] h2 {{
            color: var(--accent-yellow);
        }}

        /* Quote styling */
        .quote-content {{
            font-size: 1.3rem;
            line-height: 1.6;
            font-weight: 300;
            font-style: italic;
            position: relative;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
            background-color: rgba(0, 113, 227, 0.05);
            border-radius: 12px;
        }}

        .quote-content::before {{
            content: "\\"";
            font-size: 4rem;
            position: absolute;
            left: -0.3rem;
            top: -1.5rem;
            color: rgba(0, 113, 227, 0.2);
            font-family: Georgia, serif;
        }}
        
        .quote-content::after {{
            content: "\\"";
            font-size: 4rem;
            position: absolute;
            right: 0.5rem;
            bottom: -2.5rem;
            color: rgba(0, 113, 227, 0.2);
            font-family: Georgia, serif;
        }}

        .quote-attribution {{
            font-weight: 500;
            text-align: right;
            color: var(--text-secondary);
            margin: 1.5rem 0 1rem 0;
            padding-right: 1rem;
        }}

        .quote-relevance {{
            margin-top: 1.5rem;
            font-size: 0.95rem;
            color: var(--text-primary);
            background-color: rgba(0, 113, 227, 0.04);
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid var(--primary-color);
        }}

        /* Philosophical insight styling */
        .concept-name {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            color: var(--accent-purple);
            border-bottom: 2px solid rgba(142, 68, 173, 0.2);
            padding-bottom: 0.8rem;
            display: inline-block;
        }}

        .concept-explanation {{
            margin-bottom: 1.8rem;
            font-size: 1.05rem;
            line-height: 1.7;
            padding-left: 0.5rem;
            border-left: 3px solid rgba(142, 68, 173, 0.15);
            padding-left: 1rem;
        }}

        .think-about {{
            font-style: italic;
            color: var(--accent-purple);
            font-weight: 500;
            background-color: rgba(142, 68, 173, 0.08);
            padding: 1rem;
            border-radius: 8px;
            display: block;
            margin-top: 1.5rem;
            position: relative;
        }}
        
        .think-about::before {{
            content: "Think About:";
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--accent-purple);
            font-style: normal;
        }}

        /* Well-being styling */
        .wellbeing-content {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        
        .wellbeing-section {{
            margin-bottom: 0.5rem;
        }}
        
        .wellbeing-title {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
            color: var(--accent-red);
            display: block;
        }}

        .affirmation {{
            font-size: 1.2rem;
            font-weight: 500;
            margin-bottom: 0;
            color: var(--text-primary);
            text-align: center;
            padding: 1.2rem;
            background: rgba(255, 59, 48, 0.08);
            border-radius: 12px;
            line-height: 1.6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .wellbeing-tip {{
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text-primary);
            background: rgba(0,0,0,0.02);
            padding: 1.2rem;
            border-radius: 12px;
            border-left: 3px solid var(--accent-red);
        }}
        
        .wellbeing-citation {{
            font-style: italic;
            font-size: 0.9rem;
            color: var(--text-secondary);
            display: block;
            margin-top: 0.5rem;
            text-align: right;
        }}
        
        /* Did You Know styling */
        .fact-content {{
            font-size: 1.05rem;
            line-height: 1.8;
            padding: 0.5rem 1rem;
        }}
        
        .fact-content p {{
            margin-bottom: 1rem;
        }}
        
        .fact-content p:last-child {{
            margin-bottom: 0;
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            .container {{
                padding: 15px;
            }}
            
            .section {{
                padding: 20px;
            }}

            .header {{
                padding: 30px 0;
            }}

            h1 {{
                font-size: 2rem;
            }}

            .newsletter-title {{
                font-size: 1.8rem;
            }}

            .news-headline, .breakthrough-headline {{
                font-size: 1.2rem;
            }}
            
            .news-summary, .breakthrough-summary {{
                font-size: 0.95rem;
            }}

            .news-metadata {{
                flex-direction: column;
                gap: 0.25rem;
            }}
        }}

        @media (max-width: 480px) {{
            .section {{
                padding: 18px;
                border-radius: 12px;
            }}

            h2 {{
                font-size: 1.3rem;
            }}

            .news-item, .breakthrough-item {{
                padding: 1.2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="greeting">{greeting}, Saleh 👋</div>
            <h1 class="newsletter-title">Daily Morning Digest</h1>
            <div class="date">{formatted_date}</div>
        </header>
        
        <section class="section" data-section="headlines">
            <h2>🌍 Today's Headlines</h2>
            {news_summary}
        </section>
        
        <section class="section" data-section="breakthroughs">
            <h2>🚀 Breakthrough Innovations</h2>
            {breakthrough_news}
        </section>
        
        <section class="section" data-section="philosophy">
            <h2>🧠 Philosophical Insight</h2>
            <div class="philosophy-content">
                {philosophical_insight.replace('[', '<div class="concept-name">').replace(']', '</div>').replace('Think About:', '<div class="think-about">').replace('Think About: ', '<div class="think-about">')}
            </div>
        </section>
        
        <section class="section" data-section="fact">
            <h2>💡 Did You Know?</h2>
            <div class="fact-content">
                <p>{interesting_fact}</p>
            </div>
        </section>
        
        <section class="section" data-section="quote">
            <h2>✨ Quote of the Day</h2>
            <div class="quote-container">
                <div class="quote-content">{quote_of_the_day.split('—')[0].strip()}</div>
                <div class="quote-attribution">— {quote_of_the_day.split('—')[1].split('\n\n')[0].strip()}</div>
                <div class="quote-relevance">{quote_of_the_day.split('\n\n')[-1].strip()}</div>
            </div>
        </section>
        
        <section class="section" data-section="wellbeing">
            <h2>🌿 Well-being Tip</h2>
            <div class="wellbeing-content">
                {wellbeing_tip.replace("Today's Affirmation:", '<div class="wellbeing-section"><span class="wellbeing-title">Today\'s Affirmation</span><div class="affirmation">').replace("Quick Well-being Boost:", '</div></div><div class="wellbeing-section"><span class="wellbeing-title">Quick Well-being Boost</span><div class="wellbeing-tip">')}
            </div>
        </section>
        
        <section class="section" data-section="teaser">
            <h2>🧩 Brain Teaser</h2>
            <p>{teaser_question}</p>
            <button class="reveal-button" onclick="toggleAnswer()">Reveal Answer</button>
            <div class="answer" id="teaser-answer" style="display: none;">
                <p>{teaser_answer}</p>
            </div>
        </section>
        
        <footer>
            <p>Daily Morning Digest powered by AI</p>
            <p class="timestamp">Last updated: {current_date.strftime("%Y-%m-%d %H:%M")} EST</p>
        </footer>
    </div>

    <script>
        function toggleAnswer() {{
            const answer = document.getElementById('teaser-answer');
            const isHidden = answer.style.display === 'none' || answer.style.display === '';
            
            if (isHidden) {{
                answer.style.display = 'block';
                setTimeout(function() {{
                    answer.classList.add('visible');
                }}, 10);
            }} else {{
                answer.classList.remove('visible');
                setTimeout(function() {{
                    answer.style.display = 'none';
                }}, 400);
            }}
        }}
    </script>
</body>
</html>
"""

# Save as index.html
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print(f"Newsletter generated successfully for {formatted_date}!")