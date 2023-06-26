
#!bin/bash
# "rY

FPATH="./test_analytic.py"
TEMP="./temp.py"

fn_image () {
    # cat $FPATH | grep -q "print("
    # if [[ $? -eq 0 ]]; then
    #     cmd1="cp $FPATH $TEMP"
    #     cmd2="sed -i 's/print(/vlt.null(/' $TEMP" 
    #     cmd3="python $TEMP | tiru -img -"
    #     cmd="$cmd1 && $cmd2 && $cmd3"
    # else
    #     cmd="python $FPATH | tiru -img -"
    # fi
    
    cmd="python $FPATH | tiru -img -"
    tmux send-keys -Rt bottom "$cmd" ENTER 
}

fn_text () {
    # cat $FPATH | grep -q "vlt.stream_plt("
    # if [[ $? -eq 0 ]]; then
    #     # remove vlt.stream_plt, then execute
    #     cmd1="cp $FPATH $TEMP"
    #     cmd2="sed -i 's/vlt.stream_plt(/vlt.null(/' $TEMP" 
    #     cmd3="python $TEMP"
    #     cmd="$cmd1 && $cmd2 && $cmd3"
    # else 
    #     cmd="python $FPATH"
    # fi
    cmd="python $FPATH" 
    tmux send-keys -Rt bottom "$cmd &> ./vimp" ENTER
    cat < ./vimp
}


tmux send-keys -Rt bottom C-c
fn_image &> /dev/null
fn_text


# python -m pytest --show-capture=stdout ./test_analytic.py::test_thermocouple

# cat $FPATH | grep -q "vlt.stream_plt"
# # 0 means vlt.streamplt exists
# tmux send-keys -Rt bottom C-c
# if [[ $? == 0 ]]; then
#     fn_image &> /dev/null
#     fn_text
# else 
#     fn_text
# fi 
# tmux send-keys -Rt bottom C-c
