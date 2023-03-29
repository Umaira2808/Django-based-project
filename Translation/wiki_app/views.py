from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from wikipediaapi import Wikipedia
from .models import Project, Sentence
import json
from django.http import JsonResponse, HttpResponse
from django.contrib import messages

def home(request):
    return render(request, 'wiki_app/home.html')

def dashboard(request):
    project = list(Project.objects.all().values_list())
    lang_dict = {
        "bn":"Bengali",
        "gu":"Gujarati",
        "hi":"Hindi",
        "kn":"Kannada",
        "ml":"Malayala",
        "mr":"Marathi",
        "ne":"Nepali",
        "or":"Oriya",
        "pa":"Punjabi",
        "si":"Sinhala",
        "ta":"Tamil",
        "te":"Telugu",
        "ur":"Urdu",
    }
    new_project = []
    for itm in project:
        new_itm = (itm[0],itm[1],lang_dict[itm[2]])
        new_project.append(new_itm)
    context = {'Project_Table': new_project}
    return render(request, 'wiki_app/dashboard.html', context)

def extract(title):
    summary = Wikipedia().page(title).summary
    return summary

def preprocessing(summary):
    sentences = summary.split(". ")
    return sentences

def submit(request):
    if request.method == 'POST':
        title = request.POST.get('article-title')
        language = request.POST.get('target-language')
        project_exists = Project.objects.filter(wiki_article=title, tar_lang= language).exists()
        if not project_exists:
            Project.objects.create(wiki_article=title, tar_lang=language)
            project = Project.objects.get(wiki_article=title, tar_lang=language)
            proj = project.project_id
            project = Project.objects.get(project_id=proj)
            summary = extract(title)
            sentences = preprocessing(summary)
            sent_id = []
            for idx,sentence in enumerate(sentences):
                Sentence.objects.create(sentence_id=idx, original_sentence=sentence, project=project)
                sent_id.append(idx)
            context = {'sentences': sentences, 'project_id': proj, 'sentence_id': sent_id,}
            return render(request, 'wiki_app/sentence.html', context)
       
        else:
            messages.warning(request, 'Project already exists!')
            return render('home')
    else:
        return redirect('home')
 
def save_translations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        translations = data['translations']
        sentences = data['sentences']
        proj_id = data['proj_id']
        for i in range(len(sentences)):
            sentence = Sentence.objects.get(sentence_id=i, project = proj_id)
            sentence.translated_sentence = translations[i]
            sentence.save()
        return JsonResponse({'success': True})
    else:
        sentences = Sentence.objects.all()
        context = {'sentences': sentences}
        return render(request, 'base/sentence.html', context)

def display(request):
    if request.method == 'POST':
        proj_id = request.POST.get('id')
        title = request.POST.get('title')
        lang = request.POST.get('lang')
        print(proj_id,title,lang)
        sentence = Sentence.objects.get(project = proj_id)
        original_sent = sentence.original_sentence
        translated_sent = sentence.translated_sentence
        sent_id = sentence.sentence_id
        context = {'sentences': original_sent, 'project_id': proj_id, 'sentence_id': sent_id,"translated_sentences": translated_sent}
        print('CONTEXT',context)
        return render(request, 'wiki_app/sentence.html', context)
    else:
        return HttpResponse('Invalid request method.')