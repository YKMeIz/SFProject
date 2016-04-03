#!/bin/sh

PVM_ROOT=/usr/share/pvm3

if [ "$PVM_RSH" = "" ]; then
	export PVM_RSH="/usr/bin/rsh"
fi

export PVM_ROOT

exec /usr/share/pvm3/lib/pvm "$@"
