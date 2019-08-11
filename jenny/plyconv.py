import sys
import struct
import os

if os.path.exists("data"):
	os.remove("data")
o=open("data", "w")

filename=sys.argv[1]
f=open(filename, 'rb')

line=f.readline().decode('ascii').strip()
if line!='ply':
	print("something has gone wrong, this isn't a ply file")
	sys.exit(1)
endianess=f.readline().decode('ascii').strip().split()[1] #get endianess
comment=f.readline().decode('ascii').strip().strip("comment ")
line=f.readline().decode('ascii').strip().split()
if line[1]!='vertex':
	print("didn't find any vertices, quitting")
	sys.exit(1)
num_vertices=int(line[2])
for i in range(0, 3):
	line=f.readline().decode('ascii').strip().split()
	if line[1]!='float32':
		print("expected 3 32-bit float values for xyz")
		sys.exit(1)

for i in range(0, 3):
	line=f.readline().decode('ascii').strip().split()
	if line[1]!='uchar':
		print("expected 3 8-bit uchar values for xyz")
		sys.exit(1)

for i in range(0, 3):
	line=f.readline().decode('ascii').strip()

if line!='end_header':
	print("something has gone wrong, expected header end")
	sys.exit(1)

s=struct.Struct('<fffBBB')
step=0
for i in range(0, num_vertices):
	x, y, z, r, g, b=s.unpack(f.read(s.size))
	print(x, y, z)
	o.write(str(x)+"\t"+str(y)+"\t"+str(z)+"\n")
f.close()
o.close()


	
