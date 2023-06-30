from django.views.generic import TemplateView,View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AttentionData,ClickData,ScrollData
import json
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import os
from LPheatmap import settings
import matplotlib.colors as mcolors
from collections import defaultdict



class Top(TemplateView):
    template_name = "lpanalysis/top.html"


class Index(TemplateView):

    #テンプレートファイル連携
    template_name = "lpanalysis/index.html"

    


    #attentionDataを受信するためのビュー
@csrf_exempt
def receive_attention_data(request):
            if request.method == 'POST':
                new_data = json.loads(request.body)

                
                for position, time in new_data.items():                    
                    attention_data = AttentionData.objects.filter(attention_position = position).first()
                    if attention_data is not None:
                        attention_data.stay_time = time
                    else:
                        attention_data = AttentionData(attention_position = position,stay_time = time)
                    attention_data.save()
        
                return JsonResponse("ok")
            else:
                return JsonResponse({"error": "Invalid request method"}, status=400)

#scrollDataを受信、保存するためのビュー
@csrf_exempt
def receive_scroll_data(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            
            for position, count in data.items():
                scroll_data = ScrollData.objects.filter(max_scroll_position = position).first()
                if scroll_data is not None:
                    scroll_data.max_scroll_count = count
                else:
                    scroll_data =  ScrollData(max_scroll_position = position, max_scroll_count = count)
                
                scroll_data.save()
       
            return JsonResponse({"message": "Data received successfully"})
        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)


#clickDataを受信、保存するためのビュー
@csrf_exempt
def receive_click_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        for position, count in data.items():
            x,y = map(int,position.split(","))
            click_data = ClickData.objects.filter(click_position_x = x,click_position_y =y).first()
            if click_data is not None:
                click_data.click_count = count
            else:
                click_data = ClickData(click_position_x = x,click_position_y =y,click_count =count )
            click_data.save()
            
           
        return JsonResponse({"message": "Data received successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


#アテンションヒートマップを作成するビュー
def heatmap_view(request):
    attention_data = AttentionData.objects.all()
    attention_dict = defaultdict(int)
    
    max_attention_position = max(record.attention_position for record in attention_data)

    for record in attention_data:
        interval = record.attention_position // 50
        attention_dict[interval] += record.stay_time

    heatmap = np.zeros((max_attention_position+1, 1))

    for interval, time in attention_dict.items():
        start = interval * 50
        end = start + 50
        heatmap[start:end, 0] = time

    plt.figure(figsize=(5, 5))
    
    vmin = np.min(heatmap)
    vmax = np.max(heatmap)
    
    plt.imshow(heatmap, cmap='Reds', interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax)
    plt.colorbar(label='Stay Time')
    plt.ylabel("Attention Position")
    plt.xticks([])  

    save_path = os.path.join(settings.BASE_DIR, "static", 'attentionheatmap.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()  

    return render(request, 'lpanalysis/a-heatmap.html')



#クリックヒートマップを作成するビュー
def click_heatmap_view(request):
    click_data = ClickData.objects.all()

    click_dict = defaultdict(int)

    max_click_position_x = max(record.click_position_x for record in click_data)
    max_click_position_y = max(record.click_position_y for record in click_data)

    for record in click_data:
        interval_x = record.click_position_x // 50
        interval_y = record.click_position_y // 50
        click_dict[(interval_y, interval_x)] += record.click_count

    heatmap = np.zeros((max_click_position_y+1, max_click_position_x+1))  # <- 修正された部分

    for (interval_y, interval_x), count in click_dict.items():
        start_x = interval_x * 50
        end_x = start_x + 50
        start_y = interval_y * 50
        end_y = start_y + 50
        heatmap[start_y:end_y, start_x:end_x] = count  # <- 修正された部分


    plt.figure(figsize=(5, 5))
    
    vmin = np.min(heatmap)
    vmax = np.max(heatmap)
    
    plt.imshow(heatmap, cmap='Reds', interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax)
    plt.colorbar(label='Click Count')

    save_path = os.path.join(settings.BASE_DIR, "static", 'clickheatmap.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return render(request, 'lpanalysis/c-heatmap.html')


#スクロールヒートマップを作成するビュー
def scroll_heatmap_view(request):
    
    scroll_data = ScrollData.objects.all()
    scroll_dict = defaultdict(int)
    
    max_scroll_position = max(record.max_scroll_position for record in scroll_data)

    for record in scroll_data:
        interval = record.max_scroll_position // 50
        scroll_dict[interval] += record.max_scroll_count

    heatmap = np.zeros((max_scroll_position+1, 1))

    for interval, count in scroll_dict.items():
        start = interval * 50
        end = start + 50
        heatmap[start:end, 0] = count

    plt.figure(figsize=(5, 5))
    
    vmin = np.min(heatmap)
    vmax = np.max(heatmap)
    
    plt.imshow(heatmap, cmap='Reds', interpolation='nearest', aspect='auto', vmin=vmin, vmax=vmax)
    plt.colorbar(label='count')
    plt.ylabel("max_scroll_position")
    plt.xticks([])  

    save_path = os.path.join(settings.BASE_DIR, "static", 'scrollheatmap.png')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()  

    return render(request, 'lpanalysis/s-heatmap.html')
