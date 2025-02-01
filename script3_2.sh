find $1 -name $2 -type f -perm -o=x -perm -u=r | xargs -I{} ./$3 {}
