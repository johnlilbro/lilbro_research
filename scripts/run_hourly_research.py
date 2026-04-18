from __future__ import annotations

import random
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from research.notify import write_notification
from research.search import multi_search
from research.state import load_state, save_state
from research.topics import TOPICS

BASE_DIR = Path(__file__).resolve().parent.parent
MAX_CYCLES = 6
LOG_PATH = BASE_DIR / "cron.log"


def log(message: str) -> None:
    with LOG_PATH.open("a") as f:
        f.write(message + "\n")


def choose_topic(state: dict) -> str:
    available = [t for t in TOPICS if t not in state.get("used_topics", [])]
    if not available:
        available = TOPICS[:]
    return random.choice(available)


def ideas_markdown(topic: str, items: list[dict]) -> str:
    lines = ["# IDEAS.md", "", f"Topic: {topic}", "", "## Three idea summaries", ""]
    if not items:
        lines.extend([
            "No strong live search results were retrieved for this cycle.",
            "",
            f"Fallback idea 1: Explore a practical product angle around {topic} in AI/computing.",
            f"Fallback idea 2: Survey enterprise adoption patterns related to {topic}.",
            f"Fallback idea 3: Identify where {topic} could become a durable research or startup wedge.",
        ])
        return "\n".join(lines)

    for idx, item in enumerate(items[:3], start=1):
        lines.append(f"### Idea {idx}: {item['title']}")
        lines.append("")
        lines.append(f"- Source: {item['url']}")
        lines.append(f"- Summary: {item['snippet'] or 'Recent development related to the topic.'}")
        lines.append(f"- Idea angle: Build or study a product/research direction around {topic} using this development as signal.")
        lines.append("")
    return "\n".join(lines)


def summaries_markdown(topic: str, items: list[dict]) -> str:
    lines = ["# SUMMARIES.md", "", f"Topic: {topic}", "", "## Three related paper/conference summaries", ""]
    if not items:
        lines.extend([
            "No direct paper/conference leads were found in this cycle.",
            "",
            f"Fallback lead 1: Search arXiv for recent work on {topic}.",
            f"Fallback lead 2: Search ACM/IEEE proceedings for {topic}-related conference papers.",
            f"Fallback lead 3: Look for workshop tracks or industry conference talks centered on {topic}.",
        ])
        return "\n".join(lines)

    for idx, item in enumerate(items[:3], start=1):
        lines.append(f"### Paper/Conference Lead {idx}: {item['title']}")
        lines.append("")
        lines.append(f"- Source: {item['url']}")
        lines.append(f"- Abstract/summary: {item['snippet'] or 'Related conference or paper lead discovered from web search.'}")
        lines.append("")
    return "\n".join(lines)


def run(cmd: list[str]):
    subprocess.run(cmd, cwd=BASE_DIR, check=True)


def ts_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def main():
    state = load_state()
    if state.get("completed_cycles", 0) >= MAX_CYCLES:
        log("Max cycles reached; exiting.")
        print("Max cycles reached; exiting.")
        return

    topic = choose_topic(state)
    branch = f"devel-{topic}"
    log(f"Starting cycle {state.get('completed_cycles', 0) + 1} for topic: {topic}")

    run(["git", "checkout", "main"])
    run(["git", "pull", "--ff-only", "origin", "main"])
    run(["git", "checkout", "-b", branch])

    idea_queries = [
        f"latest AI computing developments {topic}",
        f"{topic} AI latest news",
        f"{topic} machine learning recent developments",
    ]
    paper_queries = [
        f"site:arxiv.org {topic} AI",
        f"site:ieeexplore.ieee.org {topic} AI",
        f"site:dl.acm.org {topic} AI conference paper",
    ]

    idea_items = multi_search(idea_queries, limit=5)
    paper_items = multi_search(paper_queries, limit=5)
    log(f"Found {len(idea_items)} idea leads and {len(paper_items)} paper leads for {topic}")

    (BASE_DIR / "IDEAS.md").write_text(ideas_markdown(topic, idea_items))
    (BASE_DIR / "SUMMARIES.md").write_text(summaries_markdown(topic, paper_items))

    timestamp = ts_slug()
    note = "\n".join([
        "# Research Cycle Complete",
        "",
        f"Topic: {topic}",
        f"Branch: {branch}",
        f"Cycle: {state.get('completed_cycles', 0) + 1}",
        f"Timestamp: {timestamp}",
        "",
        "Generated files:",
        "- IDEAS.md",
        "- SUMMARIES.md",
    ])
    write_notification(timestamp, note)

    run(["git", "add", "IDEAS.md", "SUMMARIES.md", "notifications"])
    run(["git", "commit", "-m", f"Add research notes for topic: {topic}"])
    run(["git", "push", "-u", "origin", branch])
    run(["git", "checkout", "main"])

    state["completed_cycles"] = state.get("completed_cycles", 0) + 1
    used = state.get("used_topics", [])
    if topic not in used:
        used.append(topic)
    state["used_topics"] = used
    save_state(state)
    log(f"Completed cycle {state['completed_cycles']} on topic {topic}")
    print(f"Completed cycle {state['completed_cycles']} on topic {topic}")


if __name__ == "__main__":
    main()
