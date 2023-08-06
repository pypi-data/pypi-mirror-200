from django.conf.urls import url
from django.urls import path
from .models import Annotation, Tag, AnnotationTarget, NeedleActivity, AnnotationIntersectionRead, ContactMessage, \
    Booklet, NeedleUserFollow
from .views import AnnotationViewset, AnnotationTargetViewset, TagViewset, AnnotationTargetIntersectionViewset, \
    AnnotationIntersectionsAfterViewset, AnnotationIntersectionsBeforeViewset, AnnotationIntersectionReadViewset, \
    ContactMessageView, BookletViewset, BookletInvitationViewset, BookletQuitViewset, NeedleUserFollowViewset

urlpatterns = [
    url(r'^booklets/', BookletViewset.urls(model_prefix="booklet", model=Booklet)),
    path('booklets/<pk>/invitation/', BookletInvitationViewset.as_view({'post': 'create'}, model=Booklet)),
    path('booklets/<pk>/quit/', BookletQuitViewset.as_view({'post': 'create'}, model=Booklet)),
    url(r'^annotations/', AnnotationViewset.urls(model_prefix="annoations", model=Annotation)),
    url(r'^annotationtargets/', AnnotationTargetViewset.urls(model_prefix="annotationtarget", model=AnnotationTarget)),
    url(r'^annotationintersectionreads/', AnnotationIntersectionReadViewset.urls(model_prefix="annotationintersectionread", model=AnnotationIntersectionRead)),
    path('annotationtargetsintersection/<url>/<date>', AnnotationTargetIntersectionViewset.as_view({'get': 'list'}, model=AnnotationTarget)),
    path('annotationintersections/before/<url>/<date>',
        AnnotationIntersectionsBeforeViewset.as_view({'get': 'list'}, model=Annotation)),
    path('annotationintersections/after/<url>/<date>',
        AnnotationIntersectionsAfterViewset.as_view({'get': 'list'}, model=Annotation)),
    url(r'^users/(?P<slug>[\w\-\.]+)/yarn/', AnnotationViewset.urls(model_prefix="yarn", model=Annotation)),
    url(r'^users/(?P<slug>[\w\-\.]+)/tags', TagViewset.urls(model_prefix="tags", model=Tag)),
    url(r'^contact_messages/', ContactMessageView.as_view({'post': 'create'},  model=ContactMessage)),
    url(r'^needleuserfollow/', NeedleUserFollowViewset.urls(model=NeedleUserFollow))
]
