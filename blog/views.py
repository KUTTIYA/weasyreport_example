from django.shortcuts import render
# -*- coding: utf-8 -*-
from .models import Entry, MasterPart
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

from django.views.generic import TemplateView

from django.shortcuts import get_object_or_404

import math


def post_list(request):
    return render(request, 'blog/truck_control.html', {})

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

def truck_control_pdf(request):
    """Generate pdf."""
    # Model data
    #entryreport = Entry.objects.all().order_by('rating')

    # Rendered
    html_string = render_to_string('blog/truck_control.html')
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=truck_control.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response

class DailyReportView(TemplateView):
    template_name = 'blog/index.html'

def generate_pdf(request):
    page = 10

    all_count = MasterPart.objects.count()
    all_page_no = math.ceil(all_count/page)

    truck_no = 'กข-1234'
    truck_control_no = 'T-010-20201015'
    truck_type = '6W'
    promised_date = '2020-10-15'
    driver_name = 'นายน้ำใส ใจจริง'
    telephone = '081-2345678'

    list_pdf = []
    for i in range(0, all_page_no):
        query_max = (i+1)*page
        if query_max > all_count:
            query_max = all_count
        master_list = MasterPart.objects.all().order_by('part_id')[(i*page):query_max]
        html_string = render_to_string('blog/index.html', {'master_list': master_list, 'start_index': (i*page), 'page_no': (i+1), 'all_page_no': all_page_no, 'truck_no': truck_no, 'truck_control_no': truck_control_no, 'truck_control_no': truck_control_no, 'truck_type': truck_type, 'promised_date': promised_date, 'driver_name': driver_name, 'telephone': telephone})
        pdf = HTML(string=html_string)
        list_pdf.append(pdf)
    
    lid_render = []
    val = []
    boo_first = True
    pdf_data = None

    for pdf in list_pdf:
        if boo_first:
            boo_first = False
            pdf_data = pdf.render()
        lid_render.append(pdf.render())

    for doc in lid_render:
        for p in doc.pages:
            val.append(p)

    pdf_file = pdf_data.copy(val).write_pdf() # use metadata of pdf_first

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    return http_response


