from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from uuid import uuid4
from cgi import escape
from cStringIO import StringIO

def report():
    '''
    Gera um report em pdf das avaliacoes do professor
    '''
    prof_id = request.vars['prof_id']
    response.headers['Content-Type']='application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=b.pdf'

    s = StringIO()
    p = canvas.Canvas(s)

    p.drawString(100, 100, str(prof_id))

    p.showPage()
    p.save()
    return s.getvalue()


