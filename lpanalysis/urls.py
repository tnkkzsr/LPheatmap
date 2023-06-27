from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("",views.Index.as_view(), name="Index"),

    path("receive-attention-data",views.receive_attention_data, name="receive-attention-data"),
    path("receive-scroll-data",views.receive_scroll_data, name="receive-scroll-data"),
    path("receive-click-data",views.receive_click_data, name="receive-click-data"),
    path("create-heatmap",views.heatmap_view, name="create-heatmap"),

    

]
