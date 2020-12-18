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

    5. Copy `.env.example` to a `.env` file and update the variables within the file.
        
        1. An example would be: 
        
        ```
        SECRET_KEY=ThisSecretKeyThatShouldntBeShown
        FLASK_APP=vitality
        FLASK_ENV=development
        MONGO_URI=mongodb://localhost:27017
        MONGO_DATABASE=flask
        GOOGLE_MAPS_KEY=
        ```

    6. Double click `start_flask.bat` (windows) or `start_flask.sh` (linux/mac)
        1. Alternatively type `./start_flask.sh` (linux/mac)
        2. Or type `.\start_flask.bat` (windows)

    7. Go to browser and type http://localhost:8080/
   

--- 

**Proof of concept. Everything is subject to change.**
