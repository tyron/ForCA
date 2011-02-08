@auth.requires_membership('Admin')
def index():
    evals = db(Avaliacoes.id>0).select().as_list()
    num_evals = len(evals)

    evals_a = filter(lambda eval: eval['grade'] == 'A', evals)
    num_evals_a = len(evals_a)
    perc_evals_a = (num_evals_a/float(num_evals)) * 100

    evals_b = filter(lambda eval: eval['grade'] == 'B', evals)
    num_evals_b = len(evals_b)
    perc_evals_b = (num_evals_b/float(num_evals)) * 100

    evals_c = filter(lambda eval: eval['grade'] == 'C', evals)
    num_evals_c = len(evals_c)
    perc_evals_c = (num_evals_c/float(num_evals)) * 100

    evals_d = filter(lambda eval: eval['grade'] == 'D', evals)
    num_evals_d = len(evals_d)
    perc_evals_d = (num_evals_d/float(num_evals)) * 100

    evals_ff = filter(lambda eval: eval['grade'] == 'FF', evals)
    num_evals_ff = len(evals_ff)
    perc_evals_ff = (num_evals_ff/float(num_evals)) * 100

    return dict(num_evals_a=num_evals_a, perc_evals_a=perc_evals_a,\
                num_evals_b=num_evals_b, perc_evals_b=perc_evals_b,\
                num_evals_c=num_evals_c, perc_evals_c=perc_evals_c,\
                num_evals_d=num_evals_d, perc_evals_d=perc_evals_d,\
                num_evals_ff=num_evals_ff, perc_evals_ff=perc_evals_ff)
