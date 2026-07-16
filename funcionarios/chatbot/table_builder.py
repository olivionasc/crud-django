from django.db.models import QuerySet
from funcionarios.models import Funcionario
from .response import format_currency, get_display_name

def build_table(intent: str, data) -> dict:
    """
    Constrói a estrutura de dados para o componente de Tabela de Funcionários.
    """
    if not isinstance(data, list):
        if hasattr(data, 'iterator') or isinstance(data, QuerySet):
            data = list(data)
        else:
            data = []

    headers = ["Nome", "Cargo", "Departamento", "Salário", "Status"]
    rows = []

    for f in data:
        status_str = "Ativo" if f.ativo else "Inativo"
        dept_name = get_display_name('departamento', f.departamento)
        salary_str = format_currency(f.salario)
        rows.append([
            f.nome,
            f.cargo,
            dept_name,
            salary_str,
            status_str
        ])

    title = f"Tabela de Funcionários ({len(data)} encontrados)"
    return {
        "type": "table",
        "title": title,
        "headers": headers,
        "rows": rows
    }
