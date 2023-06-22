#!bin/bash

# "rY
cmd="python -m tiru.scratch"
cmd2="$cmd &> ./tiru/vimp"
tmux send-keys -t x.2 "$cmd2"  ENTER
cat < ./vimp

