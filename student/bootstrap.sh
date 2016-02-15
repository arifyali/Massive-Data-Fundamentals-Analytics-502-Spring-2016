#!/usr/bin/bash
#
# bootstrap script for S3 clusters
pip install mrjob
if [ -d /home/hadoop ]; then
  cat >> /home/hadoop/.bashrc <<EOF
export HADOOP_HOME=/usr/lib/hadoop
EOF
  cat >> /home/hadoop/.mrjob.coonf <<EOF
runners:
  inline:
    strict_protocols: true
  local:
    hadoop_bin: /usr/bin/hadoop
    strict_protocols: true
  hadoop:
    strict_protocols: true
EOF
fi


