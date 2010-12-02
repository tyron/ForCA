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
    return sum(cut_counts)/float(len(cut_counts))

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

def get_aluno_quality(aluno_row):
    '''
    Returns the quality index [0-2] for the given user
    '''
    pass
