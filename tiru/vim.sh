#!bin/bash

# "rY
cmd="python scratch.py | tiru -img -; python scratch.py"
tmux send-keys -t x.2 "$cmd &> ./vimp"  ENTER
cat < ./vimp

