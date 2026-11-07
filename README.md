# dev-ops-test1

A DevOps exercise from February 2024: a three-page Flask site packaged in a
Docker image and served by gunicorn. The site is only the payload. There are two
commits, and nothing has changed since.

## What is here

- `site/app.py` is the Flask application. It has three routes, and each returns
  one fixed string: `/` answers `MAIN PAGE`, `/about` answers
  `THIS IS THE ABOUT PAGE` and `/blog` answers `HERE WILL BE ARTICLES`. There are
  no templates and no data.
- `Dockerfile` copies `site/` into an image built on `python:3.12.2-bookworm`,
  installs `flask` and `gunicorn` with no version pinned, exposes port 8000 and
  starts gunicorn with five workers.

To try it, with Docker installed:

```bash
docker build -t dev-ops-test1 .
docker run -p 8000:8000 dev-ops-test1
```

Neither the image nor the site is built or tested here.

## Working on it

This repository ships no program. `.\recipe.ps1` is still its whole interface:
`.\recipe.ps1 test` runs pytest and ruff over `.claude`, and `.\recipe.ps1 info`
prints the metadata. The other verbs print `nothing to <verb>`. `CLAUDE.md`
holds the rules.

## License

MIT. See [LICENSE](LICENSE).

## Lab requirements

This repository complies with [revision 4.0.0](http://127.0.0.1:3000/igors-lab/software-requirements/src/tag/v4.0.0/BEST_REQUIREMENTS.md) of the lab requirements, except R-02 (#7), R-09 (#8), R-41 (#9), R-42 (#10).
