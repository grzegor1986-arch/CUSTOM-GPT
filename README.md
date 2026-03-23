# CUSTOM-GPT

A lightweight workspace for experimenting with custom GPT behaviors and prompts. This repository currently contains scaffolding for future automation and serves as a starting point for small utilities or notebooks.

## Getting started
1. Ensure you have Python 3.11 or later installed.
2. Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
3. Install any project dependencies as they are added.

## Development
- Commit changes in small, reviewable increments.
- Keep configuration files under version control and avoid committing secrets.
- Use `.gitignore` to keep transient artifacts out of the repository.

## How to connect your GitHub repository with this CustomGPT workspace
If by "connect GitHub with CustomGPT" you mean syncing this project with your GitHub account, use the steps below.

### 1) Create an empty GitHub repository
- In GitHub, click **New repository**.
- Set a name (for example: `custom-gpt`).
- Do **not** initialize with a README if this local repo already has one.

### 2) Add the GitHub remote in this project
```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
```

If `origin` already exists, update it instead:
```bash
git remote set-url origin https://github.com/<your-username>/<repo-name>.git
```

### 3) Push your current branch to GitHub
```bash
git push -u origin $(git branch --show-current)
```

### 4) Verify everything is connected
```bash
git remote -v
git status
```

## Optional: connect GitHub updates to a deployed GPT workflow
If you are using OpenAI API + your own app backend, a common pattern is:
1. GitHub webhook (`push` event) triggers CI/CD.
2. CI/CD updates prompt/config files or tools used by your app.
3. Your app reloads that configuration for requests sent to GPT models.

## Bonus: your own GUI + custom tools in ChatGPT (official OpenAI path)
Yes — this is exactly where **Apps SDK** and **MCP** fit.

### Option A: GPT Actions (fastest path for API tools in a Custom GPT)
Use this when you want your GPT to call your existing REST API with an OpenAPI schema.

1. Build or expose an HTTPS API endpoint.
2. In GPT builder, add an **Action** and paste your OpenAPI schema.
3. Configure auth (None / API Key / OAuth) and test each action.
4. Add clear instructions so the GPT knows when to call each action.

Official docs:
- GPT Actions overview: https://developers.openai.com/api/docs/actions/introduction
- Getting started: https://developers.openai.com/api/docs/actions/getting-started
- Authentication: https://developers.openai.com/api/docs/actions/authentication

### Option B: Apps SDK + MCP (for your own GUI inside ChatGPT)
Use this when you want both tool calling **and** a custom interface component shown in ChatGPT.

1. Build an app with the Apps SDK.
2. Implement tools via MCP on your backend.
3. Test in ChatGPT Developer Mode.
4. Iterate on UX + tool descriptions to improve tool selection.

Official docs:
- Apps SDK intro: https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk
- Announce + concepts: https://openai.com/index/introducing-apps-in-chatgpt/
- MCP docs: https://platform.openai.com/docs/mcp/
- ChatGPT Developer Mode: https://platform.openai.com/docs/developer-mode

### Which one should you choose?
- Choose **GPT Actions** if your goal is quick API integration in a Custom GPT.
- Choose **Apps SDK + MCP** if you want richer UX (your own GUI) and deeper integration patterns.

## Contributing
Issues and pull requests are welcome as the project grows. Please include clear descriptions of any changes or ideas for new functionality.
