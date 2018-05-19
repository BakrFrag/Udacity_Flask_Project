this application is:
    flask project that enable to show sciences and it branches and brief description about it can be accessed if user loged in or not 
project display examples:
      https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/
      modules/348776022975462/lessons/3487760229239847/concepts/36483886240923
project detailed:
     https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/348776022975462/
     lessons/3487760229239847/concepts/36310386700923
loged in user:
    create there owns branches 
    edit it
    delete it 
    display json format of thecatogries of science 
    display json format for there own branches 
content:
     templates folder conatining templates used in this project (all files in template is html files )
     login provide login with google to this app
     status include the status of user (loged in or loged out )
     home the main page for loged in users 
     public home main page for un loged in users 
     description display description of branches for loged in users and provide the ability to edit or delete the branche
     public description display the description of branche only 
     catogrey display the catogrey branches for loged in users
     public catogrey display the branches of catogey for not loged in users
     static folder 
     containg style sheets (all files in this folder is css files )
     home.css containing the style sheets for the home.html and publichome.html
     catogrey provide the stylesheet for the catogrey.html and publiccatogrey.html
     description provide stylesheets for description.html and public description.html
database_setup.py
      icreate the catogrey database and build table and thier relations 
default.py 
      intailze the tables on database.setup.py 
project.py
include the project itself 
libraries:
1.install python 2
2.install flask within command (pip install flask ) on windows 
3.install oauth2client within command (pip install oauth2client )on windows 
4.install sqlalachemy within command (pip install sqlalchemy) on windows 
5.install httplib2 within command (pip install httplib2)
6.other libriers like json , string , random , requests no need to install them (build in modules);

operating instructions:
 
install python 
open project.py file with idle and run it or press f5  
goto prefered webbrowser you use and paste localhost:5000 them the app will displayed 

 