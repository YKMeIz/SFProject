#!/bin/sh

export PVM_ROOT=/usr/share/pvm3
export XPVM_ROOT=/usr/share/pvm3/xpvm
export PVM_DPATH=/usr/share/pvm3/lib/pvmd

ARCH=`uname -i | tr [a-z] [A-Z]`
PVM_ARCH=LINUX$ARCH

export PATH=$PATH:$PVM_ROOT/bin/$PVM_ARCH

$PVM_ROOT/bin/$PVM_ARCH/xpvm "$@"
