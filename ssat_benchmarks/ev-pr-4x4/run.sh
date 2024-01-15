FILES=*.ssat_log
for i in $FILES 
do 
    echo "$i"
    tail -10 $i
    echo ""
done
ls *.sdimacs | wc -l
ls *.ssat_log | wc -l
