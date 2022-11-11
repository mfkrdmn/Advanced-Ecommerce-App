from .models import *

# A context processor is a function that accepts an argument and returns a dictionary as its output. 
#In our case, the returning dictionary is added as the context and the biggest advantage is that, 
#it can be accessed globally i.e, across all templates. 

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)