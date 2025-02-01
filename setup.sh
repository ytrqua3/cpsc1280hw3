
WD="a3_example"

if test -e  $WD;
then
   echo $WD already exist
   echo Remove with the command: rm -rf $WD
   echo before running this script.  
   echo Stopping....
   exit 1
fi

mkdir $WD
cd $WD
#Directories for pattern "T?a*b"
#included
mkdir -p idx/Tgaab
mkdir -p TTaomgb/Tgaaaacb
mkdir -p a/T/?abcdddc/TZadeb

#not included
mkdir -p Tbabb
mkdir -p www/MdfeadTaaab
mkdir -p zzz/omfts
mkdir -p ol/Toamwfbc

#Directories for pattern "?cat.fish??"
#included
mkdir -p oompa/1cat.fishes
mkdir -p loompas/scat.fisher
mkdir -p zoom/tcat.fished

#not included
#files from set 1.

#files for Question 2 for patter p*r.sh
mkdir mariko
echo pwd > mariko/protectdoor.sh  #included
chmod o+x,u+r mariko/protectdoor.sh 
echo pwd > mariko/presser.sh #included
chmod o+x,u+r mariko/presser.sh
echo pwd > mariko/pistols.sh #exluded
chmod o+x,u+r mariko/pistols.sh
echo pwd > mariko/poor.sh #exluded
chmod o-x,u+r mariko/poor.sh
echo pwd > mariko/potter.sh #exluded
chmod o+x,u-r mariko/potter.sh
echo pwd > mariko/pinner.sh #exluded
chmod o-x,u-r mariko/pinner.sh



