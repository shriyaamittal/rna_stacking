for dir in *
do
echo $dir
echo $dir >> error.txt
./run_stacking.sh $dir/$dir 2>> error.txt
done

