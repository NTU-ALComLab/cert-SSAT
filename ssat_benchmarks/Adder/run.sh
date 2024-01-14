FILES=*.ssat_log
for i in $FILES 
do 
    echo "$i"
    tail -1 $i
done
ls *.sdimacs | wc -l
ls *.ssat_log | wc -l
