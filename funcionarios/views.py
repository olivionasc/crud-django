from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg, Sum
from .models import Funcionario
from .forms import FuncionarioForm
import json
from django.http import JsonResponse


def lista_funcionarios(request):

    funcionarios = Funcionario.objects.all().order_by('nome')

    total_funcionarios = funcionarios.count()

    media_salarial = funcionarios.aggregate(
        media=Avg('salario')
    )['media']

    total_departamentos = (
        funcionarios.values('departamento')
        .distinct()
        .count()
    )

    ativos = funcionarios.filter(ativo=True).count()

    percentual_ativos = 0

    if total_funcionarios > 0:
        percentual_ativos = round(
            (ativos / total_funcionarios) * 100
        )

    context = {
        'funcionarios': funcionarios,
        'total_funcionarios': total_funcionarios,
        'media_salarial': media_salarial,
        'total_departamentos': total_departamentos,
        'percentual_ativos': percentual_ativos
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

    funcionarios_cidade = (
    Funcionario.objects
    .values('cidade')
    .annotate(total=Count('id'))
    )

    cargos = (
    Funcionario.objects
    .values('cargo')
    .annotate(total=Count('id'))
    .order_by('-total')[:5]
    )

    salario_modelo = (
    Funcionario.objects
    .values('modelo_trabalho')
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
        'inativos': inativos,
        'cidades': list(funcionarios_cidade),
        'cargos': list(cargos),
        'salario_modelo': list(salario_modelo)
    }

    return render(request, 'funcionarios/dashboard.html', context)


def chat_page(request):
    """Renderiza a página principal do Chatbot."""
    return render(request, 'funcionarios/chat.html')


from django.views.decorators.csrf import csrf_exempt
from .chatbot.engine import process_message

@csrf_exempt
def chat_api(request):
    """Endpoint da API que processa a mensagem e retorna a resposta."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            response = process_message(message)
            return JsonResponse({'response': response})
        except Exception as e:
            return JsonResponse({'response': f"Erro ao processar: {str(e)}"}, status=400)
    return JsonResponse({'response': 'Método não permitido'}, status=405)


