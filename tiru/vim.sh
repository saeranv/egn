#!bin/bash

# "rY
fpath="scratch.py"
cp $fpath "temp.py"
if [[ $1 == "-img" ]]; then
    cmd="python scratch.py | tiru -img -"
else 
    # cmd1="nvim $fpath +':1,$ s/vlt.stream_plt(f)//g<CR>e temp.py<CR><ESC>'"
    cmd1="sed -i 's/vlt.stream_plt(f)//' temp.py" 
    cmd2="python temp.py"
    cmd="$cmd1 && $cmd2"

tmux send-keys -t x.2 "$cmd &> ./vimp"  ENTER
cat < ./vimp

