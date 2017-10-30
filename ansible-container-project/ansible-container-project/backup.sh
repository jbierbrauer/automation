#!/bin/bash
cp -r /root/ansible-container-project /home/jbierbrauer/automation/ansible-container-project
cd /home/jbierbrauer/automation
git add ansible-container-project
git commit -m autobackup
git push

