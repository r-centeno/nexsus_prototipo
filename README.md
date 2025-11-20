# Sistema Integrado de Gestão em Saúde - NEXSUS
## 1. Visão Geral
Esse projeto visa inicialmente, a criação de um sistema de integração automatizado de faturamento SUS, recebendo os dados de atendimento. O sistema fará o processamento das contas para gerar a cobrança pelo serviço prestado. Analisará os dados de fechamento utilizando técnicas de data science e inteligência artificial e apresentará os resultados e insights em um dashboard interativo acessível de forma segura em qualquer dispositivo. O sistema evoluirá progressivamente até se tornar um sistema de gestão completa em saúde, oferecendo soluções inteligentes para clínicas, laboratórios e hospitais públicos e privados. O sistema será desenvolvido em conformidade com as normas da LGPD, garantindo segurança, privacidade e rastreabilidade.

- Processamento de múltiplos formatos (PDF, Excel, TXT)
- Integração com webservices oficiais (CNES, ViaCEP, CADWEB)
- Banco de dados centralizado PostgreSQL
- Análise de dados com Python e IA
- Dashboards interativos
- Total conformidade com LGPD
- Configuração de ambiente híbrido (Python + Static Files)
- Arquitetura multicloud (Supabase e Vercel)

**Stack Tecnológica:**
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Chart.js
- **Backend:** Python 3.9+, Django 4.2 (produção), Flask (desenvolvimento)
- **Banco de Dados:** PostgreSQL 14+
- **Integrações:** CNES, ViaCEP, CADWEB, Firebird
- **Dependências:** PyPDF2, openpyxl, pandas, requests, fdb.

## 2. Arquitetura e Tecnologias
### Back-end e Segurança:
**Framework Principal:**
Django + Django REST Framework (DRF) O Django já vem configurado com proteções embutidas (contra CSRF, XSS, SQL Injection etc.) e, usando o DRF, você conseguirá estruturar APIs RESTful seguras para a comunicação com o front-end.<br>
**Autenticação e Autorização:**
+	autenticação robusta utilizando JSON Web Tokens (JWT) ou OAuth2 para garantir que somente usuários autorizados acessem os dados.
+	sistema de controle de acesso baseado em papéis (RBAC), para definir quais operações cada tipo de usuário pode executar.
**Banco de Dados:**
+ Utilizaremos o PostgreSQL para base produção e SQLite para base desenvolvimento.
+	Conexões via TLS para garantir a confidencialidade em trânsito.
+	Mecanismos de criptografia e backups seguros para proteção dos dados em repouso.
**Integração de IA e Ciência de Dados:**
+	Bibliotecas como Pandas para limpeza e manipulação dos dados.
+	Scikit-learn ou TensorFlow/Keras podem ser aplicados para construir modelos preditivos ou de classificação com base nos dados armazenados.
+	Rotinas periódicas (por exemplo, via cron jobs ou tarefas agendadas com o Celery) para processar os dados, gerar métricas e criar relatórios automáticos.
**Boas Práticas de Segurança Adicionais:**
+	Validação e sanitização completa de todas as entradas no lado do cliente e do servidor.
+	Testes de penetração utilizando ferramentas especializadas para identificar e corrigir vulnerabilidades.
+	Implementação de logs centralizados e monitoramento para detecção precoce de atividades suspeitas.

###Front-end e Dashboard Interativo:
**Framework e Biblioteca:**
+  Tecnologias utilizadas html, css e javascript.<br> 
**Componentes de Visualização:**
+ 	Serão utilizadas bibliotecas de gráficos interativos como Chart.js para exibir relatórios analíticos e dashboards. Esse componente pode oferecer funcionalidades de filtragem, seleção de período e personalização dos gráficos, permitindo que o usuário explore os dados de diferentes ângulos.<br>
**Comunicação com o Back-end:**
+  front-end deve consumir as APIs RESTful do back-end, utilizando chamadas seguras (HTTPS, tokens de autenticação) para manusear e exibir os dados de forma dinâmica.com websockets para atualizações em tempo real nos gráficos.<br>
**Integração de IA e Ciência de Dados:**
+	Pipeline de Dados e Relatórios Analíticos:
+	Extração e Transformação: scripts automatizados que periodicamente extraiam os dados do banco, façam limpeza e transformações necessárias.<br>
**Análise e Modelagem:**
+	Algoritmos de machine learning para identificar padrões, prever tendências ou segmentar dados.
+	Relatórios analíticos que sumarizem resultados, quais podem ser disponibilizados de forma interativa no dashboard e exportáveis para formatos como PDF ou CSV.<br>
**Feedback e Alertas:**
+	Notificações no sistema para alertar os usuários quando determinados indicadores alcançarem valores críticos ou quando novas análises forem geradas.

## 2.1 – Levantamento de Requisitos

### Requisitos Funcionais
- **Importação e Processamento de Dados:**  
  - Módulo para leitura de arquivos PDF  
  - Módulo para leitura de arquivos XLSX, tratamento de duplicidades e sanitização dos dados.  
  - Integração com webservices para obtenção de dados do CNES.
  - Módulo para consulta à API viacep e armazenamento dos dados na tabela Cep.  
  - Módulo para importação de arquivos TXT, carregando dados na tabela Procedimento.
  - Módulo de inserção na tabela Produção, com regras de mapeamento.
  - Processamento automatizado da produção e geração do arquivo de exportação para o SUS.  
  - Módulo para geração de estatísticas financeiras e dashboard interativo.

- **Interface e Segurança:**  
  - Tela de login com autenticação robusta (JWT ou OAuth2).  
  - Tela de recuperação de senha.  
  - Tela CRUD para gerenciamento de todos os registros.  
  - Tela de importação de dados.  
  - Dashboard interativo com gráficos e filtros dinâmicos.

### Requisitos Não Funcionais
- **Segurança:**  
   - Criptografia dos dados sensíveis (em repouso e em trânsito).  
   - Validação e sanitização de todas as entradas.  
   - Logs e auditorias detalhadas (tabela Auditoria).  
   - Conformidade com a LGPD, garantindo transparência e consentimento.
- **Desempenho e Escalabilidade:**  
   - Utilização de PostgreSQL (ou SQLite para desenvolvimento) com otimizações para consultas.
   - Deploy com Docker e pipelines CI/CD para manter a integridade do sistema.
- **Usabilidade:**  
   - Interface intuitiva, responsiva e compatível com dispositivos móveis.
- **Manutenibilidade:**  
   - Estrutura modular com separação clara de responsabilidades entre os módulos.
   - Testes automatizados para garantir a qualidade e segurança.
  
## 3. Fluxo Geral da Aplicação
1.	Acesso e Autenticação: Usuários acessam o dashboard via web e efetuam login. O sistema utiliza JWT ou outro método seguro, garantindo acesso somente a usuários autenticados.
2.	Interação e Visualização: O front-end, usando frameworks modernos, consome as APIs seguras do back-end e exibe um dashboard interativo com gráficos e relatórios, responsivos em qualquer dispositivo.
3.	Análise e Atualização dos Dados: Em paralelo, processos de IA e ciência de dados analisam os dados armazenados, atualizando periodicamente os relatórios e identificando insights relevantes (como tendências, anomalias ou predições).
4.	Feedback e Segurança: Todas as comunicações são realizadas por HTTPS, e os mecanismos de logs e monitoramento garantem a integridade do sistema, permitindo identificar e reagir rapidamente a qualquer incidente.

## 4. Módulos do Sistema
A aplicação ficará organizada em torno de um módulo principal (main) que integrará e disparará as execuções dos demais módulos:
1.	Módulo Main: Responsável por iniciar e orquestrar todos os módulos do sistema. Essa camada gerencia o fluxo de trabalho e a execução sequencial ou paralela dos módulos conforme a demanda.
2.	Módulo 1 – Processamento de PDF para Atendimento:
Ler arquivos em PDF.
3.	Módulo 2 – Processamento de XLSX para Cadastro de Pacientes:
Ler planilhas Excel, identificar duplicidades e completar campos vazios utilizando dados de registros já existentes.
Inserir/atualizar os dados na tabela Paciente.
4.	Módulo 3 – Integração com Webservice do CNES:
Baixar dados do webservice do CNES.
5.	Módulo 4 – Integração com API ViaCEP:
Usar a biblioteca viacep para obter os dados do endereço.
6.	Módulo 5 – Atualização via Webservice CADWEB:
Consultar o webservice CADWEB para validar e corrigir dados ausentes ou incorretos.
7.	Módulo 6 – Cadastro de Estabelecimento:
Permitir que o usuário cadastre manualmente ou confirme os dados do estabelecimento.
8.	Módulo 7 – Cadastro de Usuário:
Tela para criação, edição e exclusão de usuários
9.	Módulo 8 – Auditoria de Acessos:
Capturar e armazenar, em tempo real, informações de acesso dos usuários.
10.	Módulo 9 – Importação de Procedimentos via Arquivo TXT:
Fornecer uma interface para o usuário indicar a localização de um arquivo TXT.
Ler e inserir os dados na tabela Procedimento.
11.	Módulo 10 – Geração de Inserts na Tabela Produção:
Inserir registros na tabela Producao com o mapeamento dos campos conforme regra de negócio.
12.	Módulo 11 – Geração de Estatísticas Financeiras:
Processar os dados armazenados para gerar relatórios e análises financeiras, utilizando técnicas de Data Science e algoritmos de IA para identificar tendências e gerar insights.
13.	Módulo 12 – Dashboard Interativo:
Gerar um dashboard interativo, responsivo e criado com HTML, CSS e JavaScript.
Exibir as estatísticas financeiras, com gráficos dinâmicos (utilizando bibliotecas como Chart.js, D3.js ou Plotly) e filtros para exploração dos dados.

## 5. Telas da Aplicação
O sistema terá as seguintes telas, projetadas para oferecer uma experiência de uso intuitiva e segura:
+	Tela de Login: Acesso seguro com autenticação via JWT ou OAuth2.
+	Tela de Recuperação de Senha: Fluxo para redefinir senha, com validações e envio de e-mail se necessário.
+	Tela CRUD: Para gerenciamento completo de registros (atendimentos, pacientes, profissionais, etc.).
+	Tela Dashboard: Exibição dos relatórios financeiros, gráficos interativos e insights de análise de dados.
+	Tela de Importação de Dados: Interface para seleção de arquivos (PDF, XLSX, TXT) e integração via webservices.

## 6. Considerações Finais
+	Integração Contínua / Deploy: utilização de Docker para containerização, pipelines CI/CD (por exemplo, via GitHub Actions) e deploy em um ambiente Cloud seguro.
+	Testes e Validação: testes automatizados (unitários e integrados) para cada módulo, garantindo a qualidade do código e a segurança contra vulnerabilidades.
+	Evolução do Sistema: Com o MVP implementado, novas funcionalidades (novos dashboards, aprimoramentos dos modelos de IA e Data Science) poderão ser incorporadas, sempre com monitoramento e auditoria para atender novos requisitos legais e de negócio.
    Essa proposta unifica o projeto apresentado anteriormente com os novos requisitos para a gestão de atendimentos médicos, garantindo uma solução robusta, segura e que traz insights valiosos para a tomada de decisões.
    Gostaria de aprofundar algum dos módulos específicos, discutir estratégias para a integração com os webservices ou quem sabe explorar ideias para os modelos preditivos? Posso também detalhar como configurar cada parte da infraestrutura ou como estruturar os testes automatizados para garantir a qualidade e a segurança da aplicação.

## DER INICIAL
````mermaid
erDiagram
    PESSOA {
        int id_pessoa PK
        varchar nome
        char(11) cpf UK
        date dt_nascimento
        char(1) sexo
        varchar raca
        varchar nacionalidade
        char(15) cns
        boolean cns_validado
        timestamp data_validacao_cns
        timestamp data_ultima_consulta_cns
        varchar matricula
        varchar email
        char(2) ddd_telefone
        varchar telefone
    }

    PACIENTE {
        int id_paciente PK
        int id_pessoa FK
    }

    COLABORADOR {
        int id_colaborador PK
        int id_pessoa FK
        int id_funcao FK
    }

    COLABORADOR_PROF_SAUDE {
        int id_prof_saude PK
        int id_colaborador FK
        varchar codigo_cbo
        boolean cbo_validado
        timestamp data_validacao_cbo
        int carga_horaria
        boolean carga_horaria_validada
        timestamp data_validacao_ch
    }

    FUNCAO {
        int id_funcao PK
        varchar nome_funcao
    }

    ENDERECO {
        int id_endereco PK
        int id_pessoa FK
        char(8) cep
        boolean cep_validado
        timestamp data_validacao_cep
        varchar tipo_logradouro
        varchar nome_logradouro
        varchar bairro
        varchar cidade
        char(2) uf
        varchar numero
        varchar complemento
    }

    ATENDIMENTO {
        int id_atendimento PK
        int id_paciente FK
        int id_procedimento FK
        date data_proc
        varchar mnem_proc

        timestamp criado_em
    }

    PRODUCAO {
        int id_producao PK
        varchar prd_uid
        date prd_cmp
        char(15) prd_cnsmed
        varchar prd_cbo
        varchar prd_flh
        int prd_seq
        varchar prd_pa
        char(15) prd_cnspac
        varchar prd_nmpac
        date prd_dtnasc
        char(1) prd_sexo
        varchar prd_ibge
        date prd_dtaten
        varchar prd_cid
        int prd_idade
        int prd_qt_p
        varchar prd_caten
        varchar prd_naut
        varchar prd_org
        varchar prd_mvm
        boolean prd_flpa
        boolean prd_flcbo
        boolean prd_flca
        boolean prd_flida
        boolean prd_flqt
        boolean prd_fler
        boolean prd_flmun
        boolean prd_flcid
        varchar prd_raca
        varchar prd_servico
        varchar prd_classificacao
        varchar prd_equipe
        varchar prd_etnia
        varchar prd_nac
        int prd_advqt
        varchar prd_cnpj
        varchar prd_eqp_area
        int prd_eqp_seq
        varchar prd_lograd_pcnte
        char(8) prd_cep_pcnte
        varchar prd_end_pcnte
        varchar prd_compl_pcnte
        varchar prd_num_pcnte
        varchar prd_bairro_pcnte
        char(2) prd_ddtel_pcnte
        varchar prd_tel_pcnte
        varchar prd_email_pcnte
        varchar prd_ine
        boolean chk_sum
        char(11) prd_cpf_pcnte
        varchar prd_situacao_rua
        varchar prd_apres
        timestamp processado_em
        boolean validado_via_api
        timestamp data_validacao_api
    }

    USUARIOS {
        int id_usuario PK
        int id_pessoa FK
        char senha_hash
        bool ativo
        timestamptz criado_em
        timestamptz ultima_atualizacao
    }

    PAPEIS {
        int id_papel PK
        varchar nome UK
        text descricao
        timestamptz criado_em
    }

    PERMISSOES {
        int id_permissao PK
        varchar nome UK
        text descricao
        timestamptz criado_em
    }

    PAPEIS_PERMISSOES {
        int id_papel FK
        int id_permissao FK
    }

    USUARIOS_PAPEIS {
        int id_usuario FK
        int id_papel FK
        timestamptz atribuido_em
    }

    AUDITORIA_ACESSOS {
        int id_auditoria PK
        int id_usuario FK
        varchar ip
        varchar cidade
        varchar pais
        varchar acao
        timestamptz data_hora
        text user_agent
    }

    SESSOES {
        int id_sessao PK
        int id_usuario FK
        text token_jwt UK
        timestamptz criado_em
        timestamptz expira_em
        bool revogado
    }

    CODIGOS_2FA {
        int id_codigo PK
        int id_usuario FK
        char codigo_6d
        timestamptz criado_em
        timestamptz expira_em
        bool usado
        varchar tipo
    }

    HISTORICO_CNS {
        int id_historico PK
        int id_pessoa FK
        char(15) cns_anterior
        timestamp data_consulta
        boolean valido
        varchar resposta_api
        text observacoes
    }

    HISTORICO_CEP {
        int id_historico PK
        int id_endereco FK
        char(8) cep_anterior
        timestamp data_consulta
        boolean valido
        varchar resposta_api
        text observacoes
    }

    HISTORICO_CBO {
        int id_historico PK
        int id_prof_saude FK
        varchar cbo_anterior
        timestamp data_consulta
        boolean valido
        varchar resposta_api
        text observacoes
    }

    PROCEDIMENTO{
        int id_procedimento PK
        varchar cod_proc
        varchar proc
        decimal vlr_proc
    }

        ORGANIZACAO{
        int id_organizacao PK
        int id_procedimento FK
        varchar codigo
        varchar descricao        
    }
        
    ATENDIMENTO ||--o{ PROCEDIMENTO : "possui"
    PESSOA ||--o{ PACIENTE : "pode ser"
    PESSOA ||--o{ COLABORADOR : "pode ser"
    PESSOA ||--o{ ENDERECO : "possui"
    PESSOA ||--o{ USUARIOS : "pode ter acesso"
    PESSOA ||--o{ HISTORICO_CNS : "possui histórico"
    PACIENTE ||--o{ ATENDIMENTO : "possui"
    COLABORADOR }o--|| FUNCAO : "tem"
    COLABORADOR ||--o{ COLABORADOR_PROF_SAUDE : "pode ser"
    ENDERECO ||--o{ HISTORICO_CEP : "possui histórico"
    COLABORADOR_PROF_SAUDE ||--o{ HISTORICO_CBO : "possui histórico"
    USUARIOS ||--o{ USUARIOS_PAPEIS : possui
    USUARIOS ||--o{ AUDITORIA_ACESSOS : registra
    USUARIOS ||--o{ SESSOES : inicia
    USUARIOS ||--o{ CODIGOS_2FA : recebe
    PAPEIS ||--o{ USUARIOS_PAPEIS : contem
    PAPEIS ||--o{ PAPEIS_PERMISSOES : contem
    PERMISSOES ||--o{ PAPEIS_PERMISSOES : possui
````




