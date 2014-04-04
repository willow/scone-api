#!/bin/sh

# prevent `stdin: is not a tty` https://github.com/mitchellh/vagrant/issues/1673#issuecomment-26650102
sed -i 's/^mesg n$/tty -s \&\& mesg n/g' /root/.profile

# abort immediately on error
set -e

apt-get install dos2unix

apt-get update -y

apt-get install software-properties-common python-software-properties -y
apt-get install libxml2-dev libxslt-dev python-lxml -y
apt-get install binutils libproj-dev gdal-bin -y

apt-get install -y git

add-apt-repository ppa:fkrull/deadsnakes -y
apt-get update -y

apt-get install -y build-essential python python-dev python-setuptools python-pip
apt-get install -y python2.7-dev
apt-get install -y python3.4-dev

wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/postgresql.list'
apt-get update -y
apt-get install -y postgresql-9.3 pgadmin3
apt-get install -y libpq-dev

pip install virtualenv
pip install virtualenvwrapper

wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

cp /vagrant/vagrant/.bashrc /home/vagrant/.bashrc
dos2unix /home/vagrant/.bashrc
