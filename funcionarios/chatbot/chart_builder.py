from django.db.models import Count, Avg
from funcionarios.models import Funcionario
from .response import get_display_name

def build_chart(chart_type: str, query_text: str) -> dict:
    """
    Constrói a estrutura de dados para gráficos do Chart.js.
    """
    text = query_text.lower().strip()

    # 1. Salário médio por setor
    if "salario" in text and ("setor" in text or "departamento" in text):
        data_query = Funcionario.objects.values('departamento').annotate(val=Avg('salario')).order_by('departamento')
        labels = [get_display_name('departamento', item['departamento']) for item in data_query]
        values = [float(item['val'] or 0.0) for item in data_query]
        return {
            "type": chart_type,
            "title": "Salário Médio por Setor",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Média Salarial (R$)",
                    "data": values
                }]
            }
        }

    # 2. Funcionários ativos por departamento
    elif "ativo" in text and ("setor" in text or "departamento" in text):
        data_query = Funcionario.objects.filter(ativo=True).values('departamento').annotate(val=Count('id')).order_by('departamento')
        labels = [get_display_name('departamento', item['departamento']) for item in data_query]
        values = [item['val'] for item in data_query]
        return {
            "type": chart_type,
            "title": "Funcionários Ativos por Setor",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Ativos",
                    "data": values
                }]
            }
        }

    # 3. Funcionários por setor / Distribuição por setor
    elif "setor" in text or "departamento" in text:
        data_query = Funcionario.objects.values('departamento').annotate(val=Count('id')).order_by('departamento')
        labels = [get_display_name('departamento', item['departamento']) for item in data_query]
        values = [item['val'] for item in data_query]
        return {
            "type": chart_type,
            "title": "Funcionários por Setor",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Quantidade de Colaboradores",
                    "data": values
                }]
            }
        }

    # 4. Funcionários por cargo / Distribuição por cargo
    elif "cargo" in text or "funcao" in text:
        data_query = Funcionario.objects.values('cargo').annotate(val=Count('id')).order_by('-val')
        labels = [item['cargo'] for item in data_query]
        values = [item['val'] for item in data_query]
        return {
            "type": chart_type,
            "title": "Distribuição de Colaboradores por Cargo",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Quantidade",
                    "data": values
                }]
            }
        }

    # 5. Ativos x Inativos
    elif any(k in text for k in ["ativo", "inativo", "situacao"]):
        ativos = Funcionario.objects.filter(ativo=True).count()
        inativos = Funcionario.objects.filter(ativo=False).count()
        return {
            "type": chart_type,
            "title": "Funcionários Ativos x Inativos",
            "data": {
                "labels": ["Ativos", "Inativos"],
                "datasets": [{
                    "label": "Quantidade de Colaboradores",
                    "data": [ativos, inativos]
                }]
            }
        }

    # 6. Contratações ao longo do tempo / Evolução / Crescimento
    elif any(k in text for k in ["contratac", "evoluc", "cresciment"]):
        funcionarios = Funcionario.objects.all().order_by('data_admissao')
        
        years = {}
        for f in funcionarios:
            year = f.data_admissao.year
            years[year] = years.get(year, 0) + 1
            
        sorted_years = sorted(years.keys())
        labels = [str(y) for y in sorted_years]
        
        values = []
        cumulative = 0
        for y in sorted_years:
            cumulative += years[y]
            values.append(cumulative)
            
        return {
            "type": chart_type,
            "title": "Evolução do Número de Funcionários",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": "Total Acumulado",
                    "data": values
                }]
            }
        }

    # Fallback genérico: Funcionários por setor
    data_query = Funcionario.objects.values('departamento').annotate(val=Count('id')).order_by('departamento')
    labels = [get_display_name('departamento', item['departamento']) for item in data_query]
    values = [item['val'] for item in data_query]
    return {
        "type": chart_type,
        "title": "Quantidade de Funcionários por Setor",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "Funcionários",
                "data": values
            }]
        }
    }
