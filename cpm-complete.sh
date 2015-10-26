_cpm_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _CPM_COMPLETE=complete $1 ) )
    return 0
}

complete -F _cpm_completion -o default cpm;
