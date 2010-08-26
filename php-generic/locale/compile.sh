#!/bin/bash

lockfile="/tmp/compile-po.lock"

if [ ! -e $lockfile ]
then
    touch $lockfile
    locale_root=`dirname $0`
    echo "Compiling all locales..."
    for i in `find $locale_root -type f -name "messages.po"`; do
        dir=`dirname $i`
        stem=`basename $i .po`
        echo -n "Compiling ${i} ... "
        msgfmt -o ${dir}/${stem}.mo $i
        echo "done"
    done
    echo "All done."
    rm $lockfile
else
    echo "$lockfile present, exiting"
    exit 99
fi
