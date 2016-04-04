#!/usr/bin/env bash

#
# Fedora Drupal 8 prep licenses and docs
#
# - Moves common licenses and docs into .rpm/{licenses,docs}/ respectively
# - Provides licenses and docs file list ".rpm/licenses-and-docs.txt"
#   which can be used in spec files as "%files -f .rpm/licenses-and-docs.txt"
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

[ -d .rpm ] || mkdir .rpm

# Licenses
rm -rf .rpm/licenses
mkdir .rpm/licenses
for LICENSE_FILENAME in LICENSE COPYING COPYRIGHT
do
    for LICENSE in $(find . -type f -iregex ".*/${LICENSE_FILENAME}\(\.\(md\|rst\|txt\)\)?\$")
    do
        DIR=$(dirname "$LICENSE")
        mkdir -p .rpm/licenses/${DIR}
        mv "$LICENSE" .rpm/licenses/${DIR}/
    done
done

# Docs
rm -rf .rpm/docs
mkdir .rpm/docs
for DOC_FILENAME in AUTHORS CHANGELOG CHANGES INSTALL MAINTAINERS README TESTING UPGRADE
do
    for DOC in $(find . -type f -iregex ".*/${DOC_FILENAME}\(\.\(md\|rst\|txt\)\)?\$")
    do
        DIR=$(dirname "$DOC")
        mkdir -p .rpm/docs/${DIR}
        mv $DOC .rpm/docs/${DIR}/
    done
done
for COMPOSER in $(find . -name "composer.*")
do
    DIR=$(dirname "$COMPOSER")
    mkdir -p .rpm/docs/${DIR}
    mv $COMPOSER .rpm/docs/${DIR}/
done

# Licenses and docs files list
rm -f .rpm/licenses-and-docs.txt
touch .rpm/licenses-and-docs.txt
[ $(find .rpm/licenses/ -type f | wc -l) -ge 1 ] && \
    echo "%license .rpm/licenses/*" >> .rpm/licenses-and-docs.txt
[ $(find .rpm/docs/ -type f | wc -l) -ge 1 ] && \
    echo "%doc .rpm/docs/*" >> .rpm/licenses-and-docs.txt

# Ensure no executable files
for EXECUTABLE_FILE in $(find .rpm/{licenses,docs}/ -type f -executable)
do
    chmod a-x "${EXECUTABLE_FILE}"
    echo "NOTICE: License or doc file \"${EXECUTABLE_FILE}\" was executable and should be fixed upstream" \
        | sed 's#\.rpm/\(licenses\|docs\)/##' 1>&2
done

# Verbose output for logging...
echo "+ find .rpm/{licenses,docs}/ | sort"
find .rpm/{licenses,docs}/ | sort
echo "+ cat .rpm/licenses-and-docs.txt"
cat .rpm/licenses-and-docs.txt
