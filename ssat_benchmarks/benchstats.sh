dirlist=*

for dir in $dirlist
do
  if  [ -d  $dir  ]; then
        cd $dir
        echo "${dir}, \c" 
        ls *.sdimacs | wc -l
        cd ..
  fi
done


