from django.shortcuts import render
import ocvgui
import tkinter
from . import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from .models import Person, PersonImage,PersonBuffer
from face import face
import urllib, json


from django.views.decorators import gzip
from django.http import StreamingHttpResponse,HttpResponseServerError
from django.contrib.auth.decorators import login_required


from CONFIG import *
import cv2
import numpy as np
import mmap
from posix_ipc import Semaphore, SharedMemory, ExistentialError
from ctypes import sizeof, memmove, addressof, create_string_buffer
from time import sleep

from structures import MD

md_buf = create_string_buffer(sizeof(MD))


class ShmRead:
    def __init__(self, name):
        self.shm_buf = None
        self.md_buf = None

        while not self.md_buf:
            try:
                print("Waiting for MetaData shared memory is available.")
                md_region = SharedMemory(name + '-meta')
                self.md_buf = mmap.mmap(md_region.fd, sizeof(MD))
                md_region.close_fd()
                sleep(1)
            except ExistentialError:
                sleep(1)

        self.shm_name = name
        self.sem = Semaphore(name, 0)

    def get(self):
        md = MD()

        self.sem.acquire()
        md_buf[:] = self.md_buf
        memmove(addressof(md), md_buf, sizeof(md))
        self.sem.release()

        while not self.shm_buf:
            try:
                print("Waiting for Data shared memory is available.")
                shm_region = SharedMemory(name=self.shm_name)
                self.shm_buf = mmap.mmap(shm_region.fd, md.size)
                shm_region.close_fd()
                sleep(1)
            except ExistentialError:
                sleep(1)

        self.sem.acquire()
        f = np.ndarray(shape=(md.shape_0, md.shape_1, md.shape_2), dtype='uint8', buffer=self.shm_buf)
        self.sem.release()
        return f

    def release(self):
        self.md_buf.close()
        self.shm_buf.close()





@login_required
def search(request):
    id = request.GET.get('q')
    return HttpResponseRedirect(reverse('hq:profile',args=(id,)))

@login_required
def capImg(request,id,name): 

    folder_name = name+"-"+id
    if folder_name not in os.listdir("./media/"):
        os.mkdir("./media/"+folder_name)

    # for i in range(0,6):
    #     try:
    #         ocvgui.App(tkinter.Tk(), "{} {}".format(id,name),video_source = i,path="./media/"+name)
    #         break
    #     except Exception as e:
    #         print(e)
    #         pass
    ocvgui.App(tkinter.Tk(), "{} {}".format(id,name),video_source = WEB_CAM,path="./media/"+folder_name)
    profile_obj = Person.objects.get(id_number=id)
    for x in os.listdir(os.path.join("media",folder_name)):
        obj = PersonImage(person=profile_obj,pictures=os.path.join(folder_name,x))
        obj.save()
    return HttpResponseRedirect(reverse('hq:profile',args=(id,)))

@login_required
def new_entry(request):
    form = forms.PersonBufferForm()
    if request.method == "POST":
        form = forms.PersonBufferForm(request.POST)
        id = request.POST['list_of_people']
        buffer_entry = PersonBuffer.objects.get(id_number=id)
        name = buffer_entry.name
        buffer_entry.delete()

        new_entry = Person(name=name,id_number=id)
        new_entry.save()
        
        return HttpResponseRedirect(reverse('hq:capImg',args=(id,name.replace(' ',''))))

    return render(request,"hq/new_entry_t.html",{"form":form})

@login_required
def profile(request,id):
    
    profile_obj = Person.objects.filter(id_number=id)
    
    if len(profile_obj)==0:
        return render(request,"hq/no_profile.html")

    profile_obj = profile_obj[0]
    profile_image_obj = PersonImage.objects.filter(person=profile_obj)

    return render(request,"hq/profile.html",{"profile_obj":profile_obj,
                                          "profile_image_obj":profile_image_obj})

@login_required
def deleteimg(request,pid,imgid):
    PersonImage.objects.get(id=imgid).delete()
    name = Person.objects.get(id_number=pid).name

    if len(os.listdir(os.path.join("media",name.replace(' ',''))))==0:
        os.rmdir(os.path.join("media",name.replace(' ','')))

    return HttpResponseRedirect(reverse('hq:profile',args=(pid,)))

# @login_required
def gen():
    shm_r = ShmRead('abc')
    while True:
        frame = shm_r.get()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame =  jpeg.tobytes()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    #return HttpResponseRedirect(reverse('hq:new_entry'))

# @login_required
@gzip.gzip_page
def startstream(request): 
    try:
        return StreamingHttpResponse(gen(),content_type="multipart/x-mixed-replace;boundary=frame")
    except HttpResponseServerError as e:
        print("aborted")

@login_required
def streamer(request):
        return render(request,"hq/streamer.html")

@login_required
def sync(request):
    #Sync API GOES HERE
    #url = 
    #response = urllib.urlopen(url)

    #JSON RESPONSE Example
    response = {"Vinayak":"200","Mikkal":"123L"}

    for name,id_number in response.items():
        entry = PersonBuffer(id_number=id_number,name=name)
        entry.save()

    return HttpResponseRedirect(reverse('hq:new_entry'))


@login_required
def delete_entry(request,id):
    
    obj = Person.objects.get(id_number=id)
    obj.delete()

    return HttpResponseRedirect(reverse('hq:new_entry'))

@login_required
def edit_entry(request,id):
    
    if request.method == "POST":
        id_new = request.POST.get('id')
        name_new = request.POST.get('name')

        obj = Person.objects.get(id_number=id)
        person = obj
        obj.id_number = id_new
        old_name = obj.name
        obj.name = name_new
        obj.save()
        
        old_folder_name = old_name+"-"+id
        new_folder_name = name_new+"-"+id_new


        try:
            os.rename(os.path.join('media',old_folder_name),os.path.join('media',new_folder_name))
        except:
            pass

        obj = PersonImage.objects.filter(person=person)

        for o in obj:
            url = o.pictures.url.split("/")
            url[2] = new_folder_name
            o.pictures = r"/".join(list(url[2:]))
            o.save()

        return HttpResponseRedirect(reverse('hq:profile',args=(id_new,)))
    
    return render(request,"hq/edit.html",)