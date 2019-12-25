from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.

def indexHtml(request):
    """
    返回一个HTML文件,当想渲染一个html文件时,需要使用render方法进行打包
    """
    print('打开对话框')
    return render(request, "index.html")  # 参数1固定,参数2:指定返回的html文件

def getQuestion(request):
    questionText = request.GET['text']
    answer = getAnswer(questionText)
    return HttpResponse(answer)

def getAnswer(questionText):
    answer = "美国"
    return answer