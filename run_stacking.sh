#if [ -e "$1.pdb" ]
#then python code1_pdb.py "$1.pdb"
#else python code1_coor.py "$1_min.coor"
#fi

python code1.py "$1.pdb"
echo "code1 completed..."
python code2.py
echo "code2 completed..."
python code3.py
echo "code3 completed..."
mv ring_list "$1_ring_list"
mv c1_coord "$1_c1_coord"
mv parameters "$1_parameters"
mv stacked_bases "$1_stacked_bases"
mv nomen "$1_nomenclature"
