#!bin/bash

# "rY

FPATH="./scratch.py"
TEMP="./temp.py"

fn_image () {
    cat $FPATH | grep -q "print("
    if [[ $? -eq 0 ]]; then
        cmd1="cp $FPATH $TEMP"
        cmd2="sed -i 's/print(/vlt.null(/' $TEMP" 
        cmd3="python $TEMP | tiru -img -"
        cmd="$cmd1 && $cmd2 && $cmd3"
    else
        cmd="python $FPATH | tiru -img -"
    fi
    # tmux send-keys -t x.2 "$cmd &> /dev/null" ENTER 
    tmux send-keys -t x.2 "$cmd" ENTER 
}

fn_text () {
    cat $FPATH | grep -q "vlt.stream_plt("
    if [[ $? -eq 0 ]]; then
        # remove vlt.stream_plt, then execute
        cmd1="cp $FPATH $TEMP"
        cmd2="sed -i 's/vlt.stream_plt(/vlt.null(/' $TEMP" 
        cmd3="python $TEMP"
        cmd="$cmd1 && $cmd2 && $cmd3"
    else 
        cmd="python $FPATH"
    fi
    tmux send-keys -t x.2 "$cmd &> ./vimp" ENTER
    cat < ./vimp
}


cat $FPATH | grep -q "vlt.stream_plt"
# 0 means vlt.streamplt exists
tmux send-keys -t x.2 C-c
if [[ $? == 0 ]]; then
    fn_image &> /dev/null
    tmux send-keys -t x.2 C-c
    fn_text
 else 
    fn_text
fi 
tmux send-keys -t x.2 C-c

# don't delete, may be cause of crashing
# [[ -f $TEMP ]] && rm $TEMP


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


