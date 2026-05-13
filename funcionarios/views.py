from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Sum
from .models import Funcionario
from .forms import FuncionarioForm
import json
from django.http import JsonResponse


def lista_funcionarios(request):

    funcionarios = Funcionario.objects.all().order_by('nome')

    context = {
        'funcionarios': funcionarios
    }

    return render(
        request,
        'funcionarios/lista.html',
        context
    )


def criar_funcionario(request):
    form = FuncionarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_funcionarios')
    return render(request, 'funcionarios/form.html', {'form': form})


def editar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    form = FuncionarioForm(request.POST or None, instance=funcionario)
    if form.is_valid():
        form.save()
        return redirect('lista_funcionarios')
    return render(request, 'funcionarios/form.html', {'form': form})


def deletar_funcionario(request, id):
    funcionario = get_object_or_404(Funcionario, id=id)
    funcionario.delete()
    return redirect('lista_funcionarios')


def dashboard(request):

    funcionarios_departamento = (
    Funcionario.objects
    .values('departamento')
    .annotate(total=Count('id'))
)

    funcionarios_escolaridade = (
        Funcionario.objects
        .values('escolaridade')
        .annotate(total=Count('id'))
    )

    funcionarios_modelo = (
        Funcionario.objects
        .values('modelo_trabalho')
        .annotate(total=Count('id'))
    )

    funcionarios_contrato = (
        Funcionario.objects
        .values('tipo_contrato')
        .annotate(total=Count('id'))
    )

    media_salario = (
    Funcionario.objects
    .values('departamento')
    .annotate(media=Avg('salario'))
)

    ativos = Funcionario.objects.filter(ativo=True).count()
    inativos = Funcionario.objects.filter(ativo=False).count()

    context = {
        'departamentos': list(funcionarios_departamento),
        'escolaridade': list(funcionarios_escolaridade),
        'modelo': list(funcionarios_modelo),
        'contrato': list(funcionarios_contrato),
        'salarios': list(media_salario),
        'ativos': ativos,
        'inativos': inativos
    }

    return render(request, 'funcionarios/dashboard.html', context)