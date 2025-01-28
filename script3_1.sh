find -L $1 -name $2 -type d  -exec ls -dli {} \;| awk '{print $1 " " $2 " "  $10}' | tee /dev/tty | cat >> $3
