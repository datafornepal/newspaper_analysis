# Readme
Installation and Configuration


1. Create a directory named newspaper. 
        mkdir newspaper
2. Get in the directory 
        cd newspaper
3. Clone this repo. 
          git clone {repo_url}
4. Create a virtual environment inside the folder 
          python -m venv env  
5. Activate the virtual environment 
        . env/bin/activate  [MAC/LINUX]
        . env/scripts/activate   [Windows]
6. Install all dependencies 
        pip install -r “requirements.txt”
7. Run flask 
        export FLASK_APP=”run.py”
        flask run
8.  Sometimes, the project may not run. This is because nltk library is missing. To install it open terminal 
        import nltk 
        nltk.download()



         
    




    

