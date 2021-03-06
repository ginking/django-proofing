
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings

from models import Category, Gallery, Photo
from decorators import check_perm_for
from utils.breadcrumb import WBBreadcrumbTrail, WBBreadcrumb



def index(request, template_name="proofing_generic_list.html"):
    objects = Category.active.all()
    
    breadcrumbtrail = WBBreadcrumbTrail(WBBreadcrumb('Home',reverse('proofing-index')))
    page_title = 'Show Index'
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



def show_category(request, slug, template_name="proofing_generic_list.html"):
    object = get_object_or_404(Category, slug = slug)
    
    objects = Gallery.active.filter(category=object)
    
    breadcrumbtrail = WBBreadcrumbTrail(WBBreadcrumb('Home',reverse('proofing-index')),object)
    page_title = 'Category: '+object.title
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



@check_perm_for(Gallery)
def show_gallery(request, object, template_name="proofing_generic_list.html"):
    
    objects = Photo.active.filter(gallery=object)
    
    breadcrumbtrail = WBBreadcrumbTrail(WBBreadcrumb('Home',reverse('proofing-index')),object.category, object)
    page_title = 'Gallery: '+object.title
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))



@check_perm_for(Photo)
def show_photo(request, object, template_name="proofing_photo.html"):
    
    breadcrumbtrail = WBBreadcrumbTrail(
                                        WBBreadcrumb('Home',reverse('proofing-index')),
                                        object.gallery.category, 
                                        object.gallery,
                                        object)
    
    objects = Photo.active.filter(gallery=object.gallery)
    lenp = len(objects)
    i=0
    for i in range(lenp):
        p=objects[i]
        if object.slug==p.slug:
            next=objects[i-1] if i>0 else None
            previous = objects[i+1] if i<lenp-1 else None
            break
    page_title = 'Photo: '+object.title
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


