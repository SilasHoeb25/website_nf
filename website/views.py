from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def hello_partial(request):
    return HttpResponse("""
        <div class="p-3 bg-green-100 border border-green-300 rounded">
            HTMX response loaded without a page reload 🚀
        </div>
    """)