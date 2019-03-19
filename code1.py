#!/usr/bin/python
"""
Create a list of all rings and their properties
output files:
	ring_list
	c1_coord
"""
import sys
import math 

atom = ['N1', 'C2', 'N3', 'C4', 'C5', 'C6', 'N7', 'C8', 'N9', "C1'"]		# List of all atoms whose coordinates should be extracted
nuc = ['G', 'C', 'A', 'U']		# List of the 4 possible bases in an RNA molecule
atom5 = ['C4', 'C5', 'N7', 'C8', 'N9']		# List of the atoms in the 5 membered ring of a purene
atom6 = ['N1', 'C2', 'N3', 'C4', 'C5', 'C6']		# List of the atoms in the 6 membered ring of a purene or a pyrimidine

atom_list=[]		
type_list=[]	# Contains the nucletide type (A, G, C or U)
ring_list=[]	# Contains the chain name
number_list=[]	# Contains the nucleotide number

# x, y and z-coordinates of the atom
xc_list=[]
yc_list=[]
zc_list=[]

filename=sys.argv[1]
fin = file(filename, 'r')
line=fin.readline()
while line!="":
	line=fin.readline()
	arr=line.split('\n')
	if line.startswith('ATOM'):
		if (arr[0][13:16].strip() in atom and arr[0][17:20].strip() in nuc):
			atom_list.append(arr[0][13:16].strip())
			type_list.append(arr[0][17:20].strip())
			ring_list.append(arr[0][21:22].strip())
			number_list.append(arr[0][23:27].strip())
			xc_list.append(arr[0][31:38].strip())
			yc_list.append(arr[0][39:46].strip())
			zc_list.append(arr[0][47:54].strip())
fin.close()

jlist=[]
nlist=[]
i=0
j=1
while (i<(len(xc_list))):
        if (number_list[i]==number_list[i-1]):
                j=j+1
        else:
                if (i!=0):
#			print j, number_list[i-1]
                        jlist.append(j)
                        nlist.append(number_list[i-1])
                        j=1
        i=i+1

wronglist=[]

i=0
while (i<len(jlist)):
	if (type_list[i] is 'A' or type_list[i] is 'G'):
       		if (jlist[i]!=10):
                	wronglist.append(nlist[i])
	if (type_list[i] is 'U' or type_list[i] is 'C'):
       		if (jlist[i]!=7):
                	wronglist.append(nlist[i])
        i=i+1

#print wronglist

i=0
while (i<len(xc_list)):
        if (number_list[i] in wronglist):
                del atom_list[i]
                del type_list[i]
                del ring_list[i]
                del number_list[i]
                del xc_list[i]
                del yc_list[i]
                del zc_list[i]
		continue
        i=i+1

#i=0
#while (i<len(type_list)):
#	print atom_list[i], type_list[i], ring_list[i], number_list[i]
#	i=i+1

# x, y and z-coordinates of the means of pyrimidines (U and C)
ucx=[]
ucy=[]
ucz=[]
# x, y and z-coordinates of the means of 5-membered rings of purenes (A and G)
ag5x=[]
ag5y=[]
ag5z=[]
# x, y and z-coordinates of the means of 6-membered rings of purenes (A and G)
ag6x=[]
ag6y=[]
ag6z=[]

# Calculate the mean
i=j=0
while i<len(type_list):
	x=y=z=x5=y5=z5=x6=y6=z6=0
#	print type_list[i], number_list[i],
	# if the nucletide is a pyrimidine then calculate mean of the ring
	if (type_list[i] is 'U' or type_list[i] is 'C' ):
#		print "enter uc"
		j=0
		while (j<7):
			if (atom_list[i] in atom6):
				x=x + float(xc_list[i])
				y=y + float(yc_list[i])
				z=z + float(zc_list[i])
			i=i+1
			j=j+1
		ucx.append(format(x/6, '.4f'))
		ucy.append(format(y/6, '.4f'))
		ucz.append(format(z/6, '.4f'))	
	# if nucleotide is a purene then calculate mean of 5 and 6-membered rings separately
	elif (type_list[i] is 'A' or type_list[i] is 'G' ):
#		print "enter ag"
		j=0
		while (j<10):
#			print i, j, atom_list[i], type_list[i], ring_list[i], number_list[i]
			if (atom_list[i] in atom5):
				x5=x5 + float(xc_list[i])
				y5=y5 + float(yc_list[i])
				z5=z5 + float(zc_list[i])
			if (atom_list[i] in atom6):
				x6=x6 + float(xc_list[i])
				y6=y6 + float(yc_list[i])
				z6=z6 + float(zc_list[i])
			i=i+1
			j=j+1
		ag5x.append(format(x5/5, '.4f'))
		ag5y.append(format(y5/5, '.4f'))
		ag5z.append(format(z5/5, '.4f'))
		ag6x.append(format(x6/6, '.4f'))
		ag6y.append(format(y6/6, '.4f'))
		ag6z.append(format(z6/6, '.4f'))

# x, y and z-coordinates of the position vectors of pyrimidines (U and C)
ucrx=[]
ucry=[]
ucrz=[]
# x, y and z-coordinates of the position vectors of 5-membered rings of purenes (A and G)
ag5rx=[]
ag5ry=[]
ag5rz=[]
# x, y and z-coordinates of the position vectors of 6-membered rings of purenes (A and G)
ag6rx=[]
ag6ry=[]
ag6rz=[]

# Calculate the position vectors = atom-coordinate - mean
i=j=0
uc_nuc_num=0
ag_nuc_num=0
while i<len(type_list):
	x=y=z=0
	# if the nucletide is a pyrimidine then calculate position vectors of all atoms in ring
	if (type_list[i] is 'U' or type_list[i] is 'C' ):
		j=0
		while (j<7):
			if (atom_list[i] in atom6):
				ucrx.append(format(float(xc_list[i])-float(ucx[uc_nuc_num]), '.4f'))
				ucry.append(format(float(yc_list[i])-float(ucy[uc_nuc_num]), '.4f'))
				ucrz.append(format(float(zc_list[i])-float(ucz[uc_nuc_num]), '.4f'))
			i=i+1
			j=j+1
		uc_nuc_num=uc_nuc_num+1
	# if nucleotide is a purene then calculate position vectors of all atoms in 5 and 6-membered rings separately
	elif (type_list[i] is 'A' or type_list[i] is 'G' ):
		j=0
		while (j<10):
			if (atom_list[i] in atom5):
				ag5rx.append(format(float(xc_list[i])-float(ag5x[ag_nuc_num]), '.4f'))
				ag5ry.append(format(float(yc_list[i])-float(ag5y[ag_nuc_num]), '.4f'))
				ag5rz.append(format(float(zc_list[i])-float(ag5z[ag_nuc_num]), '.4f'))
			if (atom_list[i] in atom6):
				ag6rx.append(format(float(xc_list[i])-float(ag6x[ag_nuc_num]), '.4f'))
				ag6ry.append(format(float(yc_list[i])-float(ag6y[ag_nuc_num]), '.4f'))
				ag6rz.append(format(float(zc_list[i])-float(ag6z[ag_nuc_num]), '.4f'))
			i=i+1
			j=j+1
		ag_nuc_num=ag_nuc_num+1

# x, y and z-coordinates of R1 and R2 of pyrimidines (U and C)
ucR1x=[]
ucR1y=[]
ucR1z=[]
ucR2x=[]
ucR2y=[]
ucR2z=[]
# x, y and z-coordinates of the R1 and R2 of 5-membered rings of purenes (A and G)
ag5R1x=[]
ag5R1y=[]
ag5R1z=[]
ag5R2x=[]
ag5R2y=[]
ag5R2z=[]
# x, y and z-coordinates of the R1 and R2 of 6-membered rings of purenes (A and G)
ag6R1x=[]
ag6R1y=[]
ag6R1z=[]
ag6R2x=[]
ag6R2y=[]
ag6R2z=[]

# To calculate mean plane of ring, calculate R1 and R2 of each ring
i=j=pu5=pu6=py=num=0
while i<len(type_list):
	x=y=z=x2=y2=z2=x5=y5=z5=x52=y52=z52=x6=y6=z6=x62=y62=z62=0
	# if the nucletide is a pyrimidine then calculate R1 and R2 of all atoms in ring
	if (type_list[i] is 'U' or type_list[i] is 'C' ):
		j=0
		while (j<7):
			if (atom_list[i] in atom6):
				if (atom_list[i] is 'N1'):
					num=0
				elif (atom_list[i] in 'C2'):
					num=1
				elif (atom_list[i] in 'N3'):
					num=2
				elif (atom_list[i] in 'C4'):
					num=3
				elif (atom_list[i] in 'C5'):
					num=4
				elif (atom_list[i] in 'C6'):
					num=5
				x=x+float(ucrx[py])*math.cos((6.28*(num))/6)
				y=y+float(ucry[py])*math.cos((6.28*(num))/6)
				z=z+float(ucrz[py])*math.cos((6.28*(num))/6)
				x2=x2+float(ucrx[py])*math.sin((6.28*(num))/6)
				y2=y2+float(ucry[py])*math.sin((6.28*(num))/6)
				z2=z2+float(ucrz[py])*math.sin((6.28*(num))/6)
				py=py+1		# Count the number of pyrimidines in the molecule
			j=j+1
			i=i+1
		ucR1x.append(format(x, '.4f'))
		ucR1y.append(format(y, '.4f'))
		ucR1z.append(format(z, '.4f'))
		ucR2x.append(format(x2, '.4f'))
		ucR2y.append(format(y2, '.4f'))
		ucR2z.append(format(z2, '.4f'))
	# if nucleotide is a purene then calculate R1 and R2 of all atoms in 5 and 6-membered rings separately
	elif (type_list[i] is 'G' or type_list[i] is 'A' ):		
		j=0
		while (j<10):
			if (atom_list[i] in atom5):
				if (atom_list[i] is 'C4'):
					num=0
				elif (atom_list[i] in 'C5'):
					num=1
				elif (atom_list[i] in 'N7'):
					num=2
				elif (atom_list[i] in 'C8'):
					num=3
				elif (atom_list[i] in 'N9'):
					num=4
				x5=x5+float(ag5rx[pu5])*math.cos((6.28*(num))/5)
				y5=y5+float(ag5ry[pu5])*math.cos((6.28*(num))/5)
				z5=z5+float(ag5rz[pu5])*math.cos((6.28*(num))/5)
				x52=x52+float(ag5rx[pu5])*math.sin((6.28*(num))/5)
				y52=y52+float(ag5ry[pu5])*math.sin((6.28*(num))/5)
				z52=z52+float(ag5rz[pu5])*math.sin((6.28*(num))/5)
				pu5=pu5+1	# Count the number of purenes in the molecule
			if (atom_list[i] in atom6):
				if (atom_list[i] is 'N1'):
					num=0
				elif (atom_list[i] in 'C2'):
					num=1
				elif (atom_list[i] in 'N3'):
					num=2
				elif (atom_list[i] in 'C4'):
					num=3
				elif (atom_list[i] in 'C5'):
					num=4
				elif (atom_list[i] in 'C6'):
					num=5
				x6=x6+float(ag6rx[pu6])*math.cos((6.28*(num))/6)
				y6=y6+float(ag6ry[pu6])*math.cos((6.28*(num))/6)
				z6=z6+float(ag6rz[pu6])*math.cos((6.28*(num))/6)
				x62=x62+float(ag6rx[pu6])*math.sin((6.28*(num))/6)
				y62=y62+float(ag6ry[pu6])*math.sin((6.28*(num))/6)
				z62=z62+float(ag6rz[pu6])*math.sin((6.28*(num))/6)
				pu6=pu6+1
			i=i+1
			j=j+1
		ag5R1x.append(format(x5, '.4f'))
		ag6R1x.append(format(x6, '.4f'))
		ag5R1y.append(format(y5, '.4f'))
		ag6R1y.append(format(y6, '.4f'))
		ag5R1z.append(format(z5, '.4f'))
		ag6R1z.append(format(z6, '.4f'))
		ag5R2x.append(format(x52, '.4f'))
		ag6R2x.append(format(x62, '.4f'))
		ag5R2y.append(format(y52, '.4f'))
		ag6R2y.append(format(y62, '.4f'))
		ag5R2z.append(format(z52, '.4f'))
		ag6R2z.append(format(z62, '.4f'))

# x, y and z-coordinates normals to mean plane of pyrimidines (U and C)
ucNx=[]
ucNy=[]
ucNz=[]
# x, y and z-coordinates normals to mean plane of 5-membered rings of purenes (A and G)
ag5Nx=[]
ag5Ny=[]
ag5Nz=[]
# x, y and z-coordinates normals to mean plane of 6-membered rings of purenes (A and G)
ag6Nx=[]
ag6Ny=[]
ag6Nz=[]

# Calculate normals to each mean plane N=R1XR2
# For pyrimidines (U and C)
i=0
while i<len(ucR1x):
	x=y=z=0
	x=float(ucR1y[i])*float(ucR2z[i])-float(ucR2y[i])*float(ucR1z[i])
	y=float(ucR2x[i])*float(ucR1z[i])-float(ucR1x[i])*float(ucR2z[i])
	z=float(ucR1x[i])*float(ucR2y[i])-float(ucR2x[i])*float(ucR1y[i])
	ucNx.append(format(x, '.4f'))
	ucNy.append(format(y, '.4f'))
	ucNz.append(format(z, '.4f'))
	i=i+1
# For 5-membered ring of purenes (A and G)
i=0
while i<len(ag5R1x):
	x=y=z=0
	x=float(ag5R1y[i])*float(ag5R2z[i])-float(ag5R2y[i])*float(ag5R1z[i])
	y=float(ag5R2x[i])*float(ag5R1z[i])-float(ag5R1x[i])*float(ag5R2z[i])
	z=float(ag5R1x[i])*float(ag5R2y[i])-float(ag5R2x[i])*float(ag5R1y[i])
	ag5Nx.append(format(x, '.4f'))
	ag5Ny.append(format(y, '.4f'))
	ag5Nz.append(format(z, '.4f'))
	i=i+1
# For 6-membered ring of purenes (A and G)
i=0
while i<len(ag6R1x):
	x=y=z=0
	x=float(ag6R1y[i])*float(ag6R2z[i])-float(ag6R2y[i])*float(ag6R1z[i])
	y=float(ag6R2x[i])*float(ag6R1z[i])-float(ag6R1x[i])*float(ag6R2z[i])
	z=float(ag6R1x[i])*float(ag6R2y[i])-float(ag6R2x[i])*float(ag6R1y[i])
	ag6Nx.append(format(x, '.4f'))
	ag6Ny.append(format(y, '.4f'))
	ag6Nz.append(format(z, '.4f'))
	i=i+1

#print ag6Nx

# Writing all values to the file ring_list
fout = file ('ring_list', 'w')
fout.write('nuc\tnum\t6/5\tring\tx0\ty0\tz0\tR1x\tR1y\tR1z\tR2x\tR2y\tR2z\tNx\tNy\tNz\n')

i=py=pu5=pu6=0
while i<len(type_list):
	i=i+1
	if (type_list[i] is 'U' or type_list[i] is 'C'):
		fout.write(type_list[i]+'\t'+number_list[i]+'\t6\t'+ring_list[i]+'\t'+ucx[py]+'\t'+ucy[py]+'\t'+ucz[py]+'\t'+ucR1x[py]+'\t'+ucR1y[py]+'\t'+ucR1z[py]+'\t'+ucR2x[py]+'\t'+ucR2y[py]+'\t'+ucR2z[py]+'\t'+ucNx[py]+'\t'+ucNy[py]+'\t'+ucNz[py]+'\n')
		py=py+1
		i=i+6
	elif (type_list[i] is 'G' or type_list[i] is 'A'):
		fout.write(type_list[i]+'\t'+number_list[i]+'\t6\t'+ring_list[i]+'\t'+ag6x[pu6]+'\t'+ag6y[pu6]+'\t'+ag6z[pu6]+'\t'+ag6R1x[pu6]+'\t'+ag6R1y[pu6]+'\t'+ag6R1z[pu6]+'\t'+ag6R2x[pu6]+'\t'+ag6R2y[pu6]+'\t'+ag6R2z[pu6]+'\t'+ag6Nx[pu6]+'\t'+ag6Ny[pu6]+'\t'+ag6Nz[pu6]+'\n')
		pu6=pu6+1
		fout.write(type_list[i]+'\t'+number_list[i]+'\t5\t'+ring_list[i]+'\t'+ag5x[pu5]+'\t'+ag5y[pu5]+'\t'+ag5z[pu5]+'\t'+ag5R1x[pu5]+'\t'+ag5R1y[pu5]+'\t'+ag5R1z[pu5]+'\t'+ag5R2x[pu5]+'\t'+ag5R2y[pu5]+'\t'+ag5R2z[pu5]+'\t'+ag5Nx[pu5]+'\t'+ag5Ny[pu5]+'\t'+ag5Nz[pu5]+'\n')
		pu5=pu5+1
		i=i+9
fout.close()

# Write the coordinates of C1 atom of all nucleotides to file c1_coord 
fout = file ('c1_coord', 'w')
fout.write('nuc\tx-coord\ty-coord\tz-coord\n\n')
i=0
while i<len(type_list):
	fout.write(number_list[i]+'\t'+xc_list[i]+'\t'+yc_list[i]+'\t'+zc_list[i]+'\n')
	i=i+1
	if (type_list[i] is 'U' or type_list[i] is 'C'):
		i=i+6
	elif (type_list[i] is 'G' or type_list[i] is 'A'):
		i=i+9
fout.close()
