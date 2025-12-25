from django.forms import ModelForm
from .models import SecAdmin
from django.core.exceptions import ValidationError
from api.models import Section,Subject,Material
class AdminForm(ModelForm):
    class Meta:
        model=SecAdmin
        fields=['name','email','section']

    def clean_name(self):
        data=self.cleaned_data['name']
        data=data.strip().lower()
        dup=SecAdmin.objects.filter(name=data).exists()
        if dup:
            raise ValidationError(f'This username is already in use.')
        return data
    
    def clean_email(self):
        mail=self.cleaned_data['email']
        dups=SecAdmin.objects.filter(email=mail)
        if dups.exists():raise ValidationError(f'This College Email ID is already in use.')
        if not mail[:2].isdigit() or not mail.endswith('@qiscet.edu.in'):
            raise ValidationError(f'This is not recognized as College Email ID.')
        return mail
    
    def clean(self):
        cleaned_data = super().clean()
        sec = cleaned_data.get('section')
        num=False        
        em=cleaned_data.get('email')
        data=''
        if not sec or not em: return cleaned_data
        for d in sec:
            if d!=' ':data+=d
            if d.isdigit():num=True
        if not num or '-' not in sec:
            raise ValidationError(f'This is not recognized as section, Example : AIML-5.')
        batch='20'
        if em:batch = '20' + em[:2]
        Section.objects.get_or_create(name=data,batch=batch)
        data+=f'[{batch}]'
        cleaned_data['section']=data.upper()
        count = SecAdmin.objects.filter(section=cleaned_data['section']).count()
        if count>=5: raise ValidationError(f'Registrations are limited for 5 Students in {sec}!')

        return cleaned_data

class SubjectFrom(ModelForm):
    class Meta:
        model=Subject
        fields=['name'] #add section dynamically from user data

    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super().__init__(*args,**kwargs)

    def save(self, commit = True):
        subject=super().save(commit=False)
        if self.user:
            admin=SecAdmin.objects.filter(name=self.user).first()            
            if not admin:
                raise ValidationError(f'Unable to add subject because of Username is not admin or invalid!')
            
            sec=Section.objects.filter(name=admin.section[:-6],
            batch=admin.section[-5:len(admin.section)-1]).first()#because no reverse mapping[foreignkey]
            if not sec:
                raise ValidationError(f'Unable to add subject because your not admin of this Section!')
            
            sub=Subject.objects.filter(name=subject.name,section=sec)
            if sub.exists():raise ValidationError(f'Subject already exists in this section!')

            subject.section=sec         
        else:
            raise ValidationError(f'Unable to add subject because of Username is invalid!')
        if commit:subject.save()
        return subject
    
class MaterialForm(ModelForm):
    class Meta:
        model=Material
        fields=['name','material']

    def __init__(self,*args,**kwargs):
        self.subject=kwargs.pop('subject',None)
        super().__init__(*args,**kwargs)
    
    def save(self,commit=True):
        materiall=super().save(commit=False)
        data=self.subject
        i,n=data.index('[')+1,len(data)-1 #i to get section name combined with batch
        sname=data[i:n]
        sn=sname[:-6] #extracting section name
        sb=int(sname[-6:][1:-1]) #extracting batch
        sec=Section.objects.get(name=sn,batch=sb)
        sub=Subject.objects.filter(name=data[:i-1],section=sec).first()
        materiall.subject=sub
        print(data)
        if commit:materiall.save()
        return materiall