#!/bin/bash

postgres_dep () {
	#lsb_id=`lsb_release -i | awk '{print $3}'`
	echo "Installing postgresql....."
	if [ -f /etc/lsb-release ] || [ -f /etc/debian_version ]; then 
		echo "Detected OS as Ubuntu $(lsb_release -r)"
		sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
		wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
		sudo apt-get update
		sudo apt-get -y install postgresql
	elif [ -f /etc/fedora-release ]; then
		echo "Detected OS as Fedora $(lsb_release -r)"
		sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/F-34-x86_64/pgdg-fedora-repo-latest.noarch.rpm
		sudo dnf install -y postgresql13-server
		sudo /usr/pgsql-13/bin/postgresql-13-setup initdb
		sudo systemctl enable postgresql-13
		sudo systemctl start postgresql-13
	elif [ -f /etc/redhat-release ]; then 
		echo "Detected OS as RedHat $(lsb_release -r)"
		sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
		sudo dnf -qy module disable postgresql
		sudo dnf install -y postgresql13-server
		sudo /usr/pgsql-13/bin/postgresql-13-setup initdb
		sudo systemctl enable postgresql-13
		sudo systemctl start postgresql-13
	else
		echo "Operating system does not support PostgreSQL"
	fi
} 

main () {
	echo "Hello, this installer will install the necessary dependencies for URLshortner"
	sudo apt update
	echo "Upgrading python....."
	sudo apt install python3
	if ![ command -v pip3 &> /dev/null ]; then
		echo "Installing python3-pip....."
		sudo apt -y install python3-pip
	fi
	echo "Installing database dependencies....."
	echo -e "Which database do you want?\n1)Postgresql\n2)SQLite"
	read -p "Enter choice(1/2): " type
	if [ $type -eq 1 ]; then
		if [ $(read -p "1)Do you want to install PostgreSQL or 2)point the app to an external server(1/2): ") -eq 1 ]; then
			postgres_dep
		fi
		echo "Installing python interface for postgresql...."
		pip3 install psycopg2-binary
	elif [ $type -eq 2 ]; then
		echo "SQLite will be installed along with Flask"
	fi
	echo "Installing Flask....."
	pip3 install Flask
	./setup.py $type
	echo "Installation and setup is done!!!"
	echo "You can launch the web app by starting it as in $ python3 main.py"
}

main
