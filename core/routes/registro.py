from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from core.models import Pessoa, Endereco, Atendimento, Paciente, Procedimento
from core.utils.validador_cep import validar_cep
from core.utils.extensions import db
from datetime import datetime
import requests

registro_bp = Blueprint("registro", __name__)


@registro_bp.route("/api/registros", methods=["GET"])
def listar_registros():
    pessoas = Pessoa.query.all()
    resultado = []
    for pessoa in pessoas:
        endereco = pessoa.endereco[0] if pessoa.endereco else None
        atendimento = pessoa.atendimentos[-1] if pessoa.atendimentos else None
        procedimento = atendimento.procedimento if atendimento else None

        registro = {
            "id_pessoa": pessoa.id_pessoa,
            "nome": pessoa.nome,
            "cpf": pessoa.cpf,
            "sexo": pessoa.sexo,
            "raca": pessoa.raca,
            "nacionalidade": pessoa.nacionalidade,
            "cns": pessoa.cns,
            "dt_nascimento": pessoa.dt_nascimento.strftime("%Y-%m-%d") if pessoa.dt_nascimento else "",
            "ddd": pessoa.ddd,
            "telefone": pessoa.telefone,
            "cep": endereco.cep if endereco else "",
            "tipo_logradouro": endereco.tipo_logradouro if endereco else "",
            "nome_logradouro": endereco.nome_logradouro if endereco else "",
            "numero": endereco.numero if endereco else "",
            "complemento": endereco.complemento if endereco else "",
            "bairro": endereco.bairro if endereco else "",
            "cidade": endereco.cidade if endereco else "",
            "uf": endereco.uf if endereco else "",
            "ibge": endereco.ibge if endereco else "",
            "data_proc": atendimento.data_procedimento.strftime("%Y-%m-%d") if atendimento else "",
            "codigo_procedimento": procedimento.cod_procedimento if procedimento else "",
            "nome_procedimento": procedimento.nome_procedimento if procedimento else "",
            "quantidade": atendimento.quantidade if atendimento else "",
            "cid": atendimento.cid if atendimento else "",
            "carater_atendimento": atendimento.carater_atendimento if atendimento else "",
            "vlr_procedimento": str(procedimento.vlr_procedimento) if procedimento else "0.00",
        }
        resultado.append(registro)
    return jsonify(resultado)


@registro_bp.route("/api/registros", methods=["POST"])
@cross_origin()
def criar_registro():
    dados = request.get_json()
    
    try:
        cod_proc = dados.get("codigo_procedimento")
        procedimento = Procedimento.query.filter_by(
            cod_procedimento=cod_proc).first()
        if not procedimento:
            return jsonify({"erro": "Procedimento não encontrado"}), 400

        dt_nascimento = datetime.strptime(
            dados.get("dt_nascimento"), "%Y-%m-%d").date()
        nova_pessoa = Pessoa(
            nome=dados.get("nome"),
            cpf=dados.get("cpf"),
            dt_nascimento=dt_nascimento,
            sexo=dados.get("sexo"),
            raca=dados.get("raca"),
            cns=dados.get("cns"),
            ddd=dados.get("ddd"),
            telefone=dados.get("telefone"),
            nacionalidade=dados.get("nacionalidade")
        )
        db.session.add(nova_pessoa)
        db.session.flush()

        novo_paciente = Paciente(id_pessoa=nova_pessoa.id_pessoa)
        db.session.add(novo_paciente)
        db.session.flush()

        data_proc = datetime.strptime(
            dados.get("data_proc"), "%Y-%m-%d").date()
        novo_atendimento = Atendimento(
            id_pessoa=nova_pessoa.id_pessoa,
            id_paciente=novo_paciente.id_paciente,
            id_procedimento=procedimento.id_procedimento,
            data_procedimento=data_proc,
            quantidade=dados.get("quantidade"),
            cid=dados.get("cid"),
            vlr_procedimento=procedimento.vlr_procedimento,
            carater_atendimento=dados.get("carater_atendimento")
        )
        
        db.session.add(novo_atendimento)
        db.session.flush()

        novo_endereco = Endereco(
            id_pessoa=nova_pessoa.id_pessoa,
            cep=dados.get("cep"),
            tipo_logradouro=dados.get("tipo_logradouro"),
            nome_logradouro=dados.get("nome_logradouro"),
            numero=dados.get("numero"),
            complemento=dados.get("complemento"),
            bairro=dados.get("bairro"),
            cidade=dados.get("cidade"),
            uf=dados.get("uf"),
            ibge=dados.get("ibge")
        )
        db.session.add(novo_endereco)
        db.session.flush()

        db.session.commit()
        return jsonify({"mensagem": "Registro criado com sucesso!"}), 201

    except Exception as e:
        db.session.rollback()
        print("ERRO AO SALVAR:", e)
        return jsonify({"erro": "Falha ao salvar registro"}), 500


@registro_bp.route("/api/registros/<int:id>", methods=["DELETE"])
def excluir_registro(id):
    pessoa = Pessoa.query.get_or_404(id)
    db.session.delete(pessoa)
    db.session.commit()
    return jsonify({"mensagem": "Registro excluído com sucesso!"})

@registro_bp.route("/api/registros/<int:id>", methods=["PUT"])
def atualizar_registro(id):
    dados = request.json
    pessoa = Pessoa.query.get_or_404(id)

    # Atualiza dados da Pessoa
    pessoa.nome = dados.get("nome", pessoa.nome)
    pessoa.cpf = dados.get("cpf", pessoa.cpf)
    pessoa.dt_nascimento = datetime.strptime(dados.get(
        "dt_nascimento"), "%Y-%m-%d").date() if dados.get("dt_nascimento") else pessoa.dt_nascimento
    pessoa.sexo = dados.get("sexo", pessoa.sexo)
    pessoa.cns = dados.get("cns", pessoa.cns)
    pessoa.ddd = dados.get("ddd", pessoa.ddd)
    pessoa.telefone = dados.get("telefone", pessoa.telefone)
    pessoa.raca = dados.get("raca", pessoa.raca)
    pessoa.nacionalidade = dados.get("nacionalidade", pessoa.nacionalidade)

    # Atualiza Endereço
    endereco = pessoa.endereco[0] if pessoa.endereco else None
    if endereco:
        endereco.cep = dados.get("cep", endereco.cep)
        endereco.tipo_logradouro = dados.get(
            "tipo_logradouro", endereco.tipo_logradouro)
        endereco.nome_logradouro = dados.get(
            "nome_logradouro", endereco.nome_logradouro)
        endereco.numero = dados.get("numero", endereco.numero)
        endereco.complemento = dados.get("complemento", endereco.complemento)
        endereco.bairro = dados.get("bairro", endereco.bairro)
        endereco.cidade = dados.get("cidade", endereco.cidade)
        endereco.uf = dados.get("uf", endereco.uf)
        endereco.ibge = dados.get("ibge", endereco.ibge)

    # Atualiza Atendimento
    atendimento = pessoa.atendimentos[-1] if pessoa.atendimentos else None
    if atendimento:
        atendimento.data_procedimento = datetime.strptime(dados.get(
            "data_proc"), "%Y-%m-%d").date() if dados.get("data_proc") else atendimento.data_procedimento
        atendimento.quantidade = dados.get(
            "quantidade", atendimento.quantidade)
        atendimento.cid = dados.get("cid", atendimento.cid)
        atendimento.carater_atendimento = dados.get(
            "carater_atendimento", atendimento.carater_atendimento)

        # Atualiza Procedimento se necessário
        cod_proc = dados.get("codigo_procedimento")
        if cod_proc:
            procedimento = Procedimento.query.filter_by(
                cod_procedimento=cod_proc).first()
            if procedimento:
                atendimento.id_procedimento = procedimento.id_procedimento
                atendimento.vlr_procedimento = procedimento.vlr_procedimento

    db.session.commit()
    return jsonify({"mensagem": "Registro atualizado com sucesso!"})

@registro_bp.route("/api/cep/<cep>", methods=["GET"])
def consultar_cep(cep):
    resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    if resposta.status_code == 200:
        dados_tratados = validar_cep(resposta.json())
        return jsonify(dados_tratados)
    return jsonify({"erro": "CEP não encontrado"}), 404


@registro_bp.route("/api/procedimento/<codigo>", methods=["GET"])
def obter_nome_procedimento(codigo):
    procedimento = Procedimento.query.filter_by(
        cod_procedimento=codigo).first()
    if procedimento:
        return jsonify({"nome_procedimento": procedimento.nome_procedimento})
    return jsonify({"erro": "Procedimento não encontrado"}), 404


@registro_bp.route("/api/importar", methods=["POST"])
def importar_registros():
    from werkzeug.utils import secure_filename
    import pandas as pd
    import os
    import csv
    import io
    from flask import Response

    arquivo = request.files.get("arquivo")
    if not arquivo:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    nome_seguro = secure_filename(arquivo.filename)
    extensao = os.path.splitext(nome_seguro)[1].lower()
    if extensao not in [".xlsx", ".xls"]:
        return jsonify({"erro": "Formato de arquivo inválido"}), 400

    try:
        df = pd.read_excel(arquivo, dtype={"cod_procedimento": str})
        df.columns = [col.strip().lower() for col in df.columns]
    except Exception as e:
        return jsonify({"erro": f"Erro ao ler arquivo: {str(e)}"}), 500

    erros = []
    total_inseridos = 0

    for i, linha in df.iterrows():
        try:
            nome = str(linha.get("nome")).strip()
            cpf = str(linha.get("cpf")).strip()
            cns = str(linha.get("cns")).strip()
            dt_nascimento_raw = str(linha.get("dt_nascimento")).strip()

            if not (nome and cpf and cns and dt_nascimento_raw):
                raise ValueError("Campos obrigatórios ausentes")

            dt_nascimento = datetime.strptime(dt_nascimento_raw, "%Y%m%d").date()

            pessoa = Pessoa.query.filter_by(
                nome=nome, cpf=cpf, cns=cns, dt_nascimento=dt_nascimento
            ).first()

            sexo = str(linha.get("sexo")).strip()
            raca = str(linha.get("raca")).strip().zfill(2)
            nacionalidade = str(linha.get("nacionalidade")).strip()
            ddd = str(linha.get("ddd")).strip()
            telefone = str(linha.get("telefone")).strip()

            cep = str(linha.get("cep")).strip()
            tipo_logradouro = str(linha.get("tipo_logradouro")).strip().zfill(3)
            nome_logradouro = str(linha.get("nome_logradouro")).strip()
            numero = str(linha.get("numero")).strip()
            complemento_raw = linha.get("complemento")
            complemento = "" if pd.isna(complemento_raw) else str(complemento_raw).strip()
            bairro = str(linha.get("bairro")).strip()
            cidade = str(linha.get("cidade")).strip()
            uf = str(linha.get("uf")).strip()
            ibge = str(linha.get("ibge")).strip()

            if not pessoa:
                pessoa = Pessoa(
                    nome=nome,
                    cpf=cpf,
                    cns=cns,
                    dt_nascimento=dt_nascimento,
                    sexo=sexo,
                    raca=raca,
                    nacionalidade=nacionalidade,
                    ddd=ddd,
                    telefone=telefone
                )
                db.session.add(pessoa)
                db.session.flush()

                paciente = Paciente(id_pessoa=pessoa.id_pessoa)
                db.session.add(paciente)
                db.session.flush()

                endereco = Endereco(
                    id_pessoa=pessoa.id_pessoa,
                    cep=cep,
                    tipo_logradouro=tipo_logradouro,
                    nome_logradouro=nome_logradouro,
                    numero=numero,
                    complemento=complemento,
                    bairro=bairro,
                    cidade=cidade,
                    uf=uf,
                    ibge=ibge
                )
                db.session.add(endereco)
                db.session.flush()
            else:
                paciente = Paciente.query.filter_by(id_pessoa=pessoa.id_pessoa).first()
                if not paciente:
                    paciente = Paciente(id_pessoa=pessoa.id_pessoa)
                    db.session.add(paciente)
                    db.session.flush()

            cod_proc = str(linha.get("cod_procedimento")).strip()
            print("Buscando procedimento:", repr(cod_proc))
            procedimento = Procedimento.query.filter_by(cod_procedimento=cod_proc).first()
            if not procedimento:
                raise ValueError("Procedimento não encontrado")

            data_proc_raw = linha.get("data_procedimento")
            if not data_proc_raw or pd.isna(data_proc_raw):
                raise ValueError("Data do procedimento ausente ou inválida")
            data_proc = datetime.strptime(str(data_proc_raw).strip(), "%Y%m%d").date()

            quantidade = int(linha.get("quantidade", 1))
            cid = str(linha.get("cid")).strip()
            carater_atendimento = str(linha.get("carater_atendimento")).strip().zfill(2)

            atendimento = Atendimento(
                id_pessoa=pessoa.id_pessoa,
                id_paciente=paciente.id_paciente,
                id_procedimento=procedimento.id_procedimento,
                data_procedimento=data_proc,
                quantidade=quantidade,
                cid=cid,
                carater_atendimento=carater_atendimento,
                vlr_procedimento=procedimento.vlr_procedimento
            )
            db.session.add(atendimento)
            db.session.flush()

            total_inseridos += 1

        except Exception as e:
            erros.append({
                "linha": i + 2,
                "nome": linha.get("nome"),
                "cpf": linha.get("cpf"),
                "cns": linha.get("cns"),
                "dt_nascimento": linha.get("dt_nascimento"),
                "erro": str(e)
            })
            db.session.rollback()
            continue

    db.session.commit()

    if erros:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["linha", "nome", "cpf", "cns", "dt_nascimento", "erro"])
        writer.writeheader()
        writer.writerows(erros)
        csv_data = output.getvalue()
        return Response(
            csv_data,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=erros_importacao.csv"}
        )

    return jsonify({
        "mensagem": f"{total_inseridos} atendimentos importados com sucesso.",
        "erros": []
    }), 200

