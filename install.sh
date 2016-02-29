#!/bin/bash


APPHOME=`pwd`

export PATH=$PATH:$HOME/.local/bin
echo 'export PATH=$PATH:$HOME/.local/bin' >> $HOME/.bashrc
pip install --user --editable .
./generate-autocomplete.sh
echo ". $APPHOME/cpm-complete.sh" >> $HOME/.bashrc
echo "Python module installation complete"
echo "2 lines have been added to your .bashrc"
echo "To complete installation, please source your .bashrc after reviewing the newly added line"
