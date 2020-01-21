#  Data in News
##  Installation  and  Configuration

**Make  directory  called  newspaper_analysis.**


    $  mkdir  newspaper_analysis

**cd into  newspaper_analysis**


    $  cd  newspaper_analysis

**Clone  this  repository.**

    $  git  clone  {url}  newspaper_analysis


**Make** `**virtualenv**` **for  this  repo.**

Inside your newspaper_analysis directory

    $  virtualenv  --python=`which  python` env
    $  .env/bin/activate (Linux/ Mac)
    $  .env/scripts/activate (Linux/ Mac)

**Install  all  the  dependencies.**

    (env)  $  cd  newspaper_analysis
    (env)  $  pip  install  -r  requirements.txt

**Run  the  project**

    (newspaper_analysis)  $  export flask_app = "run.py"
    (newspaper_analysis)  $  flask run

##  AWS  Configurations

    WSGIPath:  run.py  

    Static  Directory:  newspaper_analysis/static/
