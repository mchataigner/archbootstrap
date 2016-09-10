#!/bin/bash

sudo pacman -Syu --needed base base-devel curl wget
git clone https://github.com/mchataigner/archbootstrap.git
pushd archbootstrap
git submodule update --init
pushd package-query
makepkg -si
popd
pushd yaourt-moot
makepkg -si
popd
yaourt -Pi prezto-moot
yaourt -Pi moot-base
