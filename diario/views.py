from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pessoa, Diario


# Create your views here.
def home(request):
    textos = Diario.objects.all().order_by('created_at') [:3]
    return render(request, 'home.html', {'texto': textos} )

def escrever(request):
    if request.method == 'GET':
       pessoa = Pessoa.objects.all()
       return render(request, 'escrever.html', {'pessoa': pessoa})
    elif request.method == 'POST':
       titulo = request.POST.get('titulo')
       tags = request.POST.getlist('tags')
       pessoas = request.POST.getlist('pessoas')
       texto = request.POST.get('texto')
       
       if len(titulo.strip()) == 0 or len(texto.strip()) == 0:
           return HttpResponse('Por favor, preencha todos os campos')
       
       diario=Diario(
           titulo=titulo,
           texto=texto
       )
       diario.set_tag (tags)
       diario.save()
       
       for i in pessoas:
           pessoa = Pessoa.objects.get(id=i)
           diario.pessoa.add(pessoa)
           diario.save()
       
       return redirect('home')
   
def cadastrar_pessoa(request):
    if request.method == 'GET':
        return render(request, 'pessoa.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')
        
        pessoa=Pessoa(
            nome=nome,
            fotos=foto
        )
        
        pessoa.save()
        return redirect('escrever')