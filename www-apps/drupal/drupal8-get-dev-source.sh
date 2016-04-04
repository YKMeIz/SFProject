#/usr/bin/env bash

#
# Fedora Drupal 8 get dev source
#
# Usage: drupal8-get-dev-source.sh SPEC
#
# Gets a Drupal8 project's source from its' Drupal upstream git repo and
# creates an RPM *.tar.gz file.
#
# Requires the following from the source spec:
# - %global drupal8_project
# - %global drupal8_version || Version:
# - %global drupal8_commit
#
# Requires the following commands:
# - git
# - rpm (required to dynamically get the "%{_sourcedir}" RPM macro value)
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

#
# Functions
#

function print {
    echo -e "\e[0;32m>>>>> \e[0;33m${1}\e[0m"
}

function error {
    echo -e "\e[0;31mERROR: ${1}\e[0m" 1>&2
    exit 1
}

#
# Validate provided spec
#

SPEC=$1

# Spec provided?
if [[ ( $# -ne 1 ) || ( -z "$SPEC" ) ]]
then
    echo "Usage: ${0} SPEC" 1>&2
    exit 1
# Is provided spec a regular file?
elif [ ! -f "$SPEC" ]
then
    error "Spec file \"${SPEC}\" not found"
# Is spec file readable?
elif [ ! -r "$SPEC" ]
then
    error "Spec file \"${SPEC}\" is not readable"
fi

#
# Validate "git" and "rpm" commands are found
#

GIT=$(which git)
RPM=$(which rpm)

if [ -z "$GIT" ]
then
    error '"git" command not found'
elif [ -z "$RPM" ]
then
    error '"rpm" command not found'
fi

#
# Validate source information
#

DRUPAL8_PROJECT=`egrep '^\s*%global\s+drupal8_project\s+' "$SPEC" | awk '{print $3}'`

DRUPAL8_VERSION=$(egrep '^\s*%global\s+drupal8_version\s+' "$SPEC" | awk '{print $3}')
if [ -z "$DRUPAL8_VERSION" ]
then
    DRUPAL8_VERSION=$(grep '^Version:' "$SPEC" | awk '{print $2}')
fi

DRUPAL8_COMMIT=`egrep '^\s*%global\s+drupal8_commit\s+' "$SPEC" | awk '{print $3}'`

DRUPAL8_REPO=git://git.drupal.org/project/${DRUPAL8_PROJECT}.git

print "SPEC = $SPEC"
print "DRUPAL8_PROJECT = $DRUPAL8_PROJECT"
print "DRUPAL8_VERSION = $DRUPAL8_VERSION"
print "DRUPAL8_COMMIT = $DRUPAL8_COMMIT"
print "DRUPAL8_REPO = $DRUPAL8_REPO"

if [[ ( -z "$DRUPAL8_PROJECT" ) || ( -z "$DRUPAL8_VERSION" ) || ( -z "$DRUPAL8_COMMIT" ) ]]
then
    error 'Missing information'
fi

#
# Get source from upstream git repo and create *.tar.gz file
#

TEMP_DIR=$(mktemp --dir)

pushd $TEMP_DIR
    print 'Cloning git repo...'
    $GIT clone $DRUPAL8_REPO

    pushd $DRUPAL8_PROJECT
        print 'Checking out commit...'
        $GIT checkout $DRUPAL8_COMMIT
    popd

    TAR_FILE=$($RPM --eval='%{_sourcedir}')/${DRUPAL8_PROJECT}-8.x-${DRUPAL8_VERSION}-${DRUPAL8_COMMIT}.tar.gz
    print "TAR_FILE = $TAR_FILE"

    rm -f $TAR_FILE
    tar --exclude-vcs -czf $TAR_FILE $DRUPAL8_PROJECT
    chmod 0644 $TAR_FILE
popd

rm -rf $TEMP_DIR
