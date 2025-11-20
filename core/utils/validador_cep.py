import unicodedata

# Dicionário de tipos de logradouro e seus códigos
CODIGOS_LOGRADOUROS = {
    "ACESSO": "001",
    "ADRO": "002",
    "ALAMEDA": "004",
    "ALTO": "005",
    "ATALHO": "007",
    "AVENIDA": "008",
    "BOULEVARD": "014",
    "BAIXA": "015",
    "ESTRADA": "031",
    "ESTACAO": "032",
    "FAZENDA": "037",
    "FERROVIA": "038",
    "ILHA": "050",
    "JARDIM": "052",
    "LADEIRA": "053",
    "LARGO": "054",
    "LAGOA": "055",
    "LOTEAMENTO": "056",
    "MORRO": "059",
    "MONTE": "060",
    "PARALELA": "062",
    "PASSEIO": "063",
    "PATIO": "064",
    "PRACA": "065",
    "PARADA": "067",
    "PRAIA": "070",
    "PARQUE": "072",
    "PASSARELA": "073",
    "PASSAGEM": "074",
    "PONTE": "076",
    "QUADRA": "077",
    "QUINTA": "079",
    "RUA": "081",
    "RAMAL": "082",
    "RECANTO": "087",
    "RETIRO": "088",
    "RETA": "089",
    "RODOVIA": "090",
    "RETORNO": "091",
    "CHACARA": "092",
    "SETOR": "095",
    "TERMINAL": "098",
    "TREVO": "099",
    "TRAVESSA": "100",
    "VIA": "101",
    "VIADUTO": "103",
    "VILA": "104",
    "VIELA": "105",
    "AREA": "472",
    "ESPLANADA": "474",
    "QUINTAS": "475",
    "ROTULA": "476",
    "MARINA": "477",
    "DESCIDA": "478",
    "CIRCULAR": "479",
    "UNIDADE": "480",
    "CHACARA": "481",
    "RAMPA": "482",
    "PONTA": "483",
    "VIA DE PEDESTRE": "484",
    "CONDOMINIO": "485",
    "NUCLEO HABITACIONAL": "486",
    "RESIDENCIAL": "487",
    "CANAL": "495",
    "BURACO": "496",
    "MODULO": "497",
    "ESTANCIA": "498",
    "LAGO": "499",
    "NUCLEO": "500",
    "AEROPORTO": "501",
    "PASSAGEM SUBTERRANEA": "502",
    "COMPLEXO VIARIO": "503",
    "PRACA DE ESPORTES": "504",
    "VIA ELEVADO": "505",
    "ROTATORIA": "506",
    "ESTACIONAMENTO": "564",
    "VALA": "565",
    "RODO ANEL": "569",
    "TRAVESSA PARTICULAR": "570",
    "ACAMPAMENTO": "645",
    "VIA EXPRESSA": "646",
    "ESTRADA MUNICIPAL": "650",
    "AVENIDA CONTORNO": "651",
    "ENTRE QUADRA": "652",
    "RUA DE LIGACAO": "653",
    "AREA ESPECIAL": "654",
    "DISTRITO": "028"
}

def limpar_texto(texto):
    if not texto:
        return ""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("utf-8")
    return texto.upper().strip()

def extrair_tipo_logradouro(logradouro):
    palavras = logradouro.split()
    if palavras:
        tipo = limpar_texto(palavras[0])
        restante = ' '.join(palavras[1:]).upper() if len(palavras) > 1 else ''
        codigo = CODIGOS_LOGRADOUROS.get(tipo, "000")
        return tipo, restante, codigo
    return '', limpar_texto(logradouro), "000"

def validar_cep(dados):
    logradouro_original = dados.get("logradouro", "")
    tipo, nome_logradouro, codigo_logradouro = extrair_tipo_logradouro(logradouro_original)

    return {
        "bairro": limpar_texto(dados.get("bairro")),
        "cep": dados.get("cep", "").replace("-", ""),
        "complemento": limpar_texto(dados.get("complemento")),
        "ddd": dados.get("ddd"),
        "ibge": dados.get("ibge", "")[:6],
        "cidade": limpar_texto(dados.get("localidade")),
        "tipo_logradouro": codigo_logradouro,
        "nome_logradouro": nome_logradouro,
        "uf": dados.get("uf")
    }
