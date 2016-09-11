#!/bin/bash

install_required_packages() {
	pacman -Syu --noconfirm
	pacman -S --noconfirm --needed base
	pacman -S --noconfirm --needed base-devel
	pacman -S --noconfirm --needed linux-tools
	pacman -S --noconfirm --needed git python curl
}

install_required_packages
curl -o bootstrap.py https://raw.githubusercontent.com/mchataigner/archbootstrap/master/bootstrap.py
curl -o /etc/sudoers.d/tmp_admin https://raw.githubusercontent.com/mchataigner/archbootstrap/master/moot-base/admin_sudoers
chown root:root /etc/sudoers.d/admin
chmod 440 /etc/sudoers.d/admin
python bootstrap.py
