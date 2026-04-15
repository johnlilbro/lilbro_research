# lilbro_research

This repo is for short-cycle exploratory research branches.

## Planned behavior

Every hour for the next 6 hours, the system should:

1. create a new branch off `main`
2. name it `devel-<x>` where `<x>` is a random one-word topic from AI/computing
3. do lightweight web research on the latest developments in that topic
4. write 3 idea summaries into `IDEAS.md`
5. do follow-up research for conferences/papers related to those ideas
6. write 3 paper/conference summaries into `SUMMARIES.md`
7. commit and push that branch

## Notes

- The automation is intentionally lightweight and designed for iterative exploration.
- A local state file is used to stop after 6 cycles.
- The web research path can be improved later with better search and paper retrieval.

## Manual run

```bash
python3 scripts/run_hourly_research.py
```
