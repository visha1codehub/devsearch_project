from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag

def searchProjects(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print("SEARCH: ", search_query)
        
    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                      Q(owner__name__icontains=search_query) |
                                      Q(tags__in=tags)
                                      )
    return projects, search_query

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page=1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
        
    leftIndex = int(page)-4
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = int(page)+5
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    custome_range = range(leftIndex, rightIndex)
    return projects, custome_range