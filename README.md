# Daily Morning Digest

An automated daily newsletter that helps you become smarter and happier.

## Features
- Top Headlines from around the world
- Breakthrough Innovations in Technology and AI
- Daily Philosophical Insight
- Interesting Fact of the Day
- Quote of the Day
- Well-being Tip and Affirmation
- Brain Teaser

## Setup
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set your OpenAI API key as environment variable:
   ```bash
   # Create a .env file with your key
   OPENAI_API_KEY='your-openai-api-key-here'
   ```
4. Run the script: `python run_newsletter.py`

The script will generate an `index.html` file that you can open in your browser.

## How It Works
1. `generate_newsletter.py` - Main script that generates the newsletter content using OpenAI API
2. `fix_html.py` - Utility script that fixes CSS formatting issues in the generated HTML
3. `run_newsletter.py` - Wrapper script that runs both scripts in sequence

## Automatic Updates
The newsletter automatically updates daily at 8 AM EST using GitHub Actions.
To set this up in your own repository:

1. Add your OpenAI API key as a repository secret in GitHub:
   - Go to Settings → Secrets and variables → Actions
   - Add `OPENAI_API_KEY` as a secret

2. The GitHub workflow will run automatically at the scheduled time. 