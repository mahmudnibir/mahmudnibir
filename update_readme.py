import requests

username = "nibirmahmud"
url = f"https://api.chess.com/pub/player/{username}/stats"
res = requests.get(url)

if res.status_code != 200:
    raise Exception("Failed to fetch data from Chess.com API.")

data = res.json()

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

bullet = get_stats("bullet")
blitz = get_stats("blitz")
rapid = get_stats("rapid")
daily = get_stats("daily")
puzzle = data.get("tactics", {}).get("highest", {}).get("rating", "N/A")
rush = data.get("puzzle_rush", {}).get("best", {}).get("score", "N/A")

# Create markdown stats
markdown = f"""### ♟️ Chess.com Stats for [{username}](https://www.chess.com/member/{username})

| Mode   | Current | Best | Wins | Losses | Draws |
|--------|---------|------|------|--------|-------|
| Bullet | {bullet[0]} | {bullet[1]} | {bullet[2]} | {bullet[3]} | {bullet[4]} |
| Blitz  | {blitz[0]} | {blitz[1]} | {blitz[2]} | {blitz[3]} | {blitz[4]} |
| Rapid  | {rapid[0]} | {rapid[1]} | {rapid[2]} | {rapid[3]} | {rapid[4]} |
| Daily  | {daily[0]} | {daily[1]} | {daily[2]} | {daily[3]} | {daily[4]} |

🧩 **Puzzle Rating:** {puzzle}  
⚡ **Puzzle Rush Score:** {rush}
"""

# Replace the section in README.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "<!--chess-stats-start-->"
end_marker = "<!--chess-stats-end-->"
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
