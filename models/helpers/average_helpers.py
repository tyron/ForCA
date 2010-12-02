###########################################################
#                eval quality getters                     #
###########################################################

def get_karma_list(karmas_rows):
    '''
    Returns karma values list from a set of karma rows
    '''
    karmas = map(lambda row: row.value, karmas_rows)
    return karmas

def get_positive_rate(karmas_list):
    '''
    Calculates the positive karma rate given a list of karma values
    '''
    non_zeros = filter(lambda karma: karma != 0, karmas_list)
    if len(non_zeros) == 0:
        return 0
    positive_rate = non_zeros.count(1)/float(len(non_zeros))
    return positive_rate

def get_karma_count_avg():
    '''
    Returns the treated karma count average of all evals
    '''
    allevals = db(Avaliacoes.id>0).select()
    counts = map(lambda eval: len(get_karma_list(eval.karmas.select())), allevals)
    counts.sort()
    cut_counts = counts[len(counts)/10:len(counts)-len(counts)/10]
    return max(1,sum(cut_counts)/float(len(cut_counts)))

def get_avg_positive_rate():
    '''
    Returns the average positive karma rate of all evals
    '''
    allevals = db(Avaliacoes.id>0).select()
    pos_list = map(lambda eval: get_positive_rate(get_karma_list(eval.karmas.select())), allevals)
    if len(pos_list) == 0:
        return 0
    pos_avg = sum(pos_list)/len(pos_list)
    return pos_avg

def get_eval_quality(eval_row):
    '''
    Returns the quality index [0-2] for the given eval
    '''
    karmas = get_karma_list(eval_row.karmas.select())
    if len(karmas) < get_karma_count_avg():
        return 1
    positive_rate = get_positive_rate(karmas)
    avg_positive_rate = get_avg_positive_rate()
    if positive_rate < avg_positive_rate/2.0:
        return 0
    elif positive_rate > avg_positive_rate*2.0:
        return 2
    else:
        return 1

###########################################################
#                aluno quality getters                    #
###########################################################

def get_aluno_karmas(aluno_row):
    '''
    Gets all karmas received by the user's evaluations
    '''
    evals = aluno_row.avaliacoes.select()
    karmas_lists = map(lambda eval: get_karma_list(eval.karmas.select()), evals)
    allkarmas = sum(karmas_lists, []) #kids, do NOT try this at home!
    return allkarmas

def get_aluno_karma_count_avg():
    '''
    Gets the treated average student karma count
    '''
    allunos = db(Alunos.id>0).select()
    counts = map(lambda aluno: sum(get_aluno_karmas(aluno)), allunos)
    counts.sort()
    cut_counts = counts[len(counts)/10:len(counts)-len(counts)/10]
    return max(1,sum(cut_counts)/len(cut_counts))

def get_aluno_positive_rate(aluno_row):
    '''
    Gets the positive karma rate for a given student
    '''
    evals = aluno_row.avaliacoes.select()
    if len(evals) == 0:
        return 0
    pos_rates = map(lambda eval: get_positive_rate(get_karma_list(eval.karmas.select())), evals)
    return sum(pos_rates)/float(len(pos_rates))

def get_aluno_avg_positive_rate():
    '''
    Returns the average positive karma rate of all students
    '''
    allunos = db(Alunos.id>0).select()
    alunos_pos_rates = map(lambda aluno: get_aluno_positive_rate(aluno), allunos)
    if len(alunos_pos_rates) == 0:
        return 0
    pos_avg = sum(alunos_pos_rates)/float(len(alunos_pos_rates))
    return pos_avg

def get_aluno_quality(aluno_row):
    '''
    Returns the quality index [0-2] for the given user
    '''
    karmas = get_aluno_karmas(aluno_row)
    if len(karmas) < get_aluno_karma_count_avg():
        return 1
    positive_rate = get_aluno_positive_rate(aluno_row)
    avg_positive_rate = get_aluno_avg_positive_rate()
    if positive_rate < avg_positive_rate/2.0:
        return 0
    elif positive_rate > avg_positive_rate*2.0:
        return 2
    else:
        return 1
