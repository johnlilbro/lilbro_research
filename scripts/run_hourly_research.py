from __future__ import annotations

import random
import subprocess
from pathlib import Path

from research.search import search_duckduckgo
from research.state import load_state, save_state
from research.topics import TOPICS

BASE_DIR = Path(__file__).resolve().parent.parent
MAX_CYCLES = 6


def choose_topic(state: dict) -> str:
    available = [t for t in TOPICS if t not in state.get("used_topics", [])]
    if not available:
        available = TOPICS[:]
    return random.choice(available)


def ideas_markdown(topic: str, items: list[dict]) -> str:
    lines = [f"# IDEAS.md", "", f"Topic: {topic}", "", "## Three idea summaries", ""]
    for idx, item in enumerate(items[:3], start=1):
        lines.append(f"### Idea {idx}: {item['title']}")
        lines.append("")
        lines.append(f"- Source: {item['url']}")
        lines.append(f"- Summary: {item['snippet'] or 'Recent development related to the topic.'}")
        lines.append(f"- Idea angle: Build or study a product/research direction around {topic} using this development as signal.")
        lines.append("")
    return "\n".join(lines)


def summaries_markdown(topic: str, items: list[dict]) -> str:
    lines = [f"# SUMMARIES.md", "", f"Topic: {topic}", "", "## Three related paper/conference summaries", ""]
    for idx, item in enumerate(items[:3], start=1):
        lines.append(f"### Paper/Conference Lead {idx}: {item['title']}")
        lines.append("")
        lines.append(f"- Source: {item['url']}")
        lines.append(f"- Abstract/summary: {item['snippet'] or 'Related conference or paper lead discovered from web search.'}")
        lines.append("")
    return "\n".join(lines)


def run(cmd: list[str]):
    subprocess.run(cmd, cwd=BASE_DIR, check=True)


def main():
    state = load_state()
    if state.get("completed_cycles", 0) >= MAX_CYCLES:
        print("Max cycles reached; exiting.")
        return

    topic = choose_topic(state)
    branch = f"devel-{topic}"

    run(["git", "checkout", "main"])
    run(["git", "pull", "--ff-only", "origin", "main"])
    run(["git", "checkout", "-b", branch])

    idea_items = search_duckduckgo(f"latest AI computing developments {topic}", limit=5)
    paper_items = search_duckduckgo(f"conference papers abstracts {topic} AI computing", limit=5)

    (BASE_DIR / "IDEAS.md").write_text(ideas_markdown(topic, idea_items))
    (BASE_DIR / "SUMMARIES.md").write_text(summaries_markdown(topic, paper_items))

    run(["git", "add", "IDEAS.md", "SUMMARIES.md"])
    run(["git", "commit", "-m", f"Add research notes for topic: {topic}"])
    run(["git", "push", "-u", "origin", branch])
    run(["git", "checkout", "main"])

    state["completed_cycles"] = state.get("completed_cycles", 0) + 1
    used = state.get("used_topics", [])
    if topic not in used:
        used.append(topic)
    state["used_topics"] = used
    save_state(state)
    print(f"Completed cycle {state['completed_cycles']} on topic {topic}")


if __name__ == "__main__":
    main()
