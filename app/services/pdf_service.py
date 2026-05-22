from io import BytesIO
from xhtml2pdf import pisa
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

def render_to_pdf(template_src, context_dict):
    template = templates.get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return result.getvalue()
    return None
