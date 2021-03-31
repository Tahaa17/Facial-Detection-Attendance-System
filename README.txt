PLEASE NOTE: Visual Studio C++ Development Environment MUST be installed for our program to run and for dependencies to be installed!!!

THIS PROGRAM RELIES ON PYTHON3, PLEASE ENSURE YOU HAVE THIS VERSION OF PYTHON INSTALLED

IT IS RECOMMENDED THAT ALL DEPENDENCIES ARE INSTALLED IN A VIRTUAL ENVIRONMENT FOR PYTHON, PLEASE REFER TO THE FOLLOWING VIDEO ON SETUP INSTRUCTIONS:

https://www.youtube.com/watch?v=APOPm01BVrk&ab_channel=CoreySchafer

1. Copy the GitHub Repository above and save it to a local directory or extract given source code to a local directory and set up a virutalenv in this directory
2. After you've ensured Visual Studio C++ Development Environment is installed, navigate to your virtual environment and run pip3 install cmake
3. Run the following command: pip3 install dlib, NOTE: this may take a while and is very cpu intensive
4. Run the following command: pip3 install face-recognition
5. Run the following command: pip3 install -r requirements.txt
6. If all these commands ran without error, all dependecies have been installed, you can now run the program by running the following command: py menu.PYTHON
7. After you see the message " Running on http://127.0.0.1:5000/ " you can navigate to your browser and go to localhost:5000 and you will be navigated to our web application

IMPORTANT NOTE: Currently our Amazon RDS Server has restricted access to only a few white listed ip addresses, 
if you would like to gain access to the server to run our program please email jayash.singh@ontariotechu.net with your public ip address and access will be granted.