import os
import sys
import uuid

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models.course import Course, Module, Unit, Topic
from app.infrastructure.db.models.content import Question, Flashcard, Example
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.gamification import QuestionAttempt

def seed_db():
    db = SessionLocal()
    
    print("Iniciando limpeza do banco de dados...")
    db.query(QuestionAttempt).delete()
    db.query(Flashcard).delete()
    db.query(Question).delete()
    db.query(Example).delete()
    db.query(Topic).delete()
    db.query(Unit).delete()
    db.query(Module).delete()
    db.query(Course).delete()
    db.commit()
    print("Banco de dados limpo com sucesso!")

    # 0. Usuário Mock (necessário para a gamificação)
    mock_user_id = uuid.uuid5(uuid.NAMESPACE_DNS, "mock_student_user")
    user = db.query(User).filter(User.id == mock_user_id).first()
    if not user:
        user = User(id=mock_user_id, email="aluno@imparh.com", password_hash="mock")
        db.add(user)
        db.commit()

    # 1. Curso
    course = Course(
        name="Português para Concursos", 
        description="O curso definitivo de língua portuguesa focado na banca IMPARH, com teoria e questões."
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    # 2. Módulo
    module = Module(
        course_id=course.id, 
        title="Módulo 1: Morfologia", 
        order_index=1
    )
    db.add(module)
    db.commit()
    db.refresh(module)

    # 3. Unidades
    unit_variaveis = Unit(
        module_id=module.id, 
        title="Unidade 1: Classes Variáveis", 
        order_index=1
    )
    unit_invariaveis = Unit(
        module_id=module.id, 
        title="Unidade 2: Classes Invariáveis", 
        order_index=2
    )
    db.add_all([unit_variaveis, unit_invariaveis])
    db.commit()
    db.refresh(unit_variaveis)
    db.refresh(unit_invariaveis)

    # ==================== TOPICS & CONTENT ====================

    # --- 1.1 SUBSTANTIVO ---
    substantivo_theory = """
# O que é o Substantivo?
O substantivo é a classe de palavras variável responsável por nomear tudo o que existe: seres, objetos, lugares, sentimentos, ações transformadas em nome, estados e conceitos abstratos. É o núcleo do sujeito e de diversos complementos verbais, sendo a base em torno da qual orbitam artigos, adjetivos, pronomes e numerais.

## Classificação do Substantivo

| Tipo | Definição | Exemplos |
|---|---|---|
| **Comum** | Nomeia seres de uma mesma espécie de forma genérica. | cidade, cachorro, professor |
| **Próprio** | Nomeia um ser específico e é grafado com inicial maiúscula. | Curitiba, Rex, Marcela |
| **Concreto** | Nomeia seres de existência independente (real ou imaginária). | árvore, fantasma, mesa |
| **Abstrato** | Nomeia sentimentos, ações, qualidades ou estados dependentes de um ser. | alegria, beleza, coragem |
| **Coletivo** | Nomeia um conjunto de seres da mesma espécie (mesmo no singular). | cardume, alcateia, plateia |
| **Simples** | Formado por um único radical. | flor, tempo, pé |
| **Composto** | Formado por mais de um radical. | girassol, guarda-chuva, passatempo |
| **Primitivo** | Não se origina de outra palavra. | pedra, livro, terra |
| **Derivado** | Origina-se de outra palavra através de afixos. | pedreiro, livraria, terreiro |

## Flexões do Substantivo
O substantivo flexiona-se em:
* **Gênero:** masculino e feminino (Ex: *menino/menina*, *ator/atriz*).
* **Número:** singular e plural (Ex: *flor/flores*, *cidadão/cidadãos*).
* **Grau:** normal, aumentativo (sintético: *casarão*; analítico: *casa muito grande*) e diminutivo (sintético: *casinha*; analítico: *casa pequena*).

> 💡 **Fique Atento:**
> Não confunda substantivo abstrato com adjetivo: “beleza” é substantivo (nomeia a qualidade) e necessita de um ser para existir, enquanto “belo” é adjetivo (atribui a qualidade a um ser).
"""
    t_substantivo = Topic(
        unit_id=unit_variaveis.id,
        title="1.1 Substantivo",
        difficulty=2,
        order_index=1,
        introduction="Aprenda a classificar e flexionar os substantivos, o núcleo da morfologia nominal.",
        theory_markdown=substantivo_theory
    )
    db.add(t_substantivo)
    db.commit()
    db.refresh(t_substantivo)

    # Questões de Substantivo
    q_sub1 = Question(
        topic_id=t_substantivo.id,
        statement="Em 'A alcateia perseguiu a presa por horas', a palavra destacada ('alcateia') classifica-se como:",
        option_a="substantivo comum concreto",
        option_b="substantivo coletivo",
        option_c="substantivo abstrato",
        option_d="substantivo próprio",
        correct_option="B",
        justification_correct="A palavra 'alcateia' designa um conjunto de lobos, sendo, portanto, um substantivo coletivo.",
        justification_incorrect="Esta palavra não representa um substantivo abstrato, próprio ou puramente concreto individual; ela é classificada como coletiva por designar um grupo de seres da mesma espécie.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Substantivos",
        board="IMPARH"
    )
    q_sub2 = Question(
        topic_id=t_substantivo.id,
        statement="Assinale a alternativa em que todas as palavras são substantivos abstratos:",
        option_a="mesa, cadeira, porta",
        option_b="amor, saudade, coragem",
        option_c="São Paulo, Ana, Brasil",
        option_d="flor, sol, mar",
        correct_option="B",
        justification_correct="Amor, saudade e coragem são substantivos abstratos pois nomeiam sentimentos e qualidades que só existem em função de um ser.",
        justification_incorrect="Nas outras opções temos substantivos concretos (mesa, cadeira, flor, sol, mar) e próprios (São Paulo, Ana, Brasil).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Substantivos",
        board="IMPARH"
    )
    q_sub3 = Question(
        topic_id=t_substantivo.id,
        statement="O substantivo 'girassol' é classificado, quanto à estrutura, como:",
        option_a="primitivo",
        option_b="derivado",
        option_c="simples",
        option_d="composto",
        correct_option="D",
        justification_correct="O substantivo 'girassol' é formado por composição por justaposição de dois radicais (gira + sol), sendo, portanto, composto.",
        justification_incorrect="Não é simples nem primitivo ou derivado; a presença de múltiplos radicais o torna composto.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Substantivos",
        board="IMPARH"
    )
    q_sub4 = Question(
        topic_id=t_substantivo.id,
        statement="Em 'O casarão da fazenda foi reformado', o grau do substantivo destacado é:",
        option_a="diminutivo sintético",
        option_b="aumentativo sintético",
        option_c="aumentativo analítico",
        option_d="diminutivo analítico",
        correct_option="B",
        justification_correct="O sufixo '-arão' indica grau aumentativo formado de forma sintética (dentro da própria palavra).",
        justification_incorrect="O aumentativo analítico exigiria um adjetivo (ex: casa grande). Não se trata de diminutivo.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Substantivos",
        board="IMPARH"
    )
    q_sub5 = Question(
        topic_id=t_substantivo.id,
        statement="Qual par apresenta um substantivo primitivo seguido de seu derivado?",
        option_a="flor — floreira",
        option_b="casa — casarão",
        option_c="livro — livraria e livreiro",
        option_d="mesa — mesinha",
        correct_option="C",
        justification_correct="'Livro' é primitivo e 'livraria'/'livreiro' derivam diretamente dele por acréscimo de sufixos de derivação.",
        justification_incorrect="Os outros pares representam flexões de grau (aumentativo/diminutivo) e não puramente derivação de novas palavras.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Substantivos",
        board="IMPARH"
    )
    db.add_all([q_sub1, q_sub2, q_sub3, q_sub4, q_sub5])
    db.commit()

    # Flashcards Substantivo
    fc_sub1 = Flashcard(topic_id=t_substantivo.id, front="Qual a definição de substantivo próprio?", back="Nomeia um ser específico de forma individualizada e é sempre grafado com inicial maiúscula (Ex: Curitiba, Rex, Marcela).")
    fc_sub2 = Flashcard(topic_id=t_substantivo.id, front="O que diferencia um substantivo concreto de um abstrato?", back="O concreto designa seres com existência independente (real ou imaginária, ex: fada, mesa). O abstrato designa ações, sentimentos ou qualidades que dependem de outro ser (ex: alegria, beleza, coragem).")
    fc_sub3 = Flashcard(topic_id=t_substantivo.id, front="Como se formam os graus aumentativo/diminutivo de forma analítica?", back="Por meio do acréscimo de um adjetivo que indica tamanho. Ex: casa muito grande, casa pequena.")
    db.add_all([fc_sub1, fc_sub2, fc_sub3])
    db.commit()


    # --- 1.2 ARTIGO ---
    artigo_theory = """
# O que é o Artigo?
O artigo é a palavra variável que antecede o substantivo para determiná-lo de modo preciso (definido) ou indefinido (indefinido). A escolha do artigo carrega importante valor semântico e estilístico na estruturação das frases.

## Classificação do Artigo

| Tipo | Definição | Exemplos |
|---|---|---|
| **Definido** | Indica que o substantivo é conhecido, específico ou já mencionado. | o, a, os, as |
| **Indefinido** | Indica que o substantivo é genérico, não individualizado ou não identificado antes. | um, uma, uns, umas |

## Flexões e Combinações
O artigo flexiona em gênero (masculino/feminino) e número (singular/plural). 
Ele também pode se contrair ou combinar com preposições:
* **Combinação (sem perda de fonema):** a + o = *ao*; a + os = *aos*.
* **Contração (com perda de fonema):** de + o = *do*; em + a = *na*; por + o = *pelo*.

> 💡 **Fique Atento:**
> A ausência completa de artigo antes de um substantivo costuma indicar generalização máxima: *“Água é essencial à vida”* (água de forma geral). 
> Além disso, o artigo indefinido pode assumir um tom generalizante: *“Um professor deve ter paciência”* (significa qualquer professor).
"""
    t_artigo = Topic(
        unit_id=unit_variaveis.id,
        title="1.2 Artigo",
        difficulty=1,
        order_index=2,
        introduction="Aprenda a aplicar artigos definidos e indefinidos e identificar suas combinações e contrações.",
        theory_markdown=artigo_theory
    )
    db.add(t_artigo)
    db.commit()
    db.refresh(t_artigo)

    # Questões de Artigo
    q_art1 = Question(
        topic_id=t_artigo.id,
        statement="Em 'Uma solução simples resolveu o problema', o artigo destacado ('Uma') indica:",
        option_a="um ser específico e já conhecido",
        option_b="um ser genérico, não identificado antes",
        option_c="plural definido",
        option_d="contração de preposição",
        correct_option="B",
        justification_correct="'Uma' é um artigo indefinido e serve para indicar um ser de forma vaga e não identificada anteriormente.",
        justification_incorrect="Artigos definidos especificam seres conhecidos. Artigos não indicam contração solos.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Artigos",
        board="IMPARH"
    )
    q_art2 = Question(
        topic_id=t_artigo.id,
        statement="A palavra 'do' em 'O som do mar acalma' resulta da combinação de:",
        option_a="de + o",
        option_b="de + a",
        option_c="em + o",
        option_d="a + o",
        correct_option="A",
        justification_correct="A palavra 'do' é uma contração da preposição 'de' com o artigo definido masculino singular 'o'.",
        justification_incorrect="'Do' vem de 'de + o', e não das preposições 'em' ou 'a'.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Artigos",
        board="IMPARH"
    )
    q_art3 = Question(
        topic_id=t_artigo.id,
        statement="Assinale a frase em que NÃO há artigo:",
        option_a="A vida é curta.",
        option_b="Comprei um presente.",
        option_c="Ele estudou os capítulos.",
        option_d="Preciso de coragem para recomeçar.",
        correct_option="D",
        justification_correct="Em 'de coragem', temos apenas a preposição 'de' ligada ao substantivo 'coragem', sem artigo acompanhando.",
        justification_incorrect="Nas demais opções temos os artigos definidos 'A' e 'os', e o artigo indefinido 'um'.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Artigos",
        board="IMPARH"
    )
    q_art4 = Question(
        topic_id=t_artigo.id,
        statement="Em 'Os professores entregaram as notas', os artigos concordam em:",
        option_a="apenas gênero",
        option_b="apenas número",
        option_c="gênero e número com os substantivos",
        option_d="tempo verbal",
        correct_option="C",
        justification_correct="Os artigos concordam sempre em gênero e número com os substantivos que determinam ('os' masculino plural com 'professores'; 'as' feminino plural com 'notas').",
        justification_incorrect="Artigos não concordam com tempos verbais nem de forma parcial (apenas em gênero ou número).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Artigos",
        board="IMPARH"
    )
    q_art5 = Question(
        topic_id=t_artigo.id,
        statement="Qual alternativa contém um artigo indefinido no plural?",
        option_a="as flores",
        option_b="uns cadernos",
        option_c="o carro",
        option_d="à tarde",
        correct_option="B",
        justification_correct="'Uns' é o artigo indefinido masculino plural.",
        justification_incorrect="'As' e 'o' são definidos, e 'à' é crase (preposição a + artigo a).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Artigos",
        board="IMPARH"
    )
    db.add_all([q_art1, q_art2, q_art3, q_art4, q_art5])
    db.commit()

    # Flashcards Artigo
    fc_art1 = Flashcard(topic_id=t_artigo.id, front="Quais são os artigos definidos?", back="o, a, os, as. Eles determinam o substantivo de forma precisa e individualizada.")
    fc_art2 = Flashcard(topic_id=t_artigo.id, front="Qual a diferença entre combinação e contração com preposição?", back="Combinação ocorre sem perda de fonemas (a + o = ao). Contração ocorre com perda de fonemas (de + o = do; em + a = na).")
    fc_art3 = Flashcard(topic_id=t_artigo.id, front="O que a ausência de artigo antes de um substantivo costuma indicar?", back="Generalização máxima. Ex: 'Água é essencial à vida' (refere-se à água em geral, não a uma água específica).")
    db.add_all([fc_art1, fc_art2, fc_art3])
    db.commit()


    # --- 1.3 ADJETIVO ---
    adjetivo_theory = """
# O que é o Adjetivo?
O adjetivo é a classe de palavras variável que atribui uma característica ao substantivo (qualidade, defeito, estado, aparência, origem ou condição). Desempenha funções sintáticas importantes como adjunto adnominal ou predicativo.

## Classificação do Adjetivo

| Tipo | Definição | Exemplos |
|---|---|---|
| **Simples** | Formado por um único radical. | azul, feliz, grande |
| **Composto** | Formado por mais de um radical. | azul-marinho, luso-brasileiro |
| **Primitivo** | Não deriva de outra palavra da língua. | belo, triste |
| **Derivado** | Formado a partir de outra palavra. | amoroso (de amor), infeliz (de feliz) |
| **Pátrio (Gentílico)** | Indica a nacionalidade ou local de origem. | brasileiro, paranaense, carioca |
| **Locução Adjetiva** | Expressão equivalente a um adjetivo (preposição + substantivo). | de ferro (= férreo), de mãe (= materno) |

## Flexão de Grau do Adjetivo
* **Comparativo:**
  - Igualdade (*tão... quanto*)
  - Superioridade (*mais... que*)
  - Inferioridade (*menos... que*)
* **Superlativo:**
  - Absoluto (Analítico: *muito alto*; Sintético: *altíssimo*)
  - Relativo (Superioridade: *o mais alto*; Inferioridade: *o menos alto*)

> 💡 **Fique Atento:**
> As locuções adjetivas possuem papel idêntico ao de um adjetivo simples: *“dor de cabeça”* equivale a *“dor cefálica”*.
"""
    t_adjetivo = Topic(
        unit_id=unit_variaveis.id,
        title="1.3 Adjetivo",
        difficulty=2,
        order_index=3,
        introduction="Domine as características qualificadoras do adjetivo, suas locuções e flexões de grau.",
        theory_markdown=adjetivo_theory
    )
    db.add(t_adjetivo)
    db.commit()
    db.refresh(t_adjetivo)

    # Questões de Adjetivo
    q_adj1 = Question(
        topic_id=t_adjetivo.id,
        statement="Em 'Ela é menos ansiosa que o colega', o grau do adjetivo destacado é:",
        option_a="comparativo de igualdade",
        option_b="comparativo de inferioridade",
        option_c="superlativo absoluto",
        option_d="superlativo relativo",
        correct_option="B",
        justification_correct="A estrutura 'menos... que' constitui o grau comparativo de inferioridade.",
        justification_incorrect="Igualdade seria 'tão... quanto' e superioridade 'mais... que'.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Adjetivos",
        board="IMPARH"
    )
    q_adj2 = Question(
        topic_id=t_adjetivo.id,
        statement="Assinale a locução adjetiva equivalente a 'paternal':",
        option_a="de pai",
        option_b="de mãe",
        option_c="de ferro",
        option_d="de vidro",
        correct_option="A",
        justification_correct="'De pai' é a locução adjetiva que corresponde ao adjetivo 'paternal'.",
        justification_incorrect="'De mãe' equivale a materno, 'de ferro' a férreo e 'de vidro' a vítreo.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Adjetivos",
        board="IMPARH"
    )
    q_adj3 = Question(
        topic_id=t_adjetivo.id,
        statement="O adjetivo em 'crianças felicíssimas correram pelo parque' está no grau:",
        option_a="comparativo de superioridade",
        option_b="superlativo relativo",
        option_c="superlativo absoluto sintético",
        option_d="superlativo absoluto analítico",
        correct_option="C",
        justification_correct="O sufixo '-íssimo' flexiona o adjetivo no grau superlativo absoluto sintético.",
        justification_incorrect="Se fosse analítico, haveria um advérbio de intensidade (ex: muito felizes).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Adjetivos",
        board="IMPARH"
    )
    q_adj4 = Question(
        topic_id=t_adjetivo.id,
        statement="Qual adjetivo abaixo é classificado como pátrio (gentílico)?",
        option_a="gentil",
        option_b="carioca",
        option_c="estudioso",
        option_d="azul-claro",
        correct_option="B",
        justification_correct="'Carioca' indica origem natural (quem nasce na cidade do Rio de Janeiro), sendo um adjetivo pátrio.",
        justification_incorrect="Os outros representam qualidades comuns, estados ou cores.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Adjetivos",
        board="IMPARH"
    )
    q_adj5 = Question(
        topic_id=t_adjetivo.id,
        statement="Em 'Ele comprou uma mesa de mármore', a expressão destacada funciona como:",
        option_a="substantivo composto",
        option_b="locução adjetiva",
        option_c="advérbio de modo",
        option_d="artigo indefinido",
        correct_option="B",
        justification_correct="'De mármore' é formado por preposição + substantivo, qualificando a mesa. Portanto, é uma locução adjetiva.",
        justification_incorrect="Não é substantivo composto, e sim um modificador de substantivo (locução adjetiva).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Adjetivos",
        board="IMPARH"
    )
    db.add_all([q_adj1, q_adj2, q_adj3, q_adj4, q_adj5])
    db.commit()

    # Flashcards Adjetivo
    fc_adj1 = Flashcard(topic_id=t_adjetivo.id, front="O que é uma Locução Adjetiva?", back="É uma expressão com valor de adjetivo, geralmente formada por preposição + substantivo (Ex: de ferro = férreo, de mãe = materno).")
    fc_adj2 = Flashcard(topic_id=t_adjetivo.id, front="Qual a diferença entre Superlativo Absoluto Analítico e Sintético?", back="Analítico usa um advérbio de intensidade (Ex: muito alto). Sintético usa um sufixo (Ex: altíssimo).")
    fc_adj3 = Flashcard(topic_id=t_adjetivo.id, front="O que são adjetivos pátrios ou gentílicos?", back="São aqueles que indicam a nacionalidade ou local de origem de um ser (Ex: brasileiro, paranaense, carioca).")
    db.add_all([fc_adj1, fc_adj2, fc_adj3])
    db.commit()


    # --- 1.4 NUMERAL ---
    numeral_theory = """
# O que é o Numeral?
O numeral é a classe de palavras variável que indica quantidade exata de seres, a ordem em que eles se apresentam, a multiplicação ou a fração de uma grandeza. Diferencia-se do adjetivo por indicar precisão matemática e não qualidades.

## Classificação do Numeral

| Tipo | Definição | Exemplos |
|---|---|---|
| **Cardinal** | Indica quantidade exata e absoluta. | um, dois, cem, mil |
| **Ordinal** | Indica posição ou ordem em uma série. | primeiro, décimo, centésimo |
| **Multiplicativo** | Indica multiplicação de uma quantidade. | dobro, triplo, quádruplo |
| **Fracionário** | Indica divisão ou fração de uma quantidade. | meio, um terço, dois quintos |

## Observações de Uso e Flexão
* Os numerais cardinais como *“um”*, *“dois”* e as centenas flexionam em gênero (*uma*, *duas*, *duzentas*).
* A partir de dez milhões, os numerais passam a se comportar como substantivos compostos.

> 💡 **Fique Atento:**
> Cuidado para não confundir o numeral cardinal com um substantivo. Em *“Tirei um dez na prova”*, a palavra *“dez”* funciona como substantivo (nome da nota), e não como numeral.
"""
    t_numeral = Topic(
        unit_id=unit_variaveis.id,
        title="1.4 Numeral",
        difficulty=1,
        order_index=4,
        introduction="Compreenda a indicação numérica exata, os tipos de numerais e suas flexões.",
        theory_markdown=numeral_theory
    )
    db.add(t_numeral)
    db.commit()
    db.refresh(t_numeral)

    # Questões de Numeral
    q_num1 = Question(
        topic_id=t_numeral.id,
        statement="Em 'Ele ficou em décimo lugar na competição', o numeral destacado é:",
        option_a="cardinal",
        option_b="ordinal",
        option_c="multiplicativo",
        option_d="fracionário",
        correct_option="B",
        justification_correct="'Décimo' indica a posição exata em uma sequência, correspondendo a um numeral ordinal.",
        justification_incorrect="Cardinais indicam quantidades absolutas e multiplicativos indicam multiplicação.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Numerais",
        board="IMPARH"
    )
    q_num2 = Question(
        topic_id=t_numeral.id,
        statement="Assinale a alternativa com um numeral fracionário:",
        option_a="quinto lugar",
        option_b="dois quintos",
        option_c="quíntuplo",
        option_d="cinco",
        correct_option="B",
        justification_correct="'Dois quintos' expressa uma fração ou divisão de partes, sendo classificado como fracionário.",
        justification_incorrect="'Quinto' é ordinal, 'quíntuplo' é multiplicativo e 'cinco' é cardinal.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Numerais",
        board="IMPARH"
    )
    q_num3 = Question(
        topic_id=t_numeral.id,
        statement="Em 'O aluguel dobrou de valor', a ideia numérica presente remete ao numeral:",
        option_a="cardinal",
        option_b="ordinal",
        option_c="multiplicativo",
        option_d="fracionário",
        correct_option="C",
        justification_correct="A palavra 'dobrou' remete à ideia de 'o dobro' (multiplicação por dois), associada ao numeral multiplicativo.",
        justification_incorrect="Não indica ordem, fração ou quantidade estática.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Numerais",
        board="IMPARH"
    )
    q_num4 = Question(
        topic_id=t_numeral.id,
        statement="Em 'Tirei um dez na redação', a palavra 'dez' classifica-se como:",
        option_a="numeral cardinal",
        option_b="numeral ordinal",
        option_c="substantivo",
        option_d="adjetivo",
        correct_option="C",
        justification_correct="Precedida de artigo, a palavra 'dez' funciona como substantivo por nomear a nota obtida na avaliação.",
        justification_incorrect="Mesmo representando um número, neste contexto ela foi substantivada e funciona como substantivo comum.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Numerais",
        board="IMPARH"
    )
    q_num5 = Question(
        topic_id=t_numeral.id,
        statement="Qual numeral cardinal está corretamente flexionado em gênero?",
        option_a="duas mil pessoas",
        option_b="dois mil pessoas",
        option_c="segunda mil pessoas",
        option_d="duzenta pessoas",
        correct_option="A",
        justification_correct="'Duas' está flexionado no feminino concordando com o substantivo 'pessoas' (duas mil pessoas).",
        justification_incorrect="'Dois' e 'duzenta' apresentam erros de concordância de gênero com 'pessoas'.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Numerais",
        board="IMPARH"
    )
    db.add_all([q_num1, q_num2, q_num3, q_num4, q_num5])
    db.commit()

    # Flashcards Numeral
    fc_num1 = Flashcard(topic_id=t_numeral.id, front="Quais são os quatro tipos de numerais?", back="Cardinais (quantidade: um, dois), Ordinais (ordem: primeiro), Multiplicativos (dobro, triplo) e Fracionários (meio, terço).")
    fc_num2 = Flashcard(topic_id=t_numeral.id, front="Como se flexionam os numerais cardinais?", back="Alguns flexionam em gênero (um/uma, dois/duas, duzentos/duzentas). Outros são invariáveis (três, quatro, etc.).")
    fc_num3 = Flashcard(topic_id=t_numeral.id, front="A partir de qual valor os numerais podem ser escritos como substantivos compostos?", back="A partir de dez milhões (ex: 10.000.000 é escrito como substantivo composto).")
    db.add_all([fc_num1, fc_num2, fc_num3])
    db.commit()


    # --- 1.5 PRONOME ---
    pronome_theory = """
# O que é o Pronome?
O pronome é a classe variável que substitui (pronome substantivo) ou acompanha (pronome adjetivo) o substantivo, situando os seres em relação às três pessoas do discurso:
* **1ª Pessoa:** quem fala (*eu, nós*).
* **2ª Pessoa:** com quem se fala (*tu, vós, você*).
* **3ª Pessoa:** de quem se fala (*ele, ela, eles, elas*).

## Classificação do Pronome

| Tipo | Definição | Exemplos |
|---|---|---|
| **Pessoal Reto** | Funciona como sujeito da oração. | eu, tu, ele, nós, vós, eles |
| **Pessoal Oblíquo** | Funciona como complemento verbal. | me, te, se, o, a, lhe, nos, vos |
| **Possessivo** | Indica posse em relação às pessoas do discurso. | meu, teu, seu, nosso, vosso |
| **Demonstrativo** | Aponta a localização no espaço, tempo ou texto. | este, esse, aquele, isto, isso |
| **Relativo** | Retoma um antecedente e inicia oração dependente. | que, quem, o qual, cujo, onde |
| **Indefinido** | Refere-se à terceira pessoa de modo vago e impreciso. | algum, nenhum, todo, alguém, ninguém |
| **Interrogativo** | Empregado na formulação de perguntas diretas ou indiretas. | quem?, qual?, quanto?, o quê? |
| **Tratamento** | Usado no tratamento cortês ou formal. | você, senhor, Vossa Excelência |

## Observações de Concordância
Os pronomes de tratamento exigem que a concordância verbal e pronominal ocorra sempre na **3ª pessoa**, mesmo que se refiram ao interlocutor (2ª pessoa): *“Vossa Excelência está enganado”*.

> 💡 **Fique Atento:**
> O pronome relativo *“cujo”* exprime posse, concorda com o termo seguinte e nunca aceita artigo após si (não existe *“cujo o”* ou *“cujo a”*).
"""
    t_pronome = Topic(
        unit_id=unit_variaveis.id,
        title="1.5 Pronome",
        difficulty=3,
        order_index=5,
        introduction="Aprofunde-se nos pronomes, suas funções de coesão, tabelas e regras de concordância.",
        theory_markdown=pronome_theory
    )
    db.add(t_pronome)
    db.commit()
    db.refresh(t_pronome)

    # Questões de Pronome
    q_pro1 = Question(
        topic_id=t_pronome.id,
        statement="Em 'Comprei o presente para ela', o pronome destacado classifica-se como:",
        option_a="pessoal reto",
        option_b="pessoal oblíquo",
        option_c="possessivo",
        option_d="demonstrativo",
        correct_option="B",
        justification_correct="'Ela' neste caso funciona como complemento precedido de preposição ('para ela'), classificando-se como pronome pessoal oblíquo tônico.",
        justification_incorrect="Os pronomes pessoais retos exercem a função de sujeito, não de complemento preposicionado.",
        difficulty=3,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Pronomes",
        board="IMPARH"
    )
    q_pro2 = Question(
        topic_id=t_pronome.id,
        statement="Assinale a frase com pronome relativo:",
        option_a="Alguém bateu à porta.",
        option_b="O livro que você emprestou é ótimo.",
        option_c="Nós saímos cedo.",
        option_d="Aquele carro é meu.",
        correct_option="B",
        justification_correct="A palavra 'que' retoma o termo antecedente 'livro' e introduz uma oração adjetiva, funcionando como pronome relativo.",
        justification_incorrect="Nas outras opções temos pronomes indefinidos (Alguém), retos (Nós) e demonstrativos (Aquele).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Pronomes",
        board="IMPARH"
    )
    q_pro3 = Question(
        topic_id=t_pronome.id,
        statement="Em 'Vossa Excelência conhece bem o processo', o verbo concorda com o pronome de tratamento na:",
        option_a="primeira pessoa do singular",
        option_b="segunda pessoa do singular",
        option_c="terceira pessoa do singular",
        option_d="terceira pessoa do plural",
        correct_option="C",
        justification_correct="Todos os pronomes de tratamento concordam com verbos e pronomes na 3ª pessoa (conhece -> ele/ela).",
        justification_incorrect="Eles não concordam em 2ª pessoa (tu) nem em 1ª pessoa.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Pronomes",
        board="IMPARH"
    )
    q_pro4 = Question(
        topic_id=t_pronome.id,
        statement="Qual pronome abaixo é classificado como indefinido?",
        option_a="este",
        option_b="cujo",
        option_c="ninguém",
        option_d="eu",
        correct_option="C",
        justification_correct="'Ninguém' é classificado como pronome indefinido por referir-se à 3ª pessoa de forma vaga.",
        justification_incorrect="'Este' é demonstrativo, 'cujo' é relativo e 'eu' é reto.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Pronomes",
        board="IMPARH"
    )
    q_pro5 = Question(
        topic_id=t_pronome.id,
        statement="Em 'Meu carro e o seu estão na garagem', os pronomes destacados são:",
        option_a="demonstrativos",
        option_b="possessivos",
        option_c="relativos",
        option_d="interrogativos",
        correct_option="B",
        justification_correct="'Meu' e 'seu' indicam posse em relação às pessoas do discurso (1ª e 3ª pessoas), classificando-se como possessivos.",
        justification_incorrect="Eles não indicam relação espacial (demonstrativo) ou conexão de orações (relativo).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Pronomes",
        board="IMPARH"
    )
    db.add_all([q_pro1, q_pro2, q_pro3, q_pro4, q_pro5])
    db.commit()

    # Flashcards Pronome
    fc_pro1 = Flashcard(topic_id=t_pronome.id, front="Qual a regra de concordância verbal para pronomes de tratamento?", back="Eles sempre exigem verbo na 3ª pessoa. Ex: 'Vossa Excelência está enganado' (e não 'estás').")
    fc_pro2 = Flashcard(topic_id=t_pronome.id, front="Qual a particularidade do pronome relativo 'cujo'?", back="Estabelece relação de posse e concorda em gênero e número com o substantivo que o segue. Ex: a casa cujo telhado caiu.")
    fc_pro3 = Flashcard(topic_id=t_pronome.id, front="Pronomes pessoais oblíquos átonos podem funcionar como sujeito?", back="Não, eles exercem função de complemento verbal (objeto direto ou indireto). Ex: 'Ele me chamou'.")
    db.add_all([fc_pro1, fc_pro2, fc_pro3])
    db.commit()


    # --- 1.6 VERBO ---
    verbo_theory = """
# O que é o Verbo?
O verbo é a classe de palavras que expressa ação, estado, mudança de estado ou fenômeno da natureza, situando o fato no tempo (presente, pretérito ou futuro). É o núcleo do predicado e elemento indispensável da oração.

## Modos e Vozes Verbais

| Modo / Voz | Definição | Exemplos |
|---|---|---|
| **Indicativo** | Expressa certeza, um fato real. | eu estudo, ele passará |
| **Subjuntivo** | Expressa dúvida, desejo ou hipótese. | se eu estudasse, que ele venha |
| **Imperativo** | Expressa ordem, pedido ou conselho. | estude!, não faça isso! |
| **Voz Ativa** | O sujeito pratica a ação expressa. | O aluno resolveu a questão. |
| **Voz Passiva** | O sujeito sofre a ação expressa. | A questão foi resolvida pelo aluno. |
| **Voz Reflexiva** | O sujeito pratica e sofre a ação. | O candidato cortou-se. |

## Flexão e Locução Verbal
* **Conjugações:** 1ª (-ar: *cantar*), 2ª (-er/or: *vender*, *pôr*) e 3ª (-ir: *partir*).
* **Locução Verbal:** Formada por verbo auxiliar (variável) + verbo principal (nas formas nominais de infinitivo, gerúndio ou particípio): *“vou passar”*.

> 💡 **Fique Atento:**
> Não confunda locução verbal com tempos compostos. O importante é saber que a locução expressa um único processo verbal com auxílio de outros verbos.
"""
    t_verbo = Topic(
        unit_id=unit_variaveis.id,
        title="1.6 Verbo",
        difficulty=3,
        order_index=6,
        introduction="Domine os tempos, modos, vozes verbais e a estruturação das locuções na oração.",
        theory_markdown=verbo_theory
    )
    db.add(t_verbo)
    db.commit()
    db.refresh(t_verbo)

    # Questões de Verbo
    q_ver1 = Question(
        topic_id=t_verbo.id,
        statement="Em 'Se eu fosse rico, viajaria pelo mundo', o verbo destacado está no modo:",
        option_a="indicativo",
        option_b="subjuntivo",
        option_c="imperativo",
        option_d="infinitivo",
        correct_option="B",
        justification_correct="'Fosse' expressa uma hipótese irreal no pretérito, pertencendo ao modo subjuntivo.",
        justification_incorrect="O indicativo expressa certeza e o imperativo expressa ordem.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Verbos",
        board="IMPARH"
    )
    q_ver2 = Question(
        topic_id=t_verbo.id,
        statement="A frase 'O bolo foi assado por Maria' está na voz:",
        option_a="ativa",
        option_b="passiva",
        option_c="reflexiva",
        option_d="recíproca",
        correct_option="B",
        justification_correct="O sujeito sofrer a ação ('bolo foi assado') caracteriza a voz passiva analítica.",
        justification_incorrect="Se fosse ativa, a frase seria 'Maria assou o bolo'.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Verbos",
        board="IMPARH"
    )
    q_ver3 = Question(
        topic_id=t_verbo.id,
        statement="Assinale a alternativa que contém uma locução verbal:",
        option_a="Ele correu rápido.",
        option_b="Ela estava estudando à noite.",
        option_c="Comemos bem naquele restaurante.",
        option_d="O sol brilhou forte.",
        correct_option="B",
        justification_correct="'Estava estudando' combina o auxiliar 'estava' com o principal no gerúndio 'estudando', caracterizando uma locução.",
        justification_incorrect="As outras opções possuem apenas um verbo simples expressando a ação.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Verbos",
        board="IMPARH"
    )
    q_ver4 = Question(
        topic_id=t_verbo.id,
        statement="Em 'Não fales alto durante a reunião', o verbo está no modo:",
        option_a="indicativo",
        option_b="subjuntivo",
        option_c="imperativo negativo",
        option_d="gerúndio",
        correct_option="C",
        justification_correct="Expressa uma ordem de forma proibitiva (não fazer algo), caracterizando o imperativo negativo.",
        justification_incorrect="O gerúndio é uma forma nominal e não um modo verbal independente.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Verbos",
        board="IMPARH"
    )
    q_ver5 = Question(
        topic_id=t_verbo.id,
        statement="Qual verbo abaixo pertence à 3ª conjugação?",
        option_a="cantar",
        option_b="vender",
        option_c="partir",
        option_d="correr",
        correct_option="C",
        justification_correct="Os verbos terminados em '-ir' no infinitivo pertencem à 3ª conjugação, como 'partir'.",
        justification_incorrect="'Cantar' é da 1ª conjugação (-ar) e 'vender'/'correr' são da 2ª conjugação (-er).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Verbos",
        board="IMPARH"
    )
    db.add_all([q_ver1, q_ver2, q_ver3, q_ver4, q_ver5])
    db.commit()

    # Flashcards Verbo
    fc_ver1 = Flashcard(topic_id=t_verbo.id, front="Quais são as três conjugações verbais no português?", back="1ª conjugação: terminados em -ar (cantar). 2ª conjugação: terminados em -er/or (vender, pôr). 3ª conjugação: terminados em -ir (partir).")
    fc_ver2 = Flashcard(topic_id=t_verbo.id, front="O que caracteriza a voz passiva analítica?", back="É formada pelo verbo auxiliar (geralmente ser) + particípio do verbo principal. Ex: O trabalho foi entregue.")
    fc_ver3 = Flashcard(topic_id=t_verbo.id, front="Qual a diferença entre o modo Indicativo e Subjuntivo?", back="O Indicativo expressa certeza, fatos reais. O Subjuntivo expressa dúvida, desejo, hipótese ou incerteza.")
    db.add_all([fc_ver1, fc_ver2, fc_ver3])
    db.commit()


    # --- 1.7 ADVÉRBIO ---
    adverbio_theory = """
# O que é o Advérbio?
O advérbio é a classe de palavras invariável que modifica o sentido de um verbo, de um adjetivo ou de outro advérbio (e por vezes de uma oração inteira), atribuindo-lhes uma circunstância.

## Classificação do Advérbio

| Tipo | Definição | Exemplos |
|---|---|---|
| **Tempo** | Indica a circunstância temporal do fato. | hoje, ontem, sempre, cedo |
| **Lugar** | Indica o local de ocorrência da ação. | aqui, ali, longe, dentro |
| **Modo** | Indica a maneira como a ação se realiza. | bem, mal, devagar, rapidamente |
| **Intensidade** | Modifica o grau da qualidade ou ação. | muito, pouco, bastante, demais |
| **Afirmação** | Reforça a certeza do fato. | sim, certamente, realmente |
| **Negação** | Nega a realização do fato. | não, nunca, jamais |
| **Dúvida** | Expressa incerteza ou possibilidade. | talvez, possivelmente, quiçá |

## Flexão de Grau do Advérbio
Apesar de invariável em gênero/número, o advérbio pode apresentar variações de grau:
* **Comparativo:** de igualdade (*tão cedo quanto*), superioridade (*mais cedo que*) ou inferioridade (*menos cedo que*).
* **Superlativo:** absoluto analítico (*muito cedo*) ou absoluto sintético (*cedíssimo*).

> 💡 **Fique Atento:**
> Muitos advérbios de modo são formados pelo acréscimo do sufixo *-mente* à forma feminina do adjetivo: *rápida* + *-mente* = *rapidamente*.
> Advérbios **não** variam para concordar com o substantivo. Se a palavra variar, ela não é advérbio!
"""
    t_adverbio = Topic(
        unit_id=unit_invariaveis.id,
        title="1.7 Advérbio",
        difficulty=2,
        order_index=1,
        introduction="Estude as circunstâncias adverbiais, as variações de grau e a invariabilidade gramatical.",
        theory_markdown=adverbio_theory
    )
    db.add(t_adverbio)
    db.commit()
    db.refresh(t_adverbio)

    # Questões de Advérbio
    q_adv1 = Question(
        topic_id=t_adverbio.id,
        statement="Em 'Ela mora longe do centro', o advérbio destacado expressa circunstância de:",
        option_a="tempo",
        option_b="modo",
        option_c="lugar",
        option_d="intensidade",
        correct_option="C",
        justification_correct="'Longe' exprime distância espacial, constituindo um advérbio de lugar.",
        justification_incorrect="'Longe' não indica tempo, intensidade ou a maneira da ação (modo).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Advérbios",
        board="IMPARH"
    )
    q_adv2 = Question(
        topic_id=t_adverbio.id,
        statement="Assinale a alternativa com advérbio de dúvida:",
        option_a="sempre",
        option_b="possivelmente",
        option_c="aqui",
        option_d="muito",
        correct_option="B",
        justification_correct="'Possivelmente' exprime probabilidade ou dúvida acerca do acontecimento.",
        justification_incorrect="'Sempre' é de tempo, 'aqui' de lugar e 'muito' de intensidade.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Advérbios",
        board="IMPARH"
    )
    q_adv3 = Question(
        topic_id=t_adverbio.id,
        statement="O advérbio 'felizmente' é formado por:",
        option_a="adjetivo no masculino + mente",
        option_b="adjetivo no feminino + mente",
        option_c="substantivo + mente",
        option_d="verbo + mente",
        correct_option="B",
        justification_correct="Advérbios sufixados em '-mente' ligam-se ao adjetivo base flexionado no feminino (ex: feliz + mente, rapida-mente).",
        justification_incorrect="Não se formam a partir do gênero masculino ou de substantivos/verbos.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Advérbios",
        board="IMPARH"
    )
    q_adv4 = Question(
        topic_id=t_adverbio.id,
        statement="Em 'Ele chegou tarde demais à reunião', o advérbio 'demais' está no grau:",
        option_a="comparativo de igualdade",
        option_b="comparativo de superioridade",
        option_c="superlativo analítico",
        option_d="superlativo sintético",
        correct_option="C",
        justification_correct="'Tarde demais' intensifica o advérbio com o auxílio de outro termo modificador, configurando o grau superlativo analítico.",
        justification_incorrect="Não é sintético (que usaria sufixo como tardíssimo) nem estabelece comparação de igualdade ou superioridade.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Advérbios",
        board="IMPARH"
    )
    q_adv5 = Question(
        topic_id=t_adverbio.id,
        statement="Qual frase contém advérbio de negação?",
        option_a="Ele jamais desiste.",
        option_b="Ele sempre desiste.",
        option_c="Ele quase desiste.",
        option_d="Ele ainda desiste.",
        correct_option="A",
        justification_correct="'Jamais' atua negando o processo verbal, sendo um advérbio de negação.",
        justification_incorrect="Sempre é de tempo; quase é de intensidade ou aproximação; ainda é de tempo.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Advérbios",
        board="IMPARH"
    )
    db.add_all([q_adv1, q_adv2, q_adv3, q_adv4, q_adv5])
    db.commit()

    # Flashcards Advérbio
    fc_adv1 = Flashcard(topic_id=t_adverbio.id, front="O advérbio se flexiona em gênero e número?", back="Não, o advérbio é uma classe invariável. Ele nunca concorda com outros termos da oração.")
    fc_adv2 = Flashcard(topic_id=t_adverbio.id, front="Qual a função do advérbio em uma oração?", back="Modificar o sentido de um verbo, de um adjetivo, de outro advérbio ou de uma frase inteira, indicando uma circunstância.")
    fc_adv3 = Flashcard(topic_id=t_adverbio.id, front="Como é formado o grau superlativo analítico dos advérbios?", back="Pela presença de outro advérbio de intensidade acompanhando o principal. Ex: muito tarde, tarde demais.")
    db.add_all([fc_adv1, fc_adv2, fc_adv3])
    db.commit()


    # --- 1.8 PREPOSIÇÃO ---
    preposicao_theory = """
# O que é a Preposição?
A preposição é a classe invariável que serve de conectivo para ligar dois termos dentro de uma oração, subordinando o segundo ao primeiro (estabelecendo relações de sentido).

## Classificação e Relações

| Tipo | Definição | Exemplos |
|---|---|---|
| **Essenciais** | Palavras cuja única função gramatical é atuar como preposição. | a, de, em, para, com, por, sem, sob, sobre |
| **Acidentais** | Palavras de outras classes que podem funcionar como preposição. | durante, mediante, segundo, conforme, exceto |
| **Locução Prepositiva** | Expressão equivalente a uma preposição (terminada em preposição essencial). | apesar de, a fim de, por causa de, ao lado de |

## Combinações e Contrações
* **Combinação:** Junção da preposição com outra classe sem perda de fonemas (ex: *a* + *o* = *ao*).
* **Contração:** Junção com alteração de som ou perda de letras (ex: *de* + *o* = *do*; *em* + *a* = *na*).

> 💡 **Fique Atento:**
> A contração da preposição *“a”* com o artigo feminino *“a”* gera a crase (*“à”*), tema muito cobrado em provas.
"""
    t_preposicao = Topic(
        unit_id=unit_invariaveis.id,
        title="1.8 Preposição",
        difficulty=2,
        order_index=2,
        introduction="Entenda o papel de ligação das preposições, suas contrações e locuções prepositivas.",
        theory_markdown=preposicao_theory
    )
    db.add(t_preposicao)
    db.commit()
    db.refresh(t_preposicao)

    # Questões de Preposição
    q_prep1 = Question(
        topic_id=t_preposicao.id,
        statement="Em 'Ela trabalha mediante contrato', a palavra destacada ('mediante') é uma preposição:",
        option_a="essencial",
        option_b="acidental",
        option_c="combinada",
        option_d="contraída",
        correct_option="B",
        justification_correct="'Mediante' pertence originalmente a outra classe de palavras (verbo/particípio), funcionando aqui como preposição acidental.",
        justification_incorrect="As preposições essenciais são termos puramente prepositivos (a, de, em...).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Preposições",
        board="IMPARH"
    )
    q_prep2 = Question(
        topic_id=t_preposicao.id,
        statement="A forma 'pelo' resulta da:",
        option_a="combinação de per + o",
        option_b="contração de por + o",
        option_c="combinação de para + o",
        option_d="contração de a + o",
        correct_option="B",
        justification_correct="A contração da preposição 'por' (historicamente 'per') com o artigo 'o' resulta na forma 'pelo'.",
        justification_incorrect="Não é de 'para + o' ou 'a + o'.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Preposições",
        board="IMPARH"
    )
    q_prep3 = Question(
        topic_id=t_preposicao.id,
        statement="Assinale a locução prepositiva:",
        option_a="a fim de",
        option_b="muito bem",
        option_c="tão logo",
        option_d="quase sempre",
        correct_option="A",
        justification_correct="'A fim de' é uma locução prepositiva por ligar termos terminando com a preposição essencial 'de'.",
        justification_incorrect="Os outros representam locuções adverbiais ou conjuncionais.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Preposições",
        board="IMPARH"
    )
    q_prep4 = Question(
        topic_id=t_preposicao.id,
        statement="Em 'Ele estava com raiva do irmão', quantas preposições (incluindo contrações) aparecem?",
        option_a="nenhuma",
        option_b="uma",
        option_c="duas",
        option_d="três",
        correct_option="C",
        justification_correct="Aparecem 'com' (preposição essencial) e 'do' (contração da preposição 'de' + artigo 'o'). Portanto, duas preposições.",
        justification_incorrect="A contagem correta é duas. 'Raiva' é substantivo e 'irmão' também.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Preposições",
        board="IMPARH"
    )
    q_prep5 = Question(
        topic_id=t_preposicao.id,
        statement="Qual das opções é exemplo de combinação (sem perda de fonema)?",
        option_a="do",
        option_b="na",
        option_c="ao",
        option_d="pelo",
        correct_option="C",
        justification_correct="A junção de 'a + o' = 'ao' ocorre sem alteração ou perda de letras, caracterizando combinação.",
        justification_incorrect="Nas outras temos perda/alteração de som: de+o (do), em+a (na), por+o (pelo).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Preposições",
        board="IMPARH"
    )
    db.add_all([q_prep1, q_prep2, q_prep3, q_prep4, q_prep5])
    db.commit()

    # Flashcards Preposição
    fc_prep1 = Flashcard(topic_id=t_preposicao.id, front="O que é uma Preposição Essencial?", back="Palavras que funcionam unicamente como preposição. Ex: a, de, em, para, com, por, sem, sob, sobre.")
    fc_prep2 = Flashcard(topic_id=t_preposicao.id, front="O que é uma Locução Prepositiva?", back="Duas ou mais palavras que juntas exercem o papel de preposição, geralmente terminando com uma preposição essencial (Ex: apesar de, a fim de, por causa de).")
    fc_prep3 = Flashcard(topic_id=t_preposicao.id, front="Qual a diferença entre preposições essenciais e acidentais?", back="As essenciais só funcionam como preposição. As acidentais pertencem a outras classes gramaticais, mas passam a atuar como preposição em alguns contextos (Ex: segundo, durante, mediante).")
    db.add_all([fc_prep1, fc_prep2, fc_prep3])
    db.commit()


    # --- 1.9 CONJUNÇÃO ---
    conjuncao_theory = """
# O que é a Conjunção?
A conjunção é a classe de palavras invariável que liga orações ou termos de mesma função sintática, estabelecendo conexões lógicas de coordenação ou subordinação.

## Classificação das Conjunções

| Tipo | Relação de Sentido | Principais Conjunções |
|---|---|---|
| **Aditiva** | Soma ou adição de ideias. | e, nem, não só... mas também |
| **Adversativa** | Oposição, contraste ou quebra de expectativa. | mas, porém, contudo, todavia, entretanto |
| **Alternativa** | Alternância ou exclusão. | ou... ou, ora... ora, quer... quer |
| **Conclusiva** | Conclusão ou consequência lógica. | logo, portanto, por isso, destarte |
| **Explicativa** | Justificativa ou explicação do fato anterior. | pois, porque, porquanto, que |
| **Integrante** | Introduz oração subordinada substantiva. | que, se |
| **Causal/Condicional...** | Introduz orações circunstanciais subordinadas. | porque, se, embora, quando, conforme |

## Coordenação vs. Subordinação
* **Coordenativas:** Ligam termos de independência sintática: *“Estudei e passei”*.
* **Subordinativas:** Ligam orações onde uma desempenha função sintática em relação à outra: *“Espero que passes”*.

> 💡 **Fique Atento:**
> Uma mesma conjunção pode apresentar diferentes sentidos de acordo com o contexto oracional. O termo *“que”* pode atuar como integrante, explicativo ou mesmo pronome relativo.
"""
    t_conjuncao = Topic(
        unit_id=unit_invariaveis.id,
        title="1.9 Conjunção",
        difficulty=3,
        order_index=3,
        introduction="Domine as conexões lógicas das conjunções coordenativas, subordinativas e seus valores semânticos.",
        theory_markdown=conjuncao_theory
    )
    db.add(t_conjuncao)
    db.commit()
    db.refresh(t_conjuncao)

    # Questões de Conjunção
    q_conj1 = Question(
        topic_id=t_conjuncao.id,
        statement="Em 'Não fui à festa porque estava doente', a conjunção destacada expressa relação de:",
        option_a="conclusão",
        option_b="causa",
        option_c="condição",
        option_d="concessão",
        correct_option="B",
        justification_correct="'Porque' introduz a causa ou o motivo de o sujeito não ter ido à festa.",
        justification_incorrect="Não exprime conclusão (portanto), condição (se) ou concessão (embora).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Conjunções",
        board="IMPARH"
    )
    q_conj2 = Question(
        topic_id=t_conjuncao.id,
        statement="Assinale a conjunção coordenativa adversativa:",
        option_a="e",
        option_b="porém",
        option_c="portanto",
        option_d="que",
        correct_option="B",
        justification_correct="'Porém' indica uma quebra de expectativa ou contraste, classificando-se como adversativa.",
        justification_incorrect="'E' é aditiva, 'portanto' é conclusiva e 'que' pode ter diversas funções, mas não é classicamente adversativa coordenativa.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Conjunções",
        board="IMPARH"
    )
    q_conj3 = Question(
        topic_id=t_conjuncao.id,
        statement="Em 'Embora estivesse cansado, terminou o trabalho', a oração destacada tem valor:",
        option_a="causal",
        option_b="condicional",
        option_c="concessivo",
        option_d="conclusivo",
        correct_option="C",
        justification_correct="'Embora' expressa uma concessão (uma oposição aceita que não impede o resultado final).",
        justification_incorrect="Não indica uma causa, condição ou conclusão direta.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Conjunções",
        board="IMPARH"
    )
    q_conj4 = Question(
        topic_id=t_conjuncao.id,
        statement="Qual conjunção classifica-se como subordinativa integrante?",
        option_a="mas",
        option_b="que (Espero que ele venha)",
        option_c="logo",
        option_d="ou",
        correct_option="B",
        justification_correct="Em 'Espero que ele venha', a conjunção 'que' introduz uma oração subordinada substantiva objetiva direta, funcionando como integrante.",
        justification_incorrect="'Mas' é adversativa, 'logo' é conclusiva e 'ou' é alternativa.",
        difficulty=3,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Conjunções",
        board="IMPARH"
    )
    q_conj5 = Question(
        topic_id=t_conjuncao.id,
        statement="Em 'Chovia muito; por isso, adiamos a viagem', a expressão destacada é conjunção:",
        option_a="aditiva",
        option_b="alternativa",
        option_c="conclusiva",
        option_d="explicativa",
        correct_option="C",
        justification_correct="'Por isso' estabelece a conclusão ou consequência lógica do fato de estar chovendo muito.",
        justification_incorrect="Não exprime acréscimo (aditiva) ou explicação direta (explicativa).",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Conjunções",
        board="IMPARH"
    )
    db.add_all([q_conj1, q_conj2, q_conj3, q_conj4, q_conj5])
    db.commit()

    # Flashcards Conjunção
    fc_conj1 = Flashcard(topic_id=t_conjuncao.id, front="Qual a diferença básica entre coordenação e subordinação?", back="Na coordenação as orações são independentes sintaticamente (Ex: Estudei e passei). Na subordinação, uma oração depende sintaticamente da outra (Ex: Sei que passará).")
    fc_conj2 = Flashcard(topic_id=t_conjuncao.id, front="Quais são as principais conjunções coordenativas adversativas?", back="mas, porém, contudo, todavia, entretanto, no entanto. Elas indicam oposição ou contraste de ideias.")
    fc_conj3 = Flashcard(topic_id=t_conjuncao.id, front="O que faz uma conjunção subordinativa integrante?", back="Introduz orações subordinadas substantivas (que completam o sentido de termos da oração principal). Ex: Quero que você venha.")
    db.add_all([fc_conj1, fc_conj2, fc_conj3])
    db.commit()


    # --- 1.10 INTERJEIÇÃO ---
    interjeicao_theory = """
# O que é a Interjeição?
A interjeição é a classe invariável que exprime de modo direto e emocional sentimentos, sensações, apelos e estados de espírito repentinos do falante. Costuma vir acompanhada de ponto de exclamação.

## Classificação das Interjeições

| Sentimento / Tipo | Definição / Apelo | Exemplos |
|---|---|---|
| **Alegria** | Expressa contentamento. | Oba!, Viva!, Que bom! |
| **Dor / Sofrimento** | Expressa sofrimento físico ou emocional. | Ai!, Ui!, Ah! |
| **Surpresa** | Expressa espanto ou admiração. | Nossa!, Uau!, Caramba! |
| **Alívio** | Expressa sossego após tensão. | Uf!, Graças a Deus!, Ainda bem! |
| **Advertência** | Expressa chamado de atenção ou alerta. | Cuidado!, Atenção!, Olha! |
| **Repulsa** | Expressa nojo ou rejeição. | Eca!, Argh! |
| **Locução Interjetiva** | Duas ou mais palavras com valor de interjeição. | Meu Deus!, Que pena!, Ora bolas! |

> 💡 **Fique Atento:**
> Uma mesma palavra pode funcionar como interjeição em um contexto e outra classe em outro: *“Fogo!”* (interjeição de alerta) x *“O fogo queimou a floresta”* (substantivo).
"""
    t_interjeicao = Topic(
        unit_id=unit_invariaveis.id,
        title="1.10 Interjeição",
        difficulty=1,
        order_index=4,
        introduction="Aprenda sobre a classe expressiva das interjeições, seus apelos e locuções interjetivas.",
        theory_markdown=interjeicao_theory
    )
    db.add(t_interjeicao)
    db.commit()
    db.refresh(t_interjeicao)

    # Questões de Interjeição
    q_int1 = Question(
        topic_id=t_interjeicao.id,
        statement="Em 'Uf! Ainda bem que chegamos a tempo', a interjeição expressa:",
        option_a="surpresa",
        option_b="alívio",
        option_c="dor",
        option_d="advertência",
        correct_option="B",
        justification_correct="'Uf!' traduz a sensação de descanso/tranquilidade após uma situação tensa, sendo de alívio.",
        justification_incorrect="Não indica surpresa (nossa), dor (ai) ou aviso de perigo (cuidado).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Interjeições",
        board="IMPARH"
    )
    q_int2 = Question(
        topic_id=t_interjeicao.id,
        statement="Assinale a locução interjetiva:",
        option_a="Uau!",
        option_b="Ai!",
        option_c="Meu Deus!",
        option_d="Eca!",
        correct_option="C",
        justification_correct="'Meu Deus!' é uma estrutura com duas palavras exercendo papel de interjeição, constituindo uma locução interjetiva.",
        justification_incorrect="As outras opções apresentam apenas interjeições simples formadas por um único termo.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Interjeições",
        board="IMPARH"
    )
    q_int3 = Question(
        topic_id=t_interjeicao.id,
        statement="Em 'Cuidado! O cão está solto', a interjeição expressa:",
        option_a="alegria",
        option_b="advertência",
        option_c="repulsa",
        option_d="alívio",
        correct_option="B",
        justification_correct="'Cuidado!' atua como uma chamada de atenção contra um perigo iminente, sendo uma advertência.",
        justification_incorrect="Não indica alegria, nojo (repulsa) ou descanso (alívio).",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Interjeições",
        board="IMPARH"
    )
    q_int4 = Question(
        topic_id=t_interjeicao.id,
        statement="Qual interjeição abaixo expressa repulsa?",
        option_a="Eca!",
        option_b="Oba!",
        option_c="Nossa!",
        option_d="Uf!",
        correct_option="A",
        justification_correct="'Eca!' é classicamente empregado para expressar nojo, aversão ou repulsa.",
        justification_incorrect="'Oba' indica alegria, 'nossa' surpresa e 'uf' alívio.",
        difficulty=1,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Interjeições",
        board="IMPARH"
    )
    q_int5 = Question(
        topic_id=t_interjeicao.id,
        statement="Em 'Fogo! Corram todos!', a palavra destacada funciona como:",
        option_a="substantivo",
        option_b="interjeição",
        option_c="adjetivo",
        option_d="verbo",
        correct_option="B",
        justification_correct="Neste contexto de urgência e exclamação direta, 'Fogo!' atua expressando desespero e alerta, funcionando como interjeição.",
        justification_incorrect="Embora 'fogo' isolado seja substantivo comum, nesta situação exclamativa assume valor interjetivo.",
        difficulty=2,
        subject="Língua Portuguesa",
        subsubject="Morfologia - Interjeições",
        board="IMPARH"
    )
    db.add_all([q_int1, q_int2, q_int3, q_int4, q_int5])
    db.commit()

    # Flashcards Interjeição
    fc_int1 = Flashcard(topic_id=t_interjeicao.id, front="O que é uma Interjeição?", back="Classe de palavras invariável que exprime emoções, sentimentos e estados de espírito de forma direta e repentina. Ex: Oba!, Ui!, Caramba!")
    fc_int2 = Flashcard(topic_id=t_interjeicao.id, front="O que é uma Locução Interjetiva?", back="Duas ou mais palavras que atuam como interjeição. Ex: Meu Deus!, Que pena!, Ora bolas!")
    fc_int3 = Flashcard(topic_id=t_interjeicao.id, front="Como a interjeição costuma vir pontuada?", back="Normalmente isolada por vírgula ou seguida por ponto de exclamação (!).")
    db.add_all([fc_int1, fc_int2, fc_int3])
    db.commit()

    print("Seed finalizado com sucesso! Todos os 10 tópicos de Morfologia cadastrados.")
    db.close()

if __name__ == "__main__":
    seed_db()
