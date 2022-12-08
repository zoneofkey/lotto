import ast
import json
import random
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from .models import Post
# Create your views here.


def index(request):

    return render(request,'lotto/index.html')


def lotto_main(request):
    lotto2 = []
    rnd_num = random.randint(1, 45)

    for j in range(108):

        lotto = []
        for i in range(6):
            while rnd_num in lotto:
                rnd_num = random.randint(1, 45)
            lotto.append(rnd_num)

        lotto.sort()
        js2 = {"id": j, "name": lotto}

        lotto2.append(js2)

        # print("로또번호2: {}".format(js2))
        # print("로또번호: {}".format(lotto))

    # print(lotto2[1])
    # lotto3 = []
    # lotto3 = lotto2[1].__getitem__("name")
    # print("로또번호3: {}".format(lotto3))

    now = datetime.now()

    if now.weekday() == 0:
        t1 = "월요일"
    elif now.weekday() == 1:
        t1 = "화요일"
    elif now.weekday() == 2:
        t1 = "수요일"
    elif now.weekday() == 3:
        t1 = "목요일"
    elif now.weekday() == 4:
        t1 = "금요일"
    elif now.weekday() == 5:
        t1 = "토요일"
    else:
        t1 = "일요일"

    post = Post()
    post.postname = "익명"
    post.pub_date_k = str(now.year)+"년"+str(now.month)+"월"+str(now.day)+"일 "+t1+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)
    post.contents2 = lotto2
    post.save()

    return render(request, 'lotto/lotto_main.html', {'lotto': lotto2, 'pkconfirm': post.pk})


def l_save(request):

    if request.method == 'POST':

        pk = request.POST['pk']

        post = Post.objects.get(pk=pk)
        postname = request.POST['postname']
        contents = request.POST['contents']
        color_k = request.POST['color_k']
        print("값 확인:" + color_k)

        if postname == "":
            post.postname = "익명"
        else:
            post.postname = postname

        if color_k == "none":
            post.color_k = post.color_k
        else:
            post.color_k = color_k

        post.contents = contents
        post.save()

        return redirect('/l_list')
    return render(request, 'lotto/l_list')


def l_detail(request, pk):
    # post = Post.objects.order_by('-pub_date')[:1]
    #
    # # querySet 의 특성상 for문으로 돌려줘야 개별 데이터를 확인할 수 있다.
    #
    # for post1 in post:
    #     lotto4 = post1.contents2

    post = Post.objects.get(pk=pk)

    # str 을 list 로 변경해주는 메소드
    result = eval(post.contents2)
    contents = post.contents
    postname = post.postname
    # print(type(result))

    return render(request, 'lotto/l_detail.html', {'lotto': result, 'contents': contents, 'postname': postname})


def l_list_ser(request):

    if request.method == 'POST':

        ser = request.POST['ser']

        postlist = Post.objects.filter(postname=ser).order_by('-pub_date')

        return render(request, 'lotto/l_list_ser.html', {'postlist': postlist})

    return render(request, 'lotto/l_list_ser.html')


def l_list(request):

    postlist = Post.objects.all().order_by('-pub_date')

    # 최신 일자로 100개 호출 문제 100 개가 넘어가는 페이지에서 호출이 안될듯.
    # postlist = Post.objects.order_by('-pub_date')[:100]

    page = request.GET.get('page')

    paginator = Paginator(postlist, 49)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)+4)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex+1)
    # 수정 사항 오브젝트를 all()이 아닌 특정 페이지 수로 부터 특정 갯수 만큼만 호출해서 가져오기 가능하면, custom_range 1페이지일때 3개만 표시되는 것 수정

    return render(request, 'lotto/l_list.html', {'postlist': postlist, 'page_obj': page_obj, 'paginator': paginator, 'custom_range': custom_range})


def main_l(request):

    postlist = Post.objects.all()

    # 최신 일자로 100개 호출 문제 100 개가 넘어가는 페이지에서 호출이 안될듯.
    # postlist = Post.objects.order_by('-pub_date')[:100]

    page = request.GET.get('page')

    paginator = Paginator(postlist, 2)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page)+4)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages

    custom_range = range(leftIndex, rightIndex+1)
    # 수정 사항 오브젝트를 all()이 아닌 특정 페이지 수로 부터 특정 갯수 만큼만 호출해서 가져오기 가능하면, custom_range 1페이지일때 3개만 표시되는 것 수정

    return render(request, 'lotto/main_l.html', {'postlist': postlist, 'page_obj': page_obj, 'paginator': paginator, 'custom_range': custom_range})


def posting(request, pk):
    post = Post.objects.get(pk=pk)

    return render(request, 'lotto/posting.html', {'post': post})


def new_post(request):
    if request.method == 'POST':

        post = Post()

        # 미디어 파일의 경우 익셉션이 발생되어 트라이 익셉션을 해야 에러가 발생 안함.
        try:
            post.mainphoto = request.FILES['mainphoto']
        except:
            post.mainphoto = None


        new_article = Post.objects.create(
            postname=request.POST['postname'],
            contents=request.POST['contents'],
            mainphoto=post.mainphoto,
        )

        return redirect('/main_l')
    return render(request, 'lotto/new_post.html')


def remove_post(request, pk):
    post =  Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/main_l')
    return render(request, 'lotto/remove_post.html', {'Post': post})
