#!/usr/bin/python
"""
Deals with base-base parameters (shift, slide, rise, roll, tilt and twist)
output files:
        parameters
        stacked_bases
"""
import math

nuc_list=[]	# Nucleotide type (A, G, C or U)
num_list=[]
ring_list=[] 	# 6 or 5-membered ring
chain_list=[]	
# x, y and z-coordinates of the mean of the ring
x0_list=[]
y0_list=[]
z0_list=[]
# x, y and z-coordinates of R1 and R2 of each ring
R1x_list=[]
R1y_list=[]
R1z_list=[]
R2x_list=[]
R2y_list=[]
R2z_list=[]
# x, y and z-coordinates of normal to each ring
Nx_list=[]
Ny_list=[]
Nz_list=[]

# Take file create by code1 'ring_list' as input
fin=open('ring_list', 'r')
for line in fin:
	columns = line.split('\t')
	columns = [col.strip() for col in columns]
	nuc_list.append(columns[0])
	num_list.append(columns[1])
	ring_list.append(columns[2])
	chain_list.append(columns[3])
	x0_list.append(columns[4])
	y0_list.append(columns[5])
	z0_list.append(columns[6])
	R1x_list.append(columns[7])
	R1y_list.append(columns[8])
	R1z_list.append(columns[9])
	R2x_list.append(columns[10])
	R2y_list.append(columns[11])
	R2z_list.append(columns[12])
	Nx_list.append(columns[13])
	Ny_list.append(columns[14])
	Nz_list.append(columns[15])

fin.close()
pm1=pm2=pm3=0 # The values in file 'param'
# Read file 'param' to input the values accroding to which stacking rings will be shortlisted 
i=0
fin=open('param', 'r')
for line in fin:
	i=i+1
	if (i==5):
		columns = line.split('\t')
		columns = [col.strip() for col in columns]
	       	pm1=columns[1]
		pm1=float(pm1)
	if (i==6):
		columns = line.split('\t')
		columns = [col.strip() for col in columns]
	       	pm2=columns[1]
		pm2=float(pm2)	
	if (i==7):
		columns = line.split('\t')
		columns = [col.strip() for col in columns]
	       	pm3=columns[1]
		pm3=float(pm3)
fin.close()

def dot_prod(a, b):
	return float(a)*float(b)

def cal_mod(a, b, c):
	return math.sqrt(float(a)*float(a)+float(b)*float(b)+float(c)*float(c))

def angle(a, b, c, d, e, f):	# Calculate angle between two vectors, (ax+cy+ez) and (bx+dy+fz)
	x=dot_prod(a, b)
	y=dot_prod(c, d)
	z=dot_prod(e, f)
	modi=cal_mod(a, c, e)
	modj=cal_mod(b, d, f)
	return format(math.degrees(math.acos(((x+y+z)/modi)/modj)), '.4f')

# x, y and z coordinates of the distance between two rings
dijx=[]
dijy=[]
dijz=[]
distance=[] # distance between the two rings

# Calculate distance
i=1
while i<len(nuc_list):
	j=i+1
	while j<len(nuc_list):
		if (num_list[i]==num_list[j]):
			j=j+1
		if (j==len(nuc_list)):
			break
		dijx.append(float(x0_list[j])-float(x0_list[i]))
		dijy.append(float(y0_list[j])-float(y0_list[i]))
		dijz.append(float(z0_list[j])-float(z0_list[i]))
		x=cal_mod(float(x0_list[j])-float(x0_list[i]), float(y0_list[j])-float(y0_list[i]), float(z0_list[j])-float(z0_list[i]))
		distance.append(format(x, '.4f'))
		j=j+1
	i=i+1
# Calculate a few angles
thetaij=[]
taui=[]
tauj=[]
phi1ij=[]
phi2ij=[]
psii1=[]
psii2=[]
psij1=[]
psij2=[]

newcount=[]
# thetaij=Ni.Nj
count=0
i=1
while i<len(nuc_list):
	j=i+1
	while j<len(nuc_list):
#		print i, j, Nx_list[i], Nx_list[j], Ny_list[i], Ny_list[j], Nz_list[i], Nz_list[j]
		if (num_list[i]==num_list[j]):	# i and j should not be same
			j=j+1
		if (j==len(nuc_list)):
			break
		if (float(distance[count])<pm1 and float(distance[count])>-pm1 and count<len(distance)):
			newcount.append(count)
			a=angle(Nx_list[i], Nx_list[j], Ny_list[i], Ny_list[j], Nz_list[i], Nz_list[j])		# thetaij= Ni.Nj
			thetaij.append(a)
			a=angle(Nx_list[i], dijx[count], Ny_list[i], dijy[count], Nz_list[i], dijz[count])	# taui= Ni.dij
			taui.append(a)
			a=angle(Nx_list[j], dijx[count], Ny_list[j], dijy[count], Nz_list[j], dijz[count])	# tauj= Nj.dij
			tauj.append(a)
			a=angle(R1x_list[i], R1x_list[j], R1y_list[i], R1y_list[j], R1z_list[i], R1z_list[j])	# phi1ij= R1i.R1j
			phi1ij.append(a)
			a=angle(R2x_list[i], R2x_list[j], R2y_list[i], R2y_list[j], R2z_list[i], R2z_list[j])	# phi2ij= R2i.R2j
			phi2ij.append(a)
			a=angle(R1x_list[i], dijx[count], R1y_list[i], dijy[count], R1z_list[i], dijz[count])	# psii1= R1i.dij
			psii1.append(a)
			a=angle(R2x_list[i], dijx[count], R2y_list[i], dijy[count], R2z_list[i], dijz[count])	# psii2= R2i.dij
			psii2.append(a)
			a=angle(R1x_list[j], dijx[count], R1y_list[j], dijy[count], R1z_list[j], dijz[count])	# psij1= R1j.dij
			psij1.append(a)
			a=angle(R2x_list[j], dijx[count], R2y_list[j], dijy[count], R2z_list[j], dijz[count])	# psij2= R2j.dij
			psij2.append(a)
		j=j+1	
		count=count+1
	i=i+1
D1=[]   # shift
D2=[]   # slide
Dn=[]    # rise
rho=[]   # roll
tau=[]   # tilt
omega=[] #twist

# Calculate other parameters
var=-1
count=0
i=1
while i<len(nuc_list):
	j=i+1
	while j<len(nuc_list):
		if (num_list[i]==num_list[j]):
			j=j+1
		if (j==len(nuc_list)):
			break
		# D1, D2
		if (count in newcount):
			var=var+1
			a=math.sin(float(tauj[var]))
			x=dot_prod(a, dijx[count])
			y=dot_prod(a, dijy[count])
			z=dot_prod(a, dijz[count])
			b=cal_mod(R1x_list[i], R1y_list[i], R1z_list[i])
			c=cal_mod(R2x_list[i], R2y_list[i], R2z_list[i])
			p=float(R1x_list[i])/b
			q=float(R1y_list[i])/b
			r=float(R1z_list[i])/b
			D1.append(format((p+q+r), '.4f'))
			p=float(R2x_list[i])/c
			q=float(R2y_list[i])/c
			r=float(R2z_list[i])/c
			D2.append(format((p+q+r), '.4f'))
			# Dn
			a=math.cos(float(tauj[var]))
			x=dot_prod(a, dijx[count])
			y=dot_prod(a, dijy[count])
			z=dot_prod(a, dijz[count])
			b=cal_mod(x, y, z)
			Dn.append(format(b, '.4f'))
			# rho
			rho.append(format((float(psii1[var])+float(psij1[var])-180), '.4f'))
			# tau
			tau.append(format((float(psii2[var])+float(psij2[var])-180), '.4f'))
		j=j+1
		count=count+1
	i=i+1

# Calculate omega
var=-1
count=0
i=1
while i<len(nuc_list):
	j=i+1
	while j<len(nuc_list):
		if (num_list[i]==num_list[j]):
			j=j+1
		if (j==len(nuc_list)):
			break
		if (count in newcount):
			var=var+1
			a=math.cos(float(tau[var]))
			x=dot_prod(a, R1x_list[j])
			y=dot_prod(a, R1y_list[j])
			z=dot_prod(a, R1z_list[j])
			a=angle(x, R2x_list[j], y, R2y_list[j], z, R2z_list[j])
			omega.append(a)
		j=j+1
		count=count+1
	i=i+1	

# Write all values to file 'parameters'
fout=open('parameters', 'w')
fout.write('i\ttype\tring\tchain\tj\ttype\tring\tchain\tdistance\tshift\tslide\trise\troll\ttilt\ttwist\n')
var=-1
count=0
i=1
while i<len(nuc_list):
	j=i+1
	while j<len(nuc_list):
		if (num_list[i]==num_list[j]):
			j=j+1
		if (j==len(nuc_list)):
			break
		if (count in newcount):
			var=var+1
			fout.write(num_list[i]+'\t'+nuc_list[i]+'\t'+ring_list[i]+'\t'+chain_list[i]+'\t'+num_list[j]+'\t'+nuc_list[j]+'\t'+ring_list[j]+'\t'+chain_list[j]+'\t'+str(distance[count])+'\t'+D1[var]+'\t'+D2[var]+'\t'+Dn[var]+'\t'+rho[var]+'\t'+tau[var]+'\t'+omega[var]+'\n')
		j=j+1
		count=count+1
	i=i+1
fout.close()


# Write the shortlisted ring-ring pairs to 'stacked_bases' along with the parameters
fout=open('stacked_bases', 'w')
fout.write('i\ttype\tring\tchain\tj\ttype\tring\tchain\tdistance\tshift\tslide\trise\troll\ttilt\ttwist\n')
var=-1
count=0
i=1
while i<len(nuc_list):
	j=i+1
	while j<len(nuc_list):
		if (num_list[i]==num_list[j]):
			j=j+1
		if (j==len(nuc_list)):
			break
		if (count in newcount):	# scan using 'x'
			var=var+1
			if (float(thetaij[var])<pm2):		# scan using 'd'
				if ((float(taui[var])<pm3) and (float(tauj[var])<pm3)): # scan using 'p'
					fout.write(num_list[i]+'\t'+nuc_list[i]+'\t'+ring_list[i]+'\t'+chain_list[i]+'\t'+num_list[j]+'\t'+nuc_list[j]+'\t'+ring_list[j]+'\t'+chain_list[j]+'\t'+str(distance[count])+'\t'+D1[var]+'\t'+D2[var]+'\t'+Dn[var]+'\t'+rho[var]+'\t'+tau[var]+'\t'+omega[var]+'\n')
		j=j+1
		count=count+1
	i=i+1
fout.close()
