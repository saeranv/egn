#!bin/bash

# "rY
cmd="python scratch.py"
tmux send-keys -t x.2 "$cmd 2>&1 vimp" ENTER && cat < vimp
