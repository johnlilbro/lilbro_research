# NOTES

## Current automation model

- Base branch: `main`
- Each cycle creates a branch like `devel-<topic>`
- One topic per cycle
- Stops itself after 6 completed cycles

## Output files per topic branch

- `IDEAS.md`
- `SUMMARIES.md`
- notification-ready completion file in `notifications/`

## Current retrieval behavior

- uses multiple search queries per topic
- adds fallback content if live search results are weak or empty
- writes debug messages into `cron.log`
- writes a notification-ready completion note after a successful cycle

## Future improvements

- smarter topic selection
- richer summaries
- better conference/paper extraction
- stronger retry / denial handling
- real OpenClaw-driven messaging on cycle completion
