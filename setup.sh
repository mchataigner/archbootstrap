#!/bin/bash

sudo pacman -Syu --needed base base-devel linux-tools git autoconf make m4 yajl curl wget
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
yaourt -Pi moot-common
