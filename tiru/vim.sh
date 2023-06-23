#!bin/bash

# "rY

FPATH="./scratch.py"
FPATH_TEMP="./temp.py"

fn_text () {
    cmd="python $FPATH | tiru -img -"
    tmux send-keys -t x.2 "$cmd"  ENTER
}

fn_image () {
    cmd1="cp $FPATH $FPATH_TEMP"
    cmd2a="sed -i 's/vlt.stream_plt(f)//' $FPATH_TEMP" 
    cmd2b="sed -i 's/vlt.stream_plt(fig)//' $FPATH_TEMP" 
    cmd3="python $FPATH_TEMP"
    cmd="$cmd1 && $cmd2a && $cmd2b && $cmd3" 
    
    tmux send-keys -t x.2 "$cmd &> ./vimp"  ENTER
    cat < ./vimp
    rm $FPATH_TEMP
}


cat $FPATH | grep -q "vlt.stream_plt"
# 0 means vlt.streamplt exists
if [[ $? == 0 ]]; then
    fn_image &> /dev/null
    fn_text
else 
    fn_text
fi 

# if [[ $1 == "-img" ]]; then
#     cmd="python scratch.py | tiru -img -"
#     tmux send-keys -t x.2 "$cmd"  ENTER
# else 
#     cmd1="cp ./scratch.py ./temp.py"
#     cmd2="sed -i 's/vlt.stream_plt(f)//' ./temp.py" 
#     cmd3="python ./temp.py"
#     cmd="$cmd1 && $cmd2 && $cmd3" 
    
#     tmux send-keys -t x.2 "$cmd &> ./vimp"  ENTER
#     cat < ./vimp
#     rm ./temp.py
# fi 


