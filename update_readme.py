import requests

# === CONFIGURATION ===
username = "nibirmahmud"
url = f"https://api.chess.com/pub/player/{username}/stats"
headers = {"User-Agent": "Mozilla/5.0"}

# === FETCH DATA ===
res = requests.get(url, headers=headers)
print("Status Code:", res.status_code)
print("Response preview:", res.text[:200])  # Show first 200 characters of response

if res.status_code != 200:
    raise Exception("Failed to fetch data from Chess.com API.")

data = res.json()

# === HELPER FUNCTION ===
def get_stats(mode):
    stats = data.get(f"chess_{mode}", {})
    last = stats.get("last", {}).get("rating", "N/A")
    best = stats.get("best", {}).get("rating", "N/A")
    record = stats.get("record", {})
    return [
        last,
        best,
        record.get("win", 0),
        record.get("loss", 0),
        record.get("draw", 0)
    ]

# === STATS ===
bullet = get_stats("bullet")
blitz = get_stats("blitz")
rapid = get_stats("rapid")
daily = get_stats("daily")
puzzle = data.get("tactics", {}).get("highest", {}).get("rating", "N/A")
rush = data.get("puzzle_rush", {}).get("best", {}).get("score", "N/A")

# === MARKDOWN GENERATION ===
markdown = f"""### ♟️ Chess.com Stats for [{username}](https://www.chess.com/member/{username})

| Mode   | Current | Wins | Losses | Draws |
|--------|---------|-------|--------|-------|
|⏱️ Rapid  | {rapid[0]} | {rapid[2]} | {rapid[3]} | {rapid[4]} |
|⚡ Blitz  | {blitz[0]} | {blitz[2]} | {blitz[3]} | {blitz[4]} |
|🚅 Bullet | {bullet[0]} | {bullet[2]} | {bullet[3]} | {bullet[4]} |

🧩 **Puzzle Rating:** {puzzle}  
"""

# === README UPDATE ===
start_marker = "<!--chess-stats-start-->"
end_marker = "<!--chess-stats-end-->"

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find(start_marker)
end = content.find(end_marker)

if start == -1 or end == -1:
    raise Exception("Start or end markers not found in README.md")

new_content = (
    content[:start + len(start_marker)] +
    "\n" + markdown + "\n" +
    content[end:]
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ README.md updated successfully!")
