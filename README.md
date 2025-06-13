# 🚀 PIni — Project Initializer

**PIni** stands for **Project Initializer** — a blazing-fast CLI tool to scaffold new projects in your favorite frameworks **with zero setup fuss**.

Whether you're starting a new **FastAPI**, **Django**, **DRF**, **Next.js**, or plain **Python** project, PIni gets you a clean, standardized, production-ready starter in seconds.

<img src='pini-demo.gif' style="width: 100%; height: auto;" />

---

## ⚙️ Features

- ✅ Scaffolds common frameworks (FastAPI, Django, DRF, Next.js, Python)
- 🔧 Pre-configured **linters**, **formatters**, and **pre-commit hooks**
- 🧼 Opinionated defaults for **code style**, **project structure**, and **.gitignore**
- 📝 Auto-generates README and adds author info
- 🔒 Git initialized + first commit (so Commitizen doesn’t blow up)
- ✨ Commitizen + semantic commits ready out-of-the-box

---

## 💡 Why?

I got tired of rewriting the same setup boilerplate for every new idea?
PIni exists so you can **stop configuring** and **start building** without compromising on code quality and commits.
No need to create the same custom components for frontend, just import them into the templates directory and it will auto-replicate.

In other words, this project is aimed at doing things in the best and laziest way possible.

---

## 📦 Supported Frameworks

| Framework     | Stack   | Extras                                             |
| ------------- | ------- | -------------------------------------------------- |
| FastAPI       | Python  | uv, black, flake8, isort, pre-commit               |
| Django        | Python  | uv, black, flake8, isort, pre-commit               |
| DRF           | Python  | uv, black, flake8, isort, pre-commit               |
| Next.js       | Node/TS | Tailwind, Prettier, ESLint, Pre-commit, Commitizen |
| Python (base) | Python  | Linter config, Git, pyproject.toml, etc.           |
| Python (CV)   | Python  | TODO                                               |

---

## 🚀 Usage & Installation

```bash
uv tool install pini

pini configure
pini create

# Follow the prompts and enjoy!
```

---

## 🧰 Templates

All configs live under the `/templates` directory:

- `.gitignore`
- `.pre-commit-config.yaml`
- `README.md.tmpl`
- `prettierrc`, `prettierignore`
- `ISSUE_TEMPLATES`
- More to come (_maybe_)

---

## 🛣️ Roadmap

- [ ] Add testing frameworks (pytest, vitest)
- [ ] Add optional Dockerfile defaults
- [ ] Improve Commitizen integration in JS flows
- [ ] CLI flags for silent mode / auto init
- [ ] Add more frameworks
- [ ] Add Dockerized database initialization (MySQL, PostgreSQL, Supabase)

---

## 🤝 Contributing

PRs welcome — just follow the code style and keep templates clean.

---

## 📜 License

MIT — do whatever you want, just don't make it worse 😄
