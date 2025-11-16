def validar_cns(cns: str) -> bool:
    """
    Valida o CNS com base em tamanho e dígito verificador.
    Retorna True se válido, False caso contrário.
    """
    if not cns or len(cns) != 15 or not cns.isdigit():
        return False

    soma = sum(int(cns[i]) * (15 - i) for i in range(15))
    return soma % 11 == 0
