# Capstone-Project-3900-W18B-FantasticFive
Capstone-Project-3900-W18B-FantasticFive created by Ajay Arudselvam, Calvin Lau, Chowdhury Rubaiat Bin Mowla, Keerthivasan Gopalra, Shaun Zheng


## COMP3900 Computer Science Project Meal Recommendation System FantasticFive
                        
## Overview:

As society moves away from eating out and towards home cooking, there is an increased demand for recipes and cooking guides. An accumulation of many factors, especially increased health awareness, covid-19 and lockdowns, has led to a massive rise in home cooking with a 42% increase in individuals cooking more frequently (Sarda et al., 2022). Hence our application Food Nation aims to address this demand by providing a platform for users to find interesting recipes and providing a recommendation system to find recipes based on capabilities, methods, and meal types. Furthermore, with the rise of home-cooking there is a simultaneous rise in home chefs who are eager and excited to share recipes. Food Nation will allow all contributors to share and access other members' recipes and allow members to share feedback.

## Requirements and Versions 

- Python 3.9.2 
- Flask 1.1.2
- Werkzeug 1.0.1
- SQLAlchemy 1.3.22

## How to Run

### **Must be run using CSE vlab machines**

_Note: It is highly recommended to run the site on fullscreen within FireFox on vlab for the optimal experience_

1. Open up a terminal within the 'src' folder

```
$ cd src
```

2. Run the main.py

```
$ python3 main.py
```

3. Open up a web browser, specifically 'Firefox' on CSE vlab, full screen. 


4. Paste in the http link on which the server is running on, can be found on the terminal

```
http://127.0.0.1:5000/ 
```

5. Site should appear and user can navigate through it. Once loaded, see instuctions manual in final report.


6. If address already in user error occurs

```
OSError: [Errno 98] Address already in use
```

7. Open up main.py and change port number to another suitable port, rerun main.py till error no longer occurs.

```
app.run(port=5000)
```

