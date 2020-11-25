![Unittests and Dependencies Actions Status](https://github.com/santosderek/Vitality/workflows/Unittests-and-Dependencies/badge.svg)

![](vitality/static/images/heartlogo.png)


---

_Connecting trainers with trainees around the world, one workout at a time._

### Important! This is a senior project. We are not able to take outside help for this repo so pull requests from outside the group will not be accepted. Thank you for understanding. 

### Mission: 

Vitality, an all in one platform allowing users to connect to nearby trainers, schedule meetings, share workouts, and encourage healthy dieting. 

### Dependencies: 

Primarily written in Python 3.7.x, while using Flask as our webserver and PyMongo to connect to our Vitality database.

Please look at the `requirements.txt` file found in the root of our repo for the complete list of requirements.

### How to Launch:

- Online:
    
    1. Go to https://vitality.santosderek.com/

- Offline:

    1. Install Python 3.7.x or greater. https://www.python.org/downloads/
    
        1. Make sure to install Pip (a checkbox when installing) with python.
      
    2. Install MongoDB: https://www.mongodb.com/try/download/community
      
    3. Open a terminal and within the root folder of the vitality repo, next to `requirements.txt` run `pip3 install -r requirements.txt`.
    
        1. `sudo` might be needed at the beginning of the command if you need root privileges. 

    4. Make sure Mongod service is running locally and reachable.

    5. Double click start_flask.bat

    6. Go to browser and type http://localhost:8080/
   

--- 

**Proof of concept. Everything is subject to change.**
