from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from .models import Question, Choices
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import PollForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def landing(request):
    return render(request, 'vote/landing.html')


@login_required
def home(request):
    return render(request, 'vote/home.html')
    





def signup(request):
    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('vote:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
    
    
class PollList(LoginRequiredMixin, ListView):
    model = Question
    context_object_name = 'questions'
    
    def get_queryset(self):
        return Question.objects.filter(owner=self.request.user)

class PollDetails(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'vote/poll_details.html'
    
    def get_queryset(self):
        return Question.objects.filter(owner=self.request.user)
        

class PollResults(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'vote/results.html'

    def get_queryset(self):
        return Question.objects.filter(owner=self.request.user)
        
@login_required        
def create(request):
    
    if (request.method == 'POST'):
        form = PollForm(request.POST)
        
        if (form.is_valid()):
            question = form.cleaned_data.get('question_text')
            choice1 = form.cleaned_data.get('choice_text')
            choice2 = form.cleaned_data.get('choice_text2')
            
            
            q = Question.objects.create(question_text=question, owner=request.user)
            q1 = Question.objects.get(id=q.id)
            
            
            q1.choices_set.create(choice_text=choice1, owner=request.user)
            q1.choices_set.create(choice_text=choice2, owner=request.user)

            
            return redirect('vote:poll-details', q.id)
    else:
        form = PollForm()
    return render(request, 'forms/poll_form.html', {'form': form})
            


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices_set.get(pk=request.POST['choice'])
    except (KeyError, Choices.DoesNotExist):
        return render(request, 'vote/poll_details.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        
    return HttpResponseRedirect(reverse('vote:results', args=(question.id,)))
        