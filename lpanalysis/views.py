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




class Index(TemplateView):

    #テンプレートファイル連携
    template_name = "lpanalysis/index.html"

    


    #attentionDataを主審するためのビュー
@csrf_exempt
def receive_attention_data(request):
            if request.method == 'POST':
                data = json.loads(request.body)
                for attention_position, stay_time in data.items():
                    attention_data = AttentionData(attention_position= attention_position,stay_time = stay_time)
                    attention_data.save()

        
                return JsonResponse(data)
            else:
                return JsonResponse({"error": "Invalid request method"}, status=400)

#scrollDataを主審するためのビュー
@csrf_exempt
def receive_scroll_data(request):
        if request.method == 'POST':
            data = json.loads(request.body)
            for position, count in data.items():
                scroll_data = ScrollData(max_scroll_position = position,max_scroll_count = count)
                scroll_data.save()
                
        
       
            return JsonResponse({"message": "Data received successfully"})
        else:
            return JsonResponse({"error": "Invalid request method"}, status=400)


#clickDataを主審するためのビュー
@csrf_exempt
def receive_click_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        click_data_instances = []
        for click_position, click_count in data.items():
            x, y = map(int, click_position.split(','))
            click_data = ClickData(click_position_x=x, click_position_y=y, click_count=click_count)
            click_data_instances.append(click_data)
        ClickData.objects.bulk_create(click_data_instances)
        return JsonResponse({"message": "Data received successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


def heatmap_view(request):
    data = AttentionData.objects.values_list('attention_position', 'stay_time')

    
    stay_time_data = np.zeros(6001)
    for pos, time in data:
        stay_time_data[pos] = time
    print(stay_time_data[0:5])


    stay_time_data_2d = np.tile(stay_time_data, (100, 1)).T  # 100は横軸の長さで、実際のウェブページの幅に合わせて変更する必要があります。

    # ヒートマップの描画
    plt.imshow(stay_time_data_2d, cmap='hot', aspect='auto')

    save_path = os.path.join(os.path.join(settings.BASE_DIR, "static"), 'attentionheatmap.png')
    plt.savefig(save_path)
   
    
    

    return render(request, 'lpanalysis/heatmap.html')