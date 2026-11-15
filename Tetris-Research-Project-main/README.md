# Tetris-Research-Project

CS 534 Project Setup

Requires **Python 3.13 or newer**; gym-tetris will not install on older versions.


**macOS / Linux**
```
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python explore_env.py
```

**Windows PowerShell:**

python3.13 -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
python explore_env.py  


**This project uses gym-tetris as its environment**
Citation 
```tex
@misc{gym-tetris,
  author = {Christian Kauten},
  howpublished = {GitHub},
  title = {{Tetris (NES)} for {Gymnasium}},
  URL = {https://github.com/Kautenja/gym-tetris},
  year = {2019},
}