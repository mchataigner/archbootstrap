#!/bin/bash
if [ -d $HOME/bin ];then
    export PATH=$PATH:$HOME/bin
fi
if [ -f $HOME/.rvm/scripts/rvm ]
then
    source $HOME/.rvm/scripts/rvm
fi
