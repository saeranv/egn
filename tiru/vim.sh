#!bin/bash

# "rY
cmd="ls ."
tmux send-keys -t x.2 "ls . 2>&1 vimp" ENTER
cat < vimp

