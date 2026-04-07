from django.shortcuts import render
from catalog.models import Produto, Categoria
from sales.models import Sale, SaleItem
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_operador(user):
    return user.groups.filter(name='Operador').exists()

@login_required
def dashboard(request):
    if not request.user.groups.filter(name='Admin').exists():
        raise PermissionDenied  # ✅ AQUI

    hoje = timezone.now().date()
    mes = hoje.month
    ano = hoje.year

    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()
    total_vendas = Sale.objects.count()

    faturamento_total = Sale.objects.aggregate(
        total=Sum('total')
    )['total'] or 0

    vendas_hoje = Sale.objects.filter(date=hoje).count()

    faturamento_hoje = Sale.objects.filter(date=hoje).aggregate(
        total=Sum('total')
    )['total'] or 0

    vendas_mes = Sale.objects.filter(
        date__month=mes,
        date__year=ano
    ).count()

    faturamento_mes = Sale.objects.filter(
        date__month=mes,
        date__year=ano
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    ultimas_vendas = Sale.objects.order_by('-date')[:5]

    top_produtos = (
        SaleItem.objects
        .values('product__nome')
        .annotate(total_vendido=Sum('quantity'))
        .order_by('-total_vendido')[:5]
    )

    estoque_baixo = Produto.objects.filter(estoque__lte=5)

    context = {
        'total_produtos': total_produtos,
        'total_categorias': total_categorias,
        'total_vendas': total_vendas,
        'faturamento_total': faturamento_total,
        'vendas_hoje': vendas_hoje,
        'faturamento_hoje': faturamento_hoje,
        'vendas_mes': vendas_mes,
        'faturamento_mes': faturamento_mes,
        'ultimas_vendas': ultimas_vendas,
        'top_produtos': top_produtos,
        'estoque_baixo': estoque_baixo,
    }

    return render(request, 'dashboard/dashboard.html', context)