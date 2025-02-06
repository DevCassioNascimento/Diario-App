from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pessoa, Diario
from datetime import datetime , timedelta
import json

def home(request):
    textos = Diario.objects.all().order_by('created_at')[:3]
    pessoas = Pessoa.objects.all()
    
    # Coleta os nomes e contagens
    nomes = [pessoa.nome for pessoa in pessoas]
    qtds = [Diario.objects.filter(pessoas=pessoa).count() for pessoa in pessoas]

    # Converte para JSON para evitar problemas no template
    context = {
        'textos': textos,
        'nomes': json.dumps(nomes),  # Serializa os nomes como JSON
        'qtds': json.dumps(qtds),   # Serializa as contagens como JSON
    }

    return render(request, 'home.html', context)
    
    
    return render(request, 'home.html', {'textos': textos, 'nomes': nomes, 'qtds': qtds})

def escrever(request):
    if request.method == 'GET':
        pessoas = Pessoa.objects.all()
        return render(request, 'escrever.html', {'pessoas': pessoas})
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        pessoas_ids = request.POST.getlist('pessoas')
        texto = request.POST.get('texto')

        if not titulo.strip() or not texto.strip():
            return HttpResponse('Por favor, preencha todos os campos')

        diario = Diario(
            titulo=titulo,
            texto=texto
        )
        diario.save()  
        
        if hasattr(diario, "tags"):
            diario.tags.set(tags)  # Certifique-se de que Diario tem um campo ManyToMany chamado tags

        for i in pessoas_ids:
            pessoa = Pessoa.objects.get(id=i)
            diario.pessoa.add(pessoa)
        
        diario.save()
        return redirect('escrever')

def cadastrar_pessoa(request):
    if request.method == 'GET':
        return render(request, 'pessoa.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')

        pessoa = Pessoa(
            nome=nome,
            fotos=foto  
        )
        
        pessoa.save()
        return redirect('escrever')
    
def dia(request):
        data = request.GET.get('data')
        dataformatada = datetime.strptime(data, '%Y-%m-%d').date()
        diarios = Diario.objects.filter(created_at__gte=dataformatada). filter(created_at__lte=dataformatada + timedelta(days=1))
        return render(request, 'dia.html' , {'diarios': diarios , 'total': diarios.count(), 'data': data})
    
def excluir_dia(request):
        dia = datetime.strptime(request.GET.get('data'), '%Y-%m-%d')
        diarios = Diario.objects.filter(created_at__gte=dia). filter(created_at__lte=dia + timedelta(days=1))
        diarios.delete()
