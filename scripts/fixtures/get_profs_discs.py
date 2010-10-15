import sys

inp = open(sys.argv[1])
out = open('../../models/xtures/profs_discs.py', 'w')

out.write('''
if db(db.profs_discs.id > 0).count() == 0:
''')

for line in inp.readlines():
	data = map(lambda x: x.strip(), line[66:-3].split(','))
	out.write("\tdb.profs_discs.insert(id="+str(data[0]).strip()+", professor_id="+data[1]+", disciplina_id="+data[2]+")\n")

inp.close()
out.close()
