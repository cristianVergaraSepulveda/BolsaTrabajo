Ubuntu 10.10 Bootstrapping Instructions
=============

check [Ubuntu 10.10 bootstrapping instructions](https://github.com/vkhemlan/BolsaTrabajo/wiki/Ubuntu-10.10-Bootstrapping-Instructions)

Python
-------

	sudo apt-get install aptitude curl
	sudo aptitude install python2.7-dev python2.7-doc python2.7-examples
	curl -O https://github.com/pypa/pip/raw/master/contrib/get-pip.py
	sudo python get-pip.py

Virtualenv
-------
	sudo pip install virtualenv
	sudo pip install virtualenvwrapper
	mkdir ~/.virtualenvs

### Add this at the end of your ~/.bashrc:
	#Python + Virtualenv
	export WORKON_HOME=$HOME/.virtualenvs
	export PIP_VIRTUALENV_BASE=$WORKON_HOME # Tell pip to create its virtualenvs in $WORKON_HOME.
	export PIP_RESPECT_VIRTUALENV=true # Tell pip to automatically use the currently active virtualenv.
	export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python
	export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
	export VIRTUALENVWRAPPER_VIRTUALENV_ARGS="-p python2.7 --distribute --no-site-packages"

	# django bash completion
	. ~/.django_bash_completion

	source /usr/local/bin/virtualenvwrapper.sh

	# pip bash completion start
	_pip_completion()
	{
	    COMPREPLY=( $( COMP_WORDS="${COMP_WORDS[*]}" \
		           COMP_CWORD=$COMP_CWORD \
		           PIP_AUTO_COMPLETE=1 $1 ) )
	}
	complete -o default -F _pip_completion pip
	# pip bash completion end


###Create bolsa-trabajo virtualenv

	mkvirtualenv bolsa-trabajo

###Application Requirements

	curl http://code.djangoproject.com/export/16026/django/trunk/extras/django_bash_completion > ~/.django_bash_completion

	pip install --requirement=requirements.txt

###Django Configuration file

	ask for someone in the team for the settings.py file :)

###Django Initialization
	python manage.py syncdb
*don't create a superuser!

###Database Migrations
	python manage.py migrate bolsa_trabajo

###Create Superuser (whatever u want):
	python manage.py createsuperuser

###Run Django Server:
	python manage.py runserver

###Enter development site:
	http://localhost:8000/

###Windows 7 Bootstrapping Instructions
	pending
	
Server deployment
----------------------

The site is currently running on http://bolsatrabajo.cadcc.cl

To update the production application you need to enter to the server via SSH and execute 

    git pull
    service apache2 restart
    
The server is currently running Ubuntu Server 10.10 and may be migrated to CentOS at some point

The system does not execute any unit or integration tests.


