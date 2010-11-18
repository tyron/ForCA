def get_prof_dropdown(default=None):
    prof_drop = SQLFORM.factory(
            Field('prof_id', Professores, default=default,
                requires = IS_IN_DB(db, Professores.id, 
                    '%(full_name)s', zero = '')))
    return prof_drop.custom.widget.prof_id

def get_disc_dropdown(default=None):
    disc_drop = SQLFORM.factory(
            Field('disc_id', Disciplinas, default=default,
                requires = IS_IN_DB(db, Disciplinas.id,
                    '%(name)s', zero = '')))
    return disc_drop.custom.widget.disc_id

def get_year_dropdown(default=None):
    year_drop = SQLFORM.widgets.options.widget(Avaliacoes.year, default)
    year_drop.insert(0, '')
    if not default:
        for x in year_drop:
            if '_selected' in x.attributes:
                x.attributes['_selected'] = False
        year_drop[0].attributes['_selected'] = 'selected'
    return year_drop

def get_grade_dropdown(default=None):
    grade_drop = SQLFORM.widgets.options.widget(Avaliacoes.grade, default)
    grade_drop.insert(0, '')
    if not default:
        for x in grade_drop:
            if '_selected' in x.attributes:
                x.attributes['_selected'] = False
        grade_drop[0].attributes['_selected'] = 'selected'
    return grade_drop
