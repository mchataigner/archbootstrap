#!/bin/bash

install_required_packages() {
	pacman -Syu --noconfirm --needed base base-devel linux-tools git python curl ca-certificates-utils zsh
	update-ca-trust
}

install_required_packages
mv /etc/pacman.conf{,.old}
curl -o /etc/pacman.conf https://raw.githubusercontent.com/mchataigner/archbootstrap/master/pacman.conf
curl -o bootstrap.py https://raw.githubusercontent.com/mchataigner/archbootstrap/master/bootstrap.py
python bootstrap.py "$@"
