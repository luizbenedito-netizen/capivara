from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from urllib.parse import urlencode

def build_querystring(filters, filter_config, exclude=None):
    """
    Constrói querystring a partir do dict de filtros
    """
    exclude = set(exclude or [])

    params = [
        (k, filters[k])
        for k in filter_config.keys()
        if k in filters
        and k not in exclude
    ]

    return urlencode(params)


def extract_filters(request, filter_config):
    """
    Extrai os valores do request.GET aplicando defaults
    """
    raw = request.GET
    return {
        key: raw.get(key, config.get("default"))
        for key, config in filter_config.items()
    }


def apply_filters(qs, filters, filter_config):
    
    OPERATOR_MAP = {
        "0": lambda qs, f, v: qs.filter(**{f: v}),
        "1": lambda qs, f, v: qs.filter(**{f"{f}__icontains": v}),
        "2": lambda qs, f, v: qs.exclude(**{f"{f}__icontains": v}),
    }
    
    
    for key, config in filter_config.items():
        field = config.get("field")
        apply_if = config.get("apply_if")
        validate = config.get("validate")
        transform = config.get("transform")

        operator_param = config.get("operator_param")
        default_operator = config.get("default_operator", "0")

        if not field or not apply_if:
            continue

        value = filters.get(key)

        if not apply_if(value):
            continue

        if validate and not validate(value):
            raise ValidationError(f"Filtro inválido: {key}")

        if transform:
            value = transform(value)

        operator = filters.get(operator_param, default_operator)
        operator_fn = OPERATOR_MAP.get(operator)

        if not operator_fn:
            raise ValidationError(f"Operador inválido: {operator}")

        qs = operator_fn(qs, field, value)

    return qs


def paginate(qs, page, per_page=9):
    """
    Paginação padrão
    """
    paginator = Paginator(qs, per_page)
    return paginator.get_page(page)