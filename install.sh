#!/bin/bash


APPHOME=$(cd `dirname $0` && pwd)


if [ -z `which pip` ] ; then
	echo 	"Pip (python install tool) is not installed. You can install it with apt-get install python-pip"
	exit 1
fi

mkdir -p $HOME/.config
mkdir -p $HOME/.local/bin

cd $APPHOME
cp $APPHOME/default.conf $HOME/.config/cpm.conf

export PATH=$PATH:$HOME/.local/bin
echo 'export PATH=$PATH:$HOME/.local/bin' >> $HOME/.bashrc
pip install --user --editable .

if [ -z `which cpm` ] ; then
	echo "Installation failed, maybe you are missing the library python-dev (needed to build python-zmq if missing)."
	echo "You can install it with apt-get install python-dev"
	exit 1
fi

./generate-autocomplete.sh
echo ". $APPHOME/cpm-complete.sh" >> $HOME/.bashrc
echo "Python module installation complete"
echo "2 lines have been added to your .bashrc"
echo "To complete installation, please source your .bashrc after reviewing the newly added line"
