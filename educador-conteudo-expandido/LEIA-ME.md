# Conteúdo Expandido de Língua Portuguesa — Educador

Este pacote expande o currículo do projeto **Educador-IMPARH** para cobrir
Fundamental I, Fundamental II e Ensino Médio de forma muito mais completa,
mantendo 100% de compatibilidade com o schema atual (`Course -> Module -> Unit
-> Topic -> Question/Flashcard`).

## O que foi adicionado

| Curso | Antes | Depois |
|---|---|---|
| Fundamental I | 1 módulo, 1 tópico | **6 módulos, 15 tópicos** |
| Fundamental II | 1 módulo (Morfologia), 10 tópicos | **8 módulos, 39 tópicos** |
| Ensino Médio | 1 módulo (Barroco), 1 tópico | **10 módulos, 25 tópicos** |
| **Total** | 3 tópicos | **79 tópicos, 371 questões, 231 flashcards** |

### Fundamental I (1º ao 5º ano)
Alfabetização (já existia) · Sílabas e Encontros Sonoros · Ortografia Básica ·
Leitura e Interpretação de Texto · Gêneros Textuais do Cotidiano · Gramática
Inicial (frase/oração, substantivo/adjetivo, verbo)

### Fundamental II (6º ao 9º ano)
Morfologia (já existia, 10 classes gramaticais) · Fonética e Fonologia ·
Ortografia (acentuação, homônimos/parônimos) · Sintaxe — Termos da Oração ·
Sintaxe — Período Composto · Semântica e Estilística (figuras de linguagem) ·
Gêneros Textuais e Produção de Texto · Interpretação de Texto (inferência,
intertextualidade)

### Ensino Médio
Barroco (já existia) · Arcadismo · Romantismo · Realismo/Naturalismo/
Parnasianismo · Simbolismo/Pré-Modernismo · Modernismo (3 gerações) ·
Literatura Contemporânea · Gramática Avançada (concordância, regência, crase,
colocação pronominal) · Redação ENEM (estrutura, competências, proposta de
intervenção) · Interpretação de Texto e Linguagem (funções da linguagem,
variação linguística, leitura de textos multimodais)

## Arquitetura: conteúdo como dados, não código

Em vez de continuar escrevendo objetos SQLAlchemy diretamente dentro de
`seed_db.py` (que já tinha ~1370 linhas só para 12 tópicos), o novo conteúdo
vive em `backend/seed_data/*.py`, cada arquivo definindo apenas uma lista
`MODULES` com dicionários simples (título, teoria em markdown, questões,
flashcards). Um loader genérico (`backend/seed_data/loader.py`) lê esses
dados e cria os registros no banco.

Vantagens:
- Adicionar um módulo novo no futuro = criar um arquivo de dados, sem tocar
  em `seed_db.py` nem entender SQLAlchemy.
- Mais fácil de revisar/validar (é só um dicionário Python, dá para checar
  estrutura programaticamente antes de rodar contra o banco).
- Não quebra nada do que já existia: os 3 tópicos originais (Alfabeto, as 10
  classes gramaticais de Morfologia, Barroco) permanecem intactos, só os
  títulos de dois módulos e de uma unidade foram levemente ajustados para
  fazer sentido ao lado do conteúdo novo (ver abaixo).

## Como aplicar no seu repositório

**Opção A — copiar os arquivos direto:**
1. Copie a pasta `backend/seed_data/` inteira para dentro do seu `backend/`.
2. Substitua o seu `backend/seed_db.py` pelo `backend/seed_db.py` deste pacote
   (ele só adiciona um import e um bloco no final; se você tiver customizado
   o arquivo, aplique o patch abaixo em vez disso).
3. Rode `python seed_db.py` normalmente (dentro do ambiente virtual do
   backend, com o banco configurado).

**Opção B — aplicar o patch git** (preserva histórico e facilita revisão):
```bash
cd Educador-IMPARH
git apply /caminho/para/educador-conteudo-expandido.patch
```

## Pequenos ajustes de nomenclatura feitos em `seed_db.py`

Para o conteúdo novo se encaixar de forma coerente, dois títulos foram
ajustados (o conteúdo pedagógico em si não mudou):
- Fundamental I, Módulo 1: "Alfabetização e Leitura" → "Alfabetização"
  (já que "Leitura e Interpretação" agora é o Módulo 4, dedicado)
- Ensino Médio, Módulo 1: "Literatura e Redação ENEM" → "Literatura
  Brasileira - Barroco" (já que Redação ENEM agora é o Módulo 9, dedicado, e
  esse módulo só continha o tópico de Barroco)
- Ensino Médio, Unidade 1 do Módulo 1: "Barroco e Arcadismo" → "O Barroco no
  Brasil" (Arcadismo agora é o Módulo 2, dedicado)

## Validação feita antes da entrega

- Sintaxe Python de todos os 12 arquivos de dados verificada com `ast.parse`.
- Estrutura de cada tópico validada programaticamente (chaves obrigatórias,
  exatamente 4-5 questões e 3 flashcards por tópico, `correct_option` sempre
  A/B/C/D).
- **Seed completo executado de ponta a ponta** contra um banco SQLite de
  teste, usando os modelos SQLAlchemy reais do projeto — populou 3 cursos,
  24 módulos, 40 unidades, 79 tópicos, 371 questões e 231 flashcards sem
  nenhum erro.

## Próximos passos sugeridos

- Rodar `pytest` do projeto para confirmar que os testes existentes
  (`test_content_hierarchy.py` etc.) continuam passando com o volume maior
  de dados.
- Revisar o conteúdo pedagogicamente (sou um redator de IA — vale uma
  checagem humana de um professor de Português antes de usar em produção,
  especialmente nas questões de Literatura e Gramática Avançada).
- Considerar adicionar exemplos de áudio/pronúncia (`AudioContent`, que já
  existe no schema) para os módulos de Fonética.
