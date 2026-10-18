# Create your views here.
from multiprocessing import context

from django.contrib.auth.forms import UserCreationForm
from django.db.models.fields import return_None
from django.shortcuts import render,redirect
from learning_logs.models import Topic, Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
def index(request):
    return render(request, 'learning_logs/index.html')
@login_required
def topics(request):
    topics=Topic.objects.filter(owner=request.user).order_by('date_added')
    context={'topics_learnt':topics}
    return render(request, 'learning_logs/topics.html',context)
@login_required
def topic(request, topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries=topic.entry_set.order_by('-date')
    context={'topic':topic,'entries':entries}
    return render(request, 'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method !='POST':
        #No data submitted, create a blank form.
        form=TopicForm()
    else:
        form=TopicForm(data=request.POST)
        if form.is_valid():
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    context={'form':form}
    return render(request, 'learning_logs/new_topic.html',context)
@login_required
def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method !='POST':
        form=EntryForm()
    else:
        form=EntryForm(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id=topic_id)

    context={'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html',context)
@login_required
def edit_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    topic_id=entry.topic.id
    if topic.owner != request.user:
        raise Http404
    if request.method !='POST':
        form=EntryForm(instance=entry)
    else:
        form=EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id)
    context={'entry':entry,'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html',context)

@login_required
def edit_topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)

    if request.user != topic.owner:
        raise Http404

    if request.method != 'POST':
        form=TopicForm(instance=topic)

    else:
        form=TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic',topic_id=topic.id)

    context={'topic':topic, 'form':form}
    return render(request,'learning_logs/edit_topic.html',context)

@login_required
def delete_entry(request,entry_id):
    entry=Entry.objects.get(id=entry_id)
    topic=entry.topic
    if request.user != topic.owner:
         raise Http404

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    context= { 'entry':entry, 'topic':topic }
    return render(request,'learning_logs/delete_entry.html',context)

def register(request):
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()

            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))

            activation_link=request.build.absolute_url(f'/accounts/activate/{uid}/{token}/')

            send_mail(
                subject="Activate Your Learning Log Account",
                message=f"Hi,I'm Oba from learning Logs! Please click the link below to verify your account: \n\n{activation_link}",
               from_email='admin@learninglog.com',
                recipient_list=[user.email],)

            return render(request, 'registration/activation_pending.html')
    else:
        form=UserCreationForm()
    return render(request,'registration/register.html',{'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/activation_success.html')
    else:
        return render(request, 'registration/activation_invalid.html')
