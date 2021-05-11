#视图，业务逻辑，模型与模板的桥梁
from django.shortcuts import render, HttpResponse
import sys
sys.path.append('..')
from QQMusicSpider.whoosh_test import Query

q = Query()

'''
render(request,tempalte_name,context=None,content_type=None,status=None,using=None)
request:浏览器向服务器发送的请求对象
template_name:HTML模板文件名，用于生成html网页
context:对html模板的变量赋值
P44 
'''

def search_form(request):
    return render(request, 'main.html')

def search(request):
    res = None
    high=None
    if 'q' in request.GET and request.GET['q']:
        if request.GET['ca'] == 'lyric':
            res = q.Search_lyric(request.GET['q'])#得到q的参数，并以字典形式存储
            print(request.GET['q'])
            c = {
                'query': request.GET['q'],
                'resAmount': len(res),
                 'results': res,
            }
            return render(request, 'result_lyric.html', c)
        else:
            res = q.Search(request.GET['ca'], request.GET['q'])  # 得到q的参数，并以字典形式存储
            print(request.GET['q'])
            c = {
                'query': request.GET['q'],
                'resAmount': len(res),
                'results': res,
            }
            return render(request, 'result.html', c)
    else:
        return render(request, 'main.html')

    # str = ''
    # for i in res:
    #     str += '<p><a href="' + i['newsUrl'] + '">' + i['newsTitle'] + '</a></p>'
    # return HttpResponse(str)


