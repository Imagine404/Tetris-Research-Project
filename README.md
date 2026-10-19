# Tetris-Research-Project

CS 534 Project Setup

We recommend using a virtual environment to manage dependencies for this project. We can verify that this project functions properly with python version CPython 3.13 and 3.14 in CI. Other python versions may work, but we have not verified this. If you run into problems using a different python version, we recommend switching the version to CPython 3.13 and 3.14 in CI. using pyenv (or pyenv-win for Windows). You can create and activate a virtual environment using the following commands from the project root directory:

python -m venv .venv
source .venv/bin/activate

Or on Windows PowerShell:

python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1


Now that your virtual environment is activated (you should see (.venv) at the beginning of your command line), install the required dependencies using pip:

pip install -r requirements.txt
Now when running any of the Jupyter notebooks, ensure that you select the virtual environment as your kernel. You should have no problems importing the necessary libraries.



Citation 
```tex
@misc{gym-tetris,
  author = {Christian Kauten},
  howpublished = {GitHub},
  title = {{Tetris (NES)} for {Gymnasium}},
  URL = {https://github.com/Kautenja/gym-tetris},
  year = {2019},
}