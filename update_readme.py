import requests

username = "nibirmahmud"
url = f"https://api.chess.com/pub/player/{username}/stats"
res = requests.get(url)
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

markdown = f\"\"\"\n### ♟️ Chess.com Stats for [{username}](https://www.chess.com/member/{username})\n\n| Mode   | Current | Best | Wins | Losses | Draws |\n|--------|---------|------|------|--------|-------|\n| Bullet | {bullet[0]} | {bullet[1]} | {bullet[2]} | {bullet[3]} | {bullet[4]} |\n| Blitz  | {blitz[0]} | {blitz[1]} | {blitz[2]} | {blitz[3]} | {blitz[4]} |\n| Rapid  | {rapid[0]} | {rapid[1]} | {rapid[2]} | {rapid[3]} | {rapid[4]} |\n| Daily  | {daily[0]} | {daily[1]} | {daily[2]} | {daily[3]} | {daily[4]} |\n\n🧩 **Puzzle Rating:** {puzzle}  \n⚡ **Puzzle Rush Score:** {rush}\n\"\"\"

# Replace section in README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start = "<!--chess-stats-start-->"
end = "<!--chess-stats-end-->"
before = content.split(start)[0]
after = content.split(end)[1]
new_content = before + start + "\\n" + markdown + "\\n" + end + after

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)
