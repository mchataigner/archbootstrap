echo $(date) .zprofile > $HOME/login
systemctl --user status awesome.target &> /dev/null || systemctl --user start awesomeexit.target

