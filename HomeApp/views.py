# pip uninstall google-generativeai google-api-core requests urllib3
# pip install --no-cache-dir google-generativeai => both are out dated
# pip install --no-cache-dir google-genai => updated && run server by cmd or bash // ps==import error
from django.shortcuts import render,redirect
from api.models import Section,Subject,Material
from .models import SecAdmin,Ai
from .forms import AdminForm,SubjectFrom,MaterialForm
from django.conf import settings
import os
# Create your views here.

def Sections(request):
    if request.method=='POST':
        if request.POST.get('type')=='dsec':
            pk=request.POST.get('pk')
            name=request.POST['name']
            try:
                sec=Section.objects.get(id=pk)
                # i didn't know this until end of my project=> mat.subject.section
                if sec and SecAdmin.objects.filter(name=name,section=sec).exists():
                    SecAdmin.objects.filter(section=sec).delete()
                    sec.delete()
            except Exception:pass

        if request.POST.get('type')=='dsub':
            pk=request.POST.get('pk')
            sepk=request.POST.get('spk')
            name=request.POST['name']
            try:
                sub=Subject.objects.get(id=pk)
                sec=Section.objects.get(id=sepk)
                if sec and SecAdmin.objects.filter(name=name,section=sec).exists():
                    sub.delete()
            except Exception:pass

        if request.POST.get('type')=='sch':
            name=request.POST.get('name')
            batch=request.POST.get('batch')
            try:
                if name and batch:
                    name=name.upper()
                    sections=Section.objects.prefetch_related('subjects').filter(name=name,batch=batch)
                elif name:
                    name=name.upper()
                    sections=Section.objects.prefetch_related('subjects').filter(name=name)
                elif batch:
                    sections=Section.objects.prefetch_related('subjects').filter(batch=batch)
                if sections.exists():
                    return render(request,'index.html',{'sections':sections})
            except Exception:
                pass

    sections=Section.objects.prefetch_related('subjects').all()
    return render(request,'index.html',{'sections':sections})

def Materials(request):
    subject=request.GET.get('subject')
    response=''

    if request.method=='POST' and request.POST.get('query',False):
        asked=request.POST.get('query')
        url=request.POST.get('path')
        relative_path = url.replace(settings.MEDIA_URL, "") 
        file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        print(asked,file_path)
        try:
            AskAI=Ai(asked,file_path)
            res=AskAI.process()
            response=res
        except Exception as e:
            response=e

    
    if request.method=='POST' and not request.POST.get('query',None):
        pk=request.POST.get('pk')
        name=request.POST['name']
        try:
            mat=Material.objects.get(id=pk)
            # i didn't know this until end of my project=> mat.subject.section
            if mat and SecAdmin.objects.filter(name=name,section=mat.subject.section).exists():
                mat.delete()
        except Exception:pass

    materials=[]
    if subject:
        data=subject
        i,n=data.index('[')+1,len(data)-1 #i to get section name combined with batch
        sname=data[i:n]
        sn=sname[:-6] #extracting section name
        sb=int(sname[-6:][1:-1]) #extracting batch
        #print(sname,sn,sb)
        sec=Section.objects.get(name=sn,batch=sb)
        try:
            sub_materials=Subject.objects.prefetch_related('materials').get(name=data[:i-1],section=sec)
            materials=sub_materials.materials.all()
        except Exception:pass
            
    return render(request,'materials.html',{'materials':materials,'subject':subject,'response':response})

def Register(request):
    reason=''
    if request.method=='POST':
        form=AdminForm(request.POST)        
        if form.is_valid():
            form.save()
            name=form.cleaned_data.get('name') #both have same usecases
            sec=form.cleaned_data['section']
            return  render(request,'register.html',{'success': f'Hey! {name} you got Admin access for {sec} Section'})          
        else:reason=form.errors

    return  render(request,'register.html',{'message':reason})

def Addsubject(request):
    if request.method=='POST':
        if request.POST!=None:
            form=SubjectFrom(request.POST,user=request.POST.get('uname'))
            if form.is_valid():
                try:
                    form.save()
                    return redirect('sections')
                except Exception as e:
                    form.add_error(None,e)
            return render(request,'errors.html',{'errors':form.errors})
    return redirect('sections')

def AddMatrial(request):
    subject=request.GET.get('subject')
    if request.method=='POST':
        message='Your Username is invalid!'
        if SecAdmin.objects.filter(name=request.POST['uname']).exists():
            form=MaterialForm(request.POST,request.FILES,subject=subject)
            if form.is_valid():
                form.save()
                return render(request,'uploadmat.html',{'sub':subject,'success':subject+' material uploaded successfully!'})
            else:return render(request,'uploadmat.html',{'sub':subject,'message':form.errors,'sub':subject})
        else:return render(request,'uploadmat.html',{'sub':subject,'message':message})
    return render(request,'uploadmat.html',{'sub':subject})

def Features(request):
    return render(request,'about.html')