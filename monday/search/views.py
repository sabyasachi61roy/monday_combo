from django.shortcuts import render, redirect
from django.views.generic import ListView
from products.models import Combo, Addon

class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        combo = Combo.objects.filter(title__icontains=query)
        addon = Addon.objects.filter(name__icontains=query)
        context['query'] = query
        context['combo'] = combo
        context['addon'] = addon
        # SearchQuery.objects.create(query=query)
        return context
    
    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        print("q",query)
        combo = Combo.objects.filter(title__icontains=query)
        addon = Addon.objects.filter(name__icontains=query)
        if query is not None:
            print("1-c",combo)
            if addon.exists():
                print("1-a",addon)
                return Addon.objects.filter(name__icontains=query)
            print("2-c",combo)
            return Combo.objects.filter(title__icontains=query)
        return redirect("/")
        
        '''
        __icontains = field contains this
        __iexact = fields is exactly this
        '''