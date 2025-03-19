from django.shortcuts import redirect

def api_home(request):
    return redirect('/api/blog/posts/')  # 👈 Redirects to the posts list