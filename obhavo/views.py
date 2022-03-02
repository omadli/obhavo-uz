from django.http import Http404
from django.shortcuts import render
from .models import City
from .funcs import getDataCity, search_city
# Create your views here.

def main(request, city_name="Tashkent"):
	cities = City.objects.all()
	try:
		cit = City.objects.get(city=city_name)
	except City.DoesNotExist:
		raise Http404("City does not exist")
	data = getDataCity(cit)
	data.update({'Cities': cities})
	return render(request, 'home.html', data)

def search(request):
	cities = City.objects.all()
	q = request.GET.get('q')
	lat = request.GET.get('lat')
	lon = request.GET.get('lon')
	if q:
		data = search_city(q)
		if data:
			data.update({'Cities': cities, 'search': '200'})
			return render(request, 'home.html', data)
		else:
			tosh = City.objects.get(city="Tashkent")
			data = getDataCity(tosh)
			data.update({'Cities': cities, 'search': '404'})
			return render(request, 'home.html', data)
	elif lat and lon:
		data = search_location(lat, lon)
		if data:
			data.update({'Cities': cities, 'search': '200'})
			return render(request, 'home.html', data)
		else:
			tosh = City.objects.get(city="Tashkent")
			data = getDataCity(tosh)
			data.update({'Cities': cities, 'search': '404'})
			return render(request, 'home.html', data)
	else:
		return main()

