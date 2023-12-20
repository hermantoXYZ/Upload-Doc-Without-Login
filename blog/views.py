from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Kategori, Dokumen
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from taggit.models import Tag
from django.template.context import RequestContext
from django.db.models import Q
from csp.decorators import csp_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import * 
from rest_framework.views import APIView
from rest_framework import viewsets, status
from .forms import DokumenForm
from django.contrib import messages
import random

class ListViewSet(APIView):
    def get(self, request):
        datanya = Post.objects.filter(status=1).all()
        serializer = ArticleSerializer(datanya, many=True)
        return Response(serializer.data)

def docs(request):
    # response = redirect('/')
    # return response
    return render(request,"blog/lozad.html") 

def pindah(request, id, slug):
    # Gunakan get_object_or_404 untuk mengambil objek Post berdasarkan ID
    post = get_object_or_404(Post, id=id, status=1)

    # Sekarang Anda memiliki objek 'post' yang sesuai dengan ID yang diberikan
    # Anda dapat melakukan apa pun yang Anda inginkan dengan objek ini, misalnya, mengirimkannya ke template
    return render(request, "blog/detailpost.html", {'post': post})

def cari(request):
    q = request.GET.get('q')

    print(q)
    return HttpResponse("asdasd")

# search view
@csp_exempt
def search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:            
            results = Post.objects.filter(  
            	Q( title__contains = q ) |
                Q( slug__contains = q ),status=1  )[:7]          
            # print(results.query)
            return render(request,'blog/hasilcari.html', {'results': results})

@csp_exempt
def PostList(request):
    kategori = Kategori.objects.all()
    queryset = Post.objects.filter(status=1).order_by('-created_on').select_related('kategori')
    randompost = random.sample(list(queryset), min(len(queryset), 3))

    # Menambahkan definisi latest_headline
    headline_list = Post.objects.filter(is_headline=True, status=1)[:4]

    # Menambahkan query untuk mendapatkan data program_pendidikan
    program_pendidikan_data = Dokumen.objects.values('program_pendidikan').distinct()

    if request.method == 'POST':
        dokumen_form = DokumenForm(request.POST, request.FILES)
        if dokumen_form.is_valid():
            dokumen = dokumen_form.save(commit=False)

            # Tambahkan pengecekan apakah pengguna terotentikasi
            if request.user.is_authenticated:
                dokumen.user = request.user
                messages.success(request, 'Dokumen berhasil diunggah oleh pengguna terotentikasi. Terima kasih!')
            else:
                # Pengguna tidak terotentikasi, set user ke None
                dokumen.user = None
                messages.success(request, 'Dokumen berhasil diunggah tanpa login. Terima kasih!')

            dokumen.save()

    else:
        dokumen_form = DokumenForm()

    # Tidak menggunakan Paginator untuk menampilkan semua posting
    post_list = queryset

    data = {
        'data': queryset,
        'post_list': post_list,
        'randompost': randompost,
        'kategori': kategori,
        'headline_list': headline_list,
        'dokumen_form': dokumen_form,
        'program_pendidikan_data': program_pendidikan_data,
    }

    return render(request, "blog/index.html", data)

@csp_exempt
def list_user(request):
    dokumen_list = Dokumen.objects.all()
    return render(request, 'blog/list_user.html', {'dokumen_list': dokumen_list})

@csp_exempt
def PostDetail(request, slug):
    dt = Post.objects.filter(status=1).select_related('kategori').get(slug=slug)
    # print(dt.slug)
    kategori = Kategori.objects.all()
    queryset = Post.objects.all().filter(status=1)
    randompost = random.sample(list(queryset), min(len(queryset),6))
    data = {
        'post':dt,
        'randompost':randompost,
        'kategori':kategori
    }
    return render(request,"blog/detailpost.html",data)

@csp_exempt
def tagged(request, slug):
    kategori = Kategori.objects.all()
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    posts = Post.objects.filter(tags=tag,status=1)
    queryset = Post.objects.all().filter(status=1)
    randompost = random.sample(list(queryset), min(len(queryset),4))
    
    paginator = Paginator(posts, 5)  # 3 posts in each page
    page = request.GET.get('page')
    # q = request.GET.get('q')

    # print(ht)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    
    context = {
        'slug':slug,
        'hitung':posts.count(),
        'tag':tag,
        'post_list':post_list,
        'randompost':randompost,
        'kategori':kategori,
        'page':page,
    }
    # for x in posts:
        # print(x.created_on)
    return render(request, 'blog/tag.html', context)

@csp_exempt
def KategoriShow(request, slug):
    dt = Post.objects.all().select_related('kategori').filter(status=1,kategori__kategori__contains=slug)
    # for x in dt:
        # print(x)
    # dt = Kategori.objects.all().filter(kategori__contains=slug)
    kategori = Kategori.objects.all()
    namakategori = Kategori.objects.all().filter(kategori__contains=slug).first()
    queryset = Post.objects.all().filter(status=1)
    randompost = random.sample(list(queryset), min(len(queryset),3))
    
    paginator = Paginator(dt, 5)  # 3 posts in each page
    page = request.GET.get('page')
    # q = request.GET.get('q')

    # print(ht)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    
    data = {
        'namakategori':namakategori,
        'hitung':dt.count(),
        'slug':slug,
        'post':dt,
        'randompost':randompost,
        'kategori':kategori,
        'page':page,
        'post_list': post_list,
    }
    return render(request,"blog/kategori.html",data)

@csp_exempt
def hand404(request,exception):
    queryset = Post.objects.all().filter(status=1)
    kategori = Kategori.objects.all()
    randompost = random.sample(list(queryset), min(len(queryset),4))
    data = {
        'randompost':randompost,
        'kategori':kategori,
    }
    return render(request,"blog/404.html",data)
    
@csp_exempt    
def hand500(request):
    return render(request, 'blog/500.html', status=500)
#     # return HttpResponse(dt)
    
# API
@api_view(['GET', ])
def APIPostList(request):
    kategori = Kategori.objects.all()
    queryset = Post.objects.filter(status=1).all()
    randompost = random.sample(list(queryset), min(len(queryset),4))
    data = []
    nextPage = 1
    previousPage = 1
    paginator = Paginator(queryset, 5)  # 3 posts in each page
    page = request.GET.get('page', 1)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    
    serializer = ArticleSerializer(data,context={'request': request},many=True)
    kat = KategoriSerializer(kategori ,many=True)    
    randompostt = ArticleSerializer(randompost,many=True)
    
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    
    data = {
        'data':serializer.data,
        'kategori': kat.data,
        'randompost': randompostt.data,
        'halaman': "cobaa",
        'count': paginator.count, 
        'numpages' : paginator.num_pages, 
        'nextlink': '/api/?page=' + str(nextPage), 
        'prevlink': '/api/?page=' + str(previousPage)

    }

    return Response(data)
    # return render(request,"blog/index.html",data) 

def APIPostDetail(request, slug):
    dt = Post.objects.filter(status=1).select_related('kategori').get(slug=slug)
    # print(dt.slug)
    kategori = Kategori.objects.all()
    queryset = Post.objects.all().filter(status=1)
    randompost = random.sample(list(queryset), min(len(queryset),4))
    data = {
        'post':dt,
        'randompost':randompost,
        'kategori':kategori
    }
    return render(request,"blog/detailpost.html",data)



