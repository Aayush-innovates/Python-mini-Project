# LogicFlow
**Interactive Digital System Design Learning Platform**

> Learn Logic. Visualize Circuits. Master DSD.

## Quick start (Windows)

Double-click **`run.bat`**  
or in PowerShell:

```powershell
cd LogicFlow
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

Open the URL shown (usually http://localhost:8501).

## Setup (first time)

```powershell
cd LogicFlow
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Features

1. **Learn DSD** — gates, Boolean laws, SOP/POS, minterms/maxterms, K-map basics  
2. **Logic Gate Simulator** — AND, OR, NOT, NAND, NOR, XOR, XNOR with live I/O + truth tables  
3. **Boolean Expression Solver** — parse, truth table, SymPy simplification, SOP  
4. **Karnaugh Map Solver** — 2/3/4-variable maps, auto-grouping, simplified SOP  
5. **Quiz & Practice** — topic MCQs + numerical questions with session scoring  

No database, login, or persistent storage.

## Tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest -q
```

## Project structure

```
LogicFlow/
├── app.py                 # Dashboard
├── run.bat                # One-click launcher (Windows)
├── requirements.txt
├── README.md
├── pages/                 # Streamlit multipage UI
├── modules/               # Pure Python logic
├── components/            # Theme + visualizations
└── tests/                 # pytest
```

## Tech stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.11+ |
| UI | Streamlit |
| Boolean algebra | SymPy |
| Visualizations | HTML / SVG |
| State | Streamlit Session State |
| Testing | pytest |
