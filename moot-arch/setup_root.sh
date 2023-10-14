#!/bin/bash

export CHROOT=$HOME/chroot/
export X64_CHROOT=$CHROOT/x86_64/root

mkarchroot -C /etc/pacman.conf -M /etc/makepkg.conf $X64_CHROOT base-devel
sudo -iu admin sudo -i cp /etc/pacman.conf $X64_CHROOT/etc/pacman.conf
sudo -iu admin sudo -i cp /etc/pacman.d/mirrorlist $X64_CHROOT/etc/pacman.d/mirrorlist
sudo -iu admin sudo -i cp /etc/makepkg.conf $X64_CHROOT/etc/makepkg.conf

arch-nspawn $X64_CHROOT pacman-key --recv-keys mathieu.chataigner@gmail.com
arch-nspawn $X64_CHROOT pacman-key --lsign-key mathieu.chataigner@gmail.com
arch-nspawn $X64_CHROOT pacman -Syu
