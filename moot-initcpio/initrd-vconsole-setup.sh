#!/bin/bash

source /etc/systemd/system/initrd-build.sh

do_pack_keymap() {
    for cfg in /etc/{vconsole,locale}.conf; do
	[[ -s $cfg ]] && . "$cfg"
    done

    [[ $LANG ]] && LOCALE=$LANG
    LANG=$l

    if [[ $LOCALE = *[Uu][Tt][Ff]?(-)8 ]]; then
        run_command touch "/etc/mkinitcpio.d/keymap.utf8"
        uc=-u
    fi
    loadkeys -q $uc ${KEYMAP:-us} -b > /etc/mkinitcpio.d/keymap.bin
}
