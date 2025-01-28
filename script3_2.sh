find $1 -name $2 -type f -perm -o=x -perm -u=r | tee /dev/tty | xargs -I{} ./$3 {}
