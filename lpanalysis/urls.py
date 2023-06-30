from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("",views.Top.as_view(), name="top"),
    path("index",views.Index.as_view(), name="index"),
    path("receive-attention-data",views.receive_attention_data, name="receive-attention-data"),
    path("receive-scroll-data",views.receive_scroll_data, name="receive-scroll-data"),
    path("receive-click-data",views.receive_click_data, name="receive-click-data"),
    path("a-heatmap",views.heatmap_view, name="a-heatmap"),
    path("c-heatmap",views.click_heatmap_view, name="c-heatmap"),
    path("s-heatmap",views.scroll_heatmap_view, name="s-heatmap"),

    

]
