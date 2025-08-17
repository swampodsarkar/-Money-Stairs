# Safe Practice GUI Panel (Python + CustomTkinter)

A clean, modular Python GUI scaffold for practicing UI and simple simulations safely. No game integration.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app
```

## Project structure

```
app/
  __init__.py
  __main__.py
  main.py
  core/
    __init__.py
    config.py
    models.py
    simulation.py
  ui/
    __init__.py
    app.py
    views/
      sidebar_view.py
      playfield_view.py
assets/
```

## Notes
- This is a sandbox UI. Implement your own logic inside `app/core/` and wire it to views in `app/ui/views/`.
- Requires: Python 3.9+ and Tk available on your system.