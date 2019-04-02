# Item Catalogue - Udacity Project
### Author: Jack Holtby

## What is this?
A web application that displays a catalogue of items in a few different
predefined categories. Items can be created, deleted, and edited. These
functions are protected by authorisation and authentication using google
sign ins.

## Set up the environment

What to do in order to have an environment that will run the application.
The $ symbol is used to show command prompts. It is not part of commands.

* 1. Install Python (version 3).
If you're running linux, run:

$ apt install python3 python3-pip

If you're using Ubuntu then append "sudo" to the front of that command.
If you're using Windows or Mac you can find python through the following links:
https://www.python.org/downloads/mac-osx/
https://www.python.org/downloads/windows/

Installation instructions can be found here: https://wiki.python.org/moin/BeginnersGuide/Download.

* 2. Install VirtualBox
You can install virtualbox on debian based linux distros with:

$ apt install virtualbox

If you're running Debian unstable then you'll be getting VirtualBox version 6.1
or some such thing. This will not work with vagrant for some reason. You'll be
able to boot (from virtualbox, don't even try booting using "vagrant up"),
but the shared folders won't work. So I recommend installing on stable or
equivalent.

Get the old version that works from here: https://www.virtualbox.org/wiki/Download_Old_Builds_5_1

* 3. Install vagrant
You install vagrant to run the virtualbox system. You can find it here:
https://www.vagrantup.com/downloads.html

Or you can install it using apt if you're using a real operating system.

$ apt install vagrant

Add "sudo" if you're using Ubuntu or other derivatives.

You'll then need to download the configuration for the system that will run
on virtualbox and vagrant. This can be downloaded here:
https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip

Unzip this file into a directory of your choice. Enter the directory called
'vagrant' inside the directory you just unzipped. While inside the vagrant
directory, run the following command:

$ vagrant up

This will take quite some time to set up, depending on your internet connection.

* 4. Log into the vagrant os

You can log into the system with:

$ vagrant ssh

While logged in, you can find the data in the /vagrant folder.

If it is not there, see the next step.

## Set up the project files
Now you have an environment working, let's get the application set up.

* 1 Download the project
Go to: https://github.com/jackholtby/catalogue and click "Clone or Download."
Click on the "Download Zip" option that appears. Save it in the shared vagrant
directory that was created when you installed the vagrant machine. Unzip it
into that directory and you should have a directory called "Catalogue."

* 2 Setup the database
In a terminal, make sure you're inside the catalogue directory and you're
accessing it via ssh so you're running the python version that is on the
vagrant machine, not on your host machine. To create the database, run:

$ python database_setup.py

Then to populate the database, run:

$ python populate_database.py

And you're set.

* 3 Run it
Now you can run the application by running:

$ python project.py

And then access it via a browser on your host machine by entering
http://localhost:5000 in the address bar.

## Set it up with your own google web sign-in setup.

If you want to have your own google sign-in set up and not use mine, do the following.

1. Go to console.developers.google.com.

2. At the top left to the right of the word google, you should see a drop down menu
icon. Click on that and you should be able to create a project. Name it Catalogue.

3. You should now Have a page titled "Credentials." Click on the "Create Credentials"
dropdown menu, and click on "Oauth Client ID." Select Web App. It may first ask you to
configure the consent screen.

4. Configure the consent screen by putting in a name for the app (again, what?), and
then your email. After that it'll take you back and you'll be able to choose web app
for your application type.

5. When you create the Web app, fill in the section with "Authorized Javascript Origins"
with "http://localhost:5000". Under that in the "Authorized redirect URIs" put:
http://localhost:5000/
http://localhost:5000/login/
http://localhost:5000/gconnect/

Then click "Save"

6. You should now see an entry in the Oauth 2.0 client IDs list. Click on the download
button way down the right end. Save the file over the top of the client_secrets.json
which already exists in the catalogue folder. Then you should be set.

Run the application!
