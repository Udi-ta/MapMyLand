from django.shortcuts import render, redirect
from .models import Property, City
from .forms import PropertyForm
from django.db.models import Q, Count
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
from django.http import HttpResponse
import xlsxwriter
from weasyprint import HTML 
from django.urls import reverse

def home(request):
    return render(request, 'estates/home.html')

def property_list(request):
    properties = Property.objects.all()
    query = request.GET.get('q')
    if query:
        properties = properties.filter(
            Q(google_location__icontains=query) |
            Q(broker__name__icontains=query) |
            Q(city__name__icontains=query) |
            Q(micro_market__name__icontains=query)
        )
    return render(request, 'estates/Property_list.html', {'properties': properties})

def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_map')
    else:
        form = PropertyForm()
    return render(request, 'estates/form.html', {'form': form})

# Similar views for Broker, City, and MicroMarket
def generate_charts():
    city_data = Property.objects.values('city__name').annotate(properties_count=Count('id'))
    
    # Convert to DataFrame
    df = pd.DataFrame(city_data)
    df.rename(columns={'city__name': 'City', 'properties_count': 'Properties'}, inplace=True)

    # Plot
    plt.figure(figsize=(10, 5))
    plt.bar(df['City'], df['Properties'])
    plt.title('Properties per City')
    plt.xlabel('City')
    plt.ylabel('Properties')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

def download_report(request):
    buffer = generate_charts()

    response = HttpResponse(buffer, content_type='application/png')
    response['Content-Disposition'] = 'attachment; filename="report.png"'

    return response

def download_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    data = Property.objects.all().values()
    df = pd.DataFrame(data)

    for i, col in enumerate(df.columns):
        worksheet.write(0, i, col)
        for j, val in enumerate(df[col]):
            worksheet.write(j + 1, i, val)

    workbook.close()
    return response