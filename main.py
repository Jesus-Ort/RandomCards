import base64
import csv
import os
import random
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

import requests
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

GENERATED_DIR = BASE_DIR / "generated"
DATA_DIR = BASE_DIR / "data"
STATS_FILE = DATA_DIR / "card_stats.csv"

GENERATED_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

load_dotenv(BASE_DIR / ".env")


TWITTERAPIS_KEY = os.getenv("TWITTERAPIS_KEY")
X_AUTH_TOKEN = os.getenv("X_AUTH_TOKEN")
X_CT0 = os.getenv("X_CT0")
POST_TEXT = os.getenv("POST_TEXT", "")

BASE_URL = "https://api.twitterapis.com/twitter"


required_credentials = {
    "TWITTERAPIS_KEY": TWITTERAPIS_KEY,
    "X_AUTH_TOKEN": X_AUTH_TOKEN,
    "X_CT0": X_CT0,
}

missing_credentials = [
    name for name, value in required_credentials.items()
    if not value
]

if missing_credentials:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing_credentials)
    )


HEADERS = {
    "Authorization": f"Bearer {TWITTERAPIS_KEY}",
    "Content-Type": "application/json",
}


# ============================================================
# DECK
# ============================================================

SUITS = {
    "Corazones": "♥",
    "Diamantes": "♦",
    "Picas": "♠",
    "Treboles": "♣",
}

VALUES = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
]

DECK = [
    (value, suit)
    for suit in SUITS
    for value in VALUES
]


# ============================================================
# GENERATE RANDOM CARD
# ============================================================

value, suit = random.choice(DECK)
symbol = SUITS[suit]

print(f"Random card: {value}{symbol}")


# ============================================================
# CREATE IMAGE
# ============================================================

WIDTH = 800
HEIGHT = 1200

img = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    "white",
)

draw = ImageDraw.Draw(img)


BORDER_WIDTH = 25
MARGIN = BORDER_WIDTH // 2

draw.rectangle(
    [
        MARGIN,
        MARGIN,
        WIDTH - MARGIN - 1,
        HEIGHT - MARGIN - 1,
    ],
    outline="black",
    width=BORDER_WIDTH,
)


def get_font(size: int):
    possible_fonts = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arial.ttf",
    ]

    for font_path in possible_fonts:
        try:
            return ImageFont.truetype(
                font_path,
                size,
            )
        except OSError:
            continue

    raise RuntimeError(
        "Could not find a suitable TrueType font."
    )


font_large = get_font(200)

text_color = (
    "red"
    if suit in ["Corazones", "Diamantes"]
    else "black"
)

card_text = f"{value}{symbol}"

bbox = draw.textbbox(
    (0, 0),
    card_text,
    font=font_large,
)

text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = (WIDTH - text_width) / 2
y = (HEIGHT - text_height) / 2 - bbox[1]

draw.text(
    (x, y),
    card_text,
    fill=text_color,
    font=font_large,
)


# ============================================================
# SAVE IMAGE
# ============================================================

now = datetime.now(ZoneInfo("America/Caracas"))
date_str = now.strftime("%d-%m-%Y")

filename = f"card_{date_str}.png"
image_path = GENERATED_DIR / filename

img.save(image_path)

print(f"Generated: {image_path}")


# ============================================================
# REGISTER X SESSION
# ============================================================

print("\nRegistering X session...")

session_response = requests.post(
    f"{BASE_URL}/customer/session",
    headers=HEADERS,
    json={
        "auth_token": X_AUTH_TOKEN,
        "ct0": X_CT0,
    },
    timeout=30,
)

if not session_response.ok:
    print(session_response.text)
    session_response.raise_for_status()

print("X session registered.")


# ============================================================
# UPLOAD IMAGE
# ============================================================

print("\nUploading image...")

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(
        image_file.read()
    ).decode("utf-8")


upload_response = requests.post(
    f"{BASE_URL}/media/upload",
    headers=HEADERS,
    json={
        "media_data": encoded_image,
    },
    timeout=60,
)

if not upload_response.ok:
    print(upload_response.text)
    upload_response.raise_for_status()


upload_data = upload_response.json()

if not upload_data.get("ok"):
    raise RuntimeError(
        f"Media upload failed: {upload_data}"
    )


media_id = upload_data["media_id"]

print(f"Media uploaded: {media_id}")


# ============================================================
# WAIT FOR MEDIA PROCESSING
# ============================================================

print("Waiting for media processing...")

time.sleep(2)


# ============================================================
# CREATE POST
# ============================================================

print("\nPublishing post...")


post_payload = {
    "text": f"{value}{symbol}",
    "media_ids": [media_id],
}


post_response = requests.post(
    f"{BASE_URL}/tweet/create",
    headers=HEADERS,
    json=post_payload,
    timeout=30,
)


if not post_response.ok:
    print("\nERROR PUBLISHING TO X")
    print("=" * 50)
    print(post_response.text)
    print("=" * 50)

    post_response.raise_for_status()


post_data = post_response.json()


if not post_data.get("ok"):
    raise RuntimeError(
        f"Post creation failed: {post_data}"
    )


post_id = post_data["tweet_id"]
post_url = post_data["url"]


print("\nPOST PUBLISHED SUCCESSFULLY")
print("=" * 50)
print(f"Card: {value}{symbol}")
print(f"Post ID: {post_id}")
print(f"URL: {post_url}")
print("=" * 50)


# ============================================================
# SAVE HISTORY
# ============================================================

file_exists = STATS_FILE.exists()

with open(
    STATS_FILE,
    "a",
    newline="",
    encoding="utf-8",
) as file:

    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "date",
            "value",
            "suit",
            "symbol",
            "filename",
            "post_id",
        ])

    writer.writerow([
        date_str,
        value,
        suit,
        symbol,
        filename,
        post_id,
    ])


print(f"\nHistory saved: {STATS_FILE}")