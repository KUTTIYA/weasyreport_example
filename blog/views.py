from django.shortcuts import render
# -*- coding: utf-8 -*-
from .models import Entry
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile


def post_list(request):
    return render(request, 'blog/post_list.html', {})

def generate_pdf(request):
    """Generate pdf."""
    # Model data
    entryreport = Entry.objects.all().order_by('rating')

    # Rendered
    html_string = render_to_string('blog/list_entry.html', {'entryreport': entryreport})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_entry.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


