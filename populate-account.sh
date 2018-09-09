#!/bin/bash

cd /home/lumb/scripts/mastodon-ebooks-master/

X=0

python3 ./main.py

while [ $X -le 10 ]
do
    python3 ./gen.py

    NUM=$(echo $RANDOM % 60 + 1 | bc)

    #X=$($X+1)
    let "x++"

    sleep $NUM
done
 
