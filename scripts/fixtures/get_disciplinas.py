import sys

inp = open(sys.argv[1])
out = open('../../models/xtures/disciplinas.py', 'w')

out.write('''
if db(db.disciplinas.id > 0).count() == 0:
''')

for line in inp.readlines():
	data = map(lambda x: x.strip(), line[61:-3].split(','))
	out.write("\tdb.disciplinas.insert(id="+str(data[0]).strip()+", code="+data[1]+", name="+data[2]+", short_name="+data[3]+")\n")

inp.close()
out.close()
