#!/bin/bash
cd /etc/drupal
for i in `ls -1`; do
mv $i/files /var/lib/drupal/files/$i
/sbin/restorecon /var/lib/drupal/files/$i
ln -s /var/lib/drupal/files/$i /etc/drupal/$i/files
done
