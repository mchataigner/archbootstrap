#!/bin/bash
[[ -s "$HOME/.profile" ]] && source "$HOME/.profile" || true # Load the default .profile

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" || true # Load RVM into a shell session *as a function*
