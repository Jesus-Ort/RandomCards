# RandomCards

A simple automated bot that randomly generates a playing card and publishes it to X once a day.

RandomCards is a small automation project built with Python, GitHub Actions, Pillow, and the TwitterAPIs service.

The goal is intentionally simple:

> Generate one completely random playing card and publish it to X once a day.

---

## Features

- Generates a completely random card from a standard 52-card deck.
- Generates an image of the selected card using Pillow.
- Publishes the generated card to X automatically.
- Runs once per day using GitHub Actions.
- Can be executed manually through GitHub Actions.
- Records each generated card and its X post ID in a CSV file.
- Does not prevent repeated cards.
- Does not assign meanings or interpretations to cards.
- Does not require a local computer or server to remain running.

---

## How It Works

The complete process is:

```text
52-card deck
     │
     ▼
Select random card
     │
     ▼
Generate card image
     │
     ▼
Upload image
     │
     ▼
Publish to X
     │
     ▼
Save publication history
```

Each execution generates exactly one random card.

The history stored in the CSV file does **not** influence future card generation.

A card can therefore be generated again at any time.

---

## Tech Stack

- Python 3.13
- Pillow
- Requests
- python-dotenv
- GitHub Actions
- TwitterAPIs
- X

---

## Project Structure

```text
RandomCards/
│
├── .github/
│   └── workflows/
│       └── daily-card.yml
│
├── data/
│   └── card_stats.csv
│
├── generated/
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

### `main.py`

Contains the complete application logic:

- Random card selection
- Image generation
- X session registration
- Image upload
- X post creation
- Publication history

### `data/card_stats.csv`

Stores the history of generated cards and their corresponding X post IDs.

Example:

```csv
date,value,suit,symbol,filename,post_id
09-09-2026,10,Picas,♠,card_09-09-2026.png,123456789
```

### `generated/`

Contains the card images generated during local executions.

Generated images are excluded from Git using `.gitignore`.

### `.github/workflows/daily-card.yml`

Contains the GitHub Actions workflow responsible for executing the bot automatically every day.

---

## Card Generation

RandomCards uses a standard 52-card deck.

### Suits

```text
♥ Hearts
♦ Diamonds
♠ Spades
♣ Clubs
```

### Values

```text
A 2 3 4 5 6 7 8 9 10 J Q K
```

A card is selected randomly from all 52 possible combinations.

Examples:

```text
A♥
7♦
10♠
Q♣
K♥
```

---

## Image Generation

Each card is generated as a PNG image with the following characteristics:

```text
Width:        800px
Height:       1200px
Format:       PNG
Background:   White
Border:       Black
```

The card value and suit symbol are displayed in the center of the image.

Hearts and diamonds are displayed in red.

Spades and clubs are displayed in black.

Example:

```text
┌──────────────────────┐
│                      │
│                      │
│                      │
│         10♠          │
│                      │
│                      │
│                      │
└──────────────────────┘
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Jesus-Ort/RandomCards.git
cd RandomCards
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root of the project:

```env
TWITTERAPIS_KEY=your_twitterapis_key
X_AUTH_TOKEN=your_x_auth_token
X_CT0=your_x_ct0
POST_TEXT=
```

These credentials are used to authenticate the application and publish posts to X through TwitterAPIs.

---

## Security

Sensitive credentials must never be committed to GitHub.

The `.env` file should be included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
generated/*.png
```

Never expose or commit:

```text
TWITTERAPIS_KEY
X_AUTH_TOKEN
X_CT0
```

For GitHub Actions, these values should be stored as GitHub Secrets.

---

## Running Locally

After configuring the environment variables, run:

```bash
python main.py
```

The program will:

1. Select a random card.
2. Generate the card image.
3. Register the X session.
4. Upload the generated image.
5. Publish the card to X.
6. Save the publication information to `data/card_stats.csv`.

Example:

```text
Random card: 10♠

Generated: generated/card_09-09-2026.png

Registering X session...
X session registered.

Uploading image...
Media uploaded.

Waiting for media processing...

Publishing post...

Post published successfully.
```

---

## GitHub Actions

RandomCards uses GitHub Actions to run the bot automatically.

This allows the application to run without keeping a personal computer or server online.

The workflow is configured to execute every day at:

**8:00 AM Venezuela time (UTC-4)**

GitHub Actions uses UTC for cron schedules, so the workflow uses:

```yaml
cron: "0 12 * * *"
```

The workflow also includes `workflow_dispatch`, allowing it to be executed manually.

---

## GitHub Secrets

The following secrets must be configured in the GitHub repository:

```text
Settings
→ Secrets and variables
→ Actions
```

Required secrets:

```text
TWITTERAPIS_KEY
X_AUTH_TOKEN
X_CT0
```

These values are provided to the application at runtime.

They are not stored directly in the source code.

---

## Manual Workflow Execution

The workflow can be executed manually from:

```text
GitHub
→ Actions
→ RandomCards Daily
→ Run workflow
```

Manual execution is useful for:

- Testing the workflow.
- Verifying API credentials.
- Testing changes.
- Confirming that GitHub Actions can publish successfully.
- Checking the complete automation pipeline.

---

## Automated Workflow

Once configured, GitHub Actions handles the complete process:

```text
GitHub Actions
      │
      ▼
Set up Python
      │
      ▼
Install dependencies
      │
      ▼
Run main.py
      │
      ├── Generate random card
      │
      ├── Generate image
      │
      ├── Register X session
      │
      ├── Upload image
      │
      └── Publish post
      │
      ▼
Update card_stats.csv
```

The local development machine does not need to be running.

---

## Publication History

Every successful publication is recorded in:

```text
data/card_stats.csv
```

The CSV contains:

| Field | Description |
|---|---|
| `date` | Date when the card was generated |
| `value` | Card value |
| `suit` | Card suit |
| `symbol` | Suit symbol |
| `filename` | Generated image filename |
| `post_id` | X post ID |

Example:

```csv
date,value,suit,symbol,filename,post_id
09-09-2026,10,Picas,♠,card_09-09-2026.png,123456789
```

The history is only informational.

It does not affect the random card selection process.

---

## Design Philosophy

RandomCards intentionally avoids unnecessary complexity.

The project does not implement:

- A database
- A backend server
- A web application
- User accounts
- Card meanings
- Recommendation algorithms
- Duplicate prevention
- Card frequency analysis
- Complex scheduling infrastructure

The entire purpose of the project is:

```text
Generate one random card
        ↓
Generate its image
        ↓
Publish it
        ↓
Record the result
```

This makes the application small, easy to understand, and easy to maintain.

---

## Why GitHub Actions?

GitHub Actions was chosen to provide a simple way to run the Python script on a schedule without maintaining a dedicated server.

It provides the environment required to:

- Run Python.
- Install project dependencies.
- Access encrypted secrets.
- Execute the application.
- Commit the updated publication history.

---

## API Integration

RandomCards uses TwitterAPIs as the external service responsible for interacting with X.

The application performs the following operations:

```text
Register X session
       │
       ▼
Upload generated image
       │
       ▼
Create X post
```

The API credentials are supplied through environment variables locally and GitHub Secrets in production.

---

## Reliability

The application is designed as a small scheduled automation rather than a continuously running service.

If an execution fails, GitHub Actions provides execution logs that can be used to identify the failed step.

The workflow can also be manually executed again after correcting an issue.

---

## Future Improvements

Possible improvements include:

- Polling the media processing status instead of using a fixed delay.
- Automated notifications when a publication fails.
- Better error handling and retry logic.
- Automated tests.
- More detailed logging.
- A small dashboard showing publication history.
- Statistics about generated cards.

These features are intentionally outside the current scope.

---

## Purpose

RandomCards is a small practical automation project designed to experiment with the integration of several technologies into a complete automated workflow.

The project demonstrates:

- Python scripting.
- Random data generation.
- Image generation with Pillow.
- REST API integration.
- Environment variable management.
- Secret management.
- Git and GitHub.
- GitHub Actions.
- Cron scheduling.
- Automated social media publishing.
- File-based data persistence.

The project is intentionally simple, but it demonstrates a complete pipeline from local development to automated cloud execution.

---

## License

This project is licensed under the MIT License.
