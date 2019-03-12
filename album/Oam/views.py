from django.shortcuts import render
from django.http import HttpResponse
from Oam.models import Pictures
from django.views.decorators.csrf import csrf_exempt
import time,os
from PIL import Image
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.#
def index(request):
	'''主页'''
	return render(request,"Oam/index.html")

def ul(request):
	'''上传图片表单'''
	return render(request,"Oam/ul.html")

@csrf_exempt
def upload(request):
	'''执行图片上传'''
	t=time.time()
	myfile=request.FILES.get("picture",None)

	if not myfile:
		context = {"info":"没有上传相片信息！"}
		return render(request,"Oam/info.html",context)
	else:
		filename=str(t)+"."+myfile.name.split('.').pop()
		destination=open("./static/"+filename,"wb+")
		# 分块写入文件
		for chunk in myfile.chunks():
			destination.write(chunk)
		destination.close()

		#获取并封装图片信息
		try:
			p = Pictures()
			p.title = request.POST['title']
			p.time = datetime.now()
			p.name=filename
			p.text = request.POST['text']
			img = Image.open("./static/"+filename)
			p.size=str(img.size[0])+"*"+str(img.size[1])
			p.save()
			context = {"info":"添加成功！"}
		except:
			context = {"info":"添加失败！"}
		return render(request,"Oam/info.html",context)

def check(request,pIndex):
	'''浏览信息'''
	list=Pictures.objects.all()
	if not list:
		context = {"info":"哎呀，都没有照片你浏览个啥啊，赶紧添加啊！"}
		return render(request,"Oam/info2.html",context)
	else:
		'''分页显示'''
		p=Paginator(list,2)# 两个图片一页
		if pIndex == "":
			pIndex="1"
		list2 = p.page(pIndex)
		plist = p.page_range
		context = {"ulist":list2,"plist":plist,"pIndex":pIndex}
		return render(request, 'Oam/check.html',context)

def delete(request,pid):
	'''删除操作'''
	try:
		ob = Pictures.objects.get(id=pid)
		ob.delete()
		os.remove("./static/"+ob.name)
		context = {"info":"删除成功！"}
	except:
		context = {"info":"删除失败！"}
	return render(request,"Oam/info.html",context)

def edit(request,pid):
	'''修改操作'''
	try:
		ob = Pictures.objects.get(id=pid)
		context={"pic":ob}
		return render(request,"Oam/edit.html",context)
	except:
		context = {"info":"没有找到要修改的相片！"}
		return render(request,"Oam/info.html",context)

def update(request):
	'''更新信息'''
	try:
		t=time.time()

		p = Pictures.objects.get(id=request.POST['pid'])

		'''执行新图片上传'''
		myfile=request.FILES.get("picture",None)

		if myfile:
			'''删除原图片'''
			p = Pictures.objects.get(id=request.POST['pid'])
			os.remove("./static/"+p.name)
			filename=str(t)+"."+myfile.name.split('.').pop()
			destination=open("./static/"+filename,"wb+")
			# 分块写入文件
			for chunk in myfile.chunks():
				destination.write(chunk)
			destination.close()
			img = Image.open("./static/"+filename)
			p.size=str(img.size[0])+"*"+str(img.size[1])
			p.time = datetime.now()
			p.name = filename

		'''执行信息修改'''
		if request.POST['title']:
			p.title = request.POST['title']
			p.time = datetime.now()

		if request.POST['text']:
			p.text = request.POST['text']
			p.time = datetime.now()

		p.save()
		context = {"info":"修改成功！"}
	except Exception as err:
		print(err)
		context = {"info":"修改失败！"}
	return render(request,"Oam/info.html",context)
