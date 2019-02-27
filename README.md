# Thunderhead Monkeys
### _**Cloudtopus Cloud Learning Environment**_

--------------------------------------------------------------------------------

**Introduction**

Cloudtopus makes it easy for you to access, track, and analyse students progress on external learning tools. You can configure tools such as Trailhead, Telegram for facilitating your teaching courses beyond classroom learning materials. The platform serves as a monitoring dashboard for faculty and students to compare student progress within the class. It also comes with an IT operations manager lab which can be used for learning the operation stages in DEVOPS.

**Quick start-up**

Follow steps from Setting up Application:

 5. Setup up dependencies: 
 6. Deploy webpage on local server (To-do):
 
**About**

The project follows Django Model-View-Template framework.

--------------------------------------------------------------------------------

Data Model

    MYSQL 
    Data are split into two Databases.
        *Cle_Data
        *App_data

--------------------------------------------------------------------------------

Views

    Main modules include:
        * Module Account
            Functionalies on login and logout 
        * Module Deployment Monitoring
            Module on functionalities on 
                1) Deployment Environment sharing
                2) AWS Server monitoring via CloudWwatch
                3) Sharing of Deployment Packages
                4) Storing AWS Credentials
        * Module Event Configuration
            Functionalies on Asynchronous tasks 
                1) AWS Server shut down
                2) AWS Web application shut down
                3) Event Recovery Log
        * Module Communication Management
            Functionalies on Telegram 
        * Module Team Management 
            Module on functionalities on 
                1) Users, mainly student and faculty
                2) Cloud learning tools (Trailhead, Trailmix, Telegram)
                3) Setting up on courses

--------------------------------------------------------------------------------

Template

    Main templates are categorized into:
        * Instructor, Student, Admin

--------------------------------------------------------------------------------


**Setup**

Below is an indication of the basic dependencies that is needed on the server for it to run Cloudtopus properly.

###### Base Environment:
* MySQL
* Python
* Git
* Redis
* Nginx 
* Gunicorn

--------------------------------------------------------------------------------

**Instructions (Setting up Server)**
###### 1. SSH into server (TO-DO):

MAC:

Navigate to the folder where you store your key pair that you've downloaded from AWS (i.e. 'CLE.pem') and run these set of commands to ssh into your server.

    $ chmod 400 <key_pair_name>.pem
    $ ssh -i "<key_pair_name>.pem" ec2-user@<public_dns>

WINDOWS:

    Install putty.exe, puttygen.exe
    Convert the <key_pair_name>.pem to a pkk file
        Having a keyphrase is optional but is highly recommended.
    SSH via putty.exe

###### 2. Install dependencies:

    $ sudo -s
    $ yum update
    $ yum install <package name>

List of packages to install on server:

 - python36.x86_64
 - python36-devel.x86_64
 - python36-libs.x86_64
 - python36-pip.noarch
 - python36-setuptools.noarch
 - python36-test.x86_64
 - python36-tools.x86_64
 - python36-virtualenv.noarch
 - mysql55.x86_64
 - mysql55-bench.x86_64
 - mysql55-devel.x86_64
 - mysql55-embedded.x86_64
 - mysql55-embedded-devel.x86_64
 - mysql55-libs.x86_64
 - mysql55-server.x86_64
 - mysql55-test.x86_64
 - git.x86_64
 - gcc

###### 3. Linking pyton, pip and virtualenv:

    $ cd/usr/bin
    $ unlink python
    $ unlink pip
    $ unlink virtualenv
    $ ln -s python36 python
    $ ln -s pip-3.6 pip
    $ ln -s virtualenv-3.6 virtualenv
    $ exit

###### 4.Installing webserver and WSGI Gunicorn
    $ sudo yum instlal nginx
    $ sudo -s
    $ python -m pip install gunicorn

--------------------------------------------------------------------------------

**Instructions (Setting up Database)**
###### 1. Initializing database:

    $ sudo -s
    $ chkconfig mysqld on
    $ service mysqld start
    $ mysqladmin -u root password cle12345
    $ exit

###### 2. Create schemas:

    $ mysql -u root -p
    mysql> CREATE DATABASE CLE_Data
    mysql> CREATE DATABASE App_Data

--------------------------------------------------------------------------------

**Instructions (Setting up Application)**
###### 1. Set up folders for repository:

    $ mkdir Django_App
    $ cd Djano_App

###### 2. Set up virtual environment:

    $ virtualenv CLE_Env
    $ cd CLE_Env
    $ . bin/activate

###### 3. Clone repository:

    $ git clone https://github.com/joeltaydy/MayhemFive.git
    $ cd MayhemFive/CLE

###### 4. Install dependencies:

    $ pip install -r requirements.txt
    $ cd ..
    $ cd bin
    $ sh install_redis.sh
    $ sh start_redis_server.sh

###### 5. Setup up dependencies: 

    $ redis-server --daemonize yes
    $ screen
    $ sh start_celery_worker.sh

Keyboard command: ctrl + A + D - To exit screen without terminating it

    $ screen
    $ sh start_celery_task.sh

Keyboard command: ctrl + A + D - To exit screen without terminating it

    $ screen
    $ python manage.py process_tasks
    
Keyboard command: ctrl + A + D - To exit screen without terminating it

###### 6. Deploy webpage on local server (To-do):

    $ cd CLE
    $ python manage.py migrate
    $ python manage.py migrate Module_TeamManagement --database=CLE_Data
    $ python manage.py migrate Module_DeploymentMonitoring --database=CLE_Data
    $ python manage.py migrate Module_EventConfig --database=CLE_Data
    $ sudo service nginx start
    $ gunicorn CLE.wsgi:application
    
Keyboard command: ctrl + A + D - To exit screen without terminating it


## Acknowledgments

Team Thunderhead Monkeys created Cloudtopus as a SMU School of Information Systems Final Year Project. 

This would not have been possible without the mentorship and ideation of:

* Professor Rafael J. Barros
   (Singapore Management University, Senior Lecturer of Information Systems)
