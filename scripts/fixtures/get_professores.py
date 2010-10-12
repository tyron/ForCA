import sys

inp = open(sys.argv[1])
out = open('../../models/xtures/professores.py', 'w')

out.write('''
if db(db.professores.id > 0).count() == 0:
''')

for line in inp.readlines():
	data = map(lambda x: x.strip(), line[83:-3].split(','))
	out.write("\tdb.professores.insert(id="+str(data[0]).strip()+", email="+data[1]+", short_name="+data[2]+", full_name="+data[3]+")\n")

inp.close()
out.close()
