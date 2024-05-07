# Automated Roomba Routes
CSCI 724 - Survey of Artificial Intelligence final project.

## Running Our Project
1. Open a terminal or command prompt on your computer
2. Ensure that you have `pip` installed. If you do not, you can visit [this link](https://pip.pypa.io/en/stable/installation/) for installing `pip`.
3. Use pip to install Flask from your terminal.  
```
pip install flask
```
4. Download the project to your computer. You can do this via github or your terminal.
```
git clone https://github.com/benjaminrybacki/roomba_stuff.git
```
5. Navigate into the project directory.
```
cd roomba_stuff
```
6. Use Flask to run the project on a local port.
```
python app.py
```

## Troubleshooting
If at some point an issue persists from following the steps above, ensure that you are using commands specific to your operating system. The commands above will work with linux based machines.  
If you have downloaded the code through a different method than listed in steps 4 and 5,  you need to navigate to that directory (where you downloaded the code) within your terminal before running the command listed in step 6.  
If the command in step 6 does not work, check your python version with `python --version`. Sometimes re-running the command in step 6 with `python3` instead of `python` works.