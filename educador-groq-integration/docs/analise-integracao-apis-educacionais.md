# Análise: Integração de APIs de Material Didático no Projeto Educador-IMPARH

## 📋 Sumário Executivo

O projeto **Educador-IMPARH** é uma plataforma de aprendizagem bem estruturada para concursos públicos. Através da análise arquitetural, identifiquei **3 oportunidades estratégicas** para integrar APIs de material didático que potencializariam significativamente o conteúdo disponível.

---

## 🏗️ Visão Geral do Projeto Atual

### Stack Tecnológico
- **Backend**: FastAPI (Python) com padrão Repository
- **Frontend**: Flutter (multiplataforma)
- **Banco de Dados**: PostgreSQL
- **Serviços Externos**: Google Gemini API (Tutor de IA)
- **Arquitetura**: Clean Architecture com injeção de dependência

### Estrutura de Conteúdo Existente
```
Course → Module → Unit → Topic → {Questions, Flashcards, Examples}
```

### Características Principais
- ✅ Estrutura modulada e escalável
- ✅ Padrão Repository implementado
- ✅ Injeção de dependência consolidada
- ✅ Suporte a serviços externos assincronamente
- ✅ Banco de dados bem normalizado

---

## 🎯 Oportunidades de Integração

### 1️⃣ **Wikipedia API** - Enriquecimento Teórico
**Status: ⭐⭐⭐ ALTAMENTE RECOMENDADO**

#### Propósito
Complementar a teoria de tópicos com artigos relevantes da Wikipédia, fornecendo contexto e referências adicionais.

#### Como Implementar

**A. Adicionar dependência:**
```bash
pip install requests  # ou httpx para manter assincronismo
```

**B. Criar novo serviço:**
```python
# backend/app/infrastructure/services/wikipedia_service.py

import httpx
import asyncio
from typing import Optional
from ...core.config import settings

class WikipediaEnricherService:
    """Busca e enriquece conteúdo de tópicos com informações da Wikipedia"""
    
    BASE_URL = "https://pt.wikipedia.org/w/api.php"
    
    @staticmethod
    async def search_article(query: str) -> Optional[dict]:
        """
        Busca um artigo na Wikipedia relacionado ao tópico
        
        Args:
            query: Termo de busca (ex: "Morfologia Portuguesa")
        
        Returns:
            Dict com título, resumo e URL do artigo
        """
        params = {
            "action": "query",
            "format": "json",
            "srsearch": query,
            "srnamespace": "0",
            "srlimit": "1",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}?action=opensearch", params={
                "search": query,
                "limit": 1,
                "namespace": 0,
                "format": "json"
            })
            
            if response.status_code == 200:
                data = response.json()
                if len(data[3]) > 0:
                    return {
                        "title": data[1][0] if data[1] else query,
                        "url": data[3][0] if data[3] else None,
                        "description": data[2][0] if data[2] else "Artigo não encontrado"
                    }
        
        return None
    
    @staticmethod
    async def get_article_content(title: str) -> Optional[str]:
        """Obtém o conteúdo completo de um artigo"""
        params = {
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(WikipediaEnricherService.BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                pages = data.get("query", {}).get("pages", {})
                for page in pages.values():
                    return page.get("extract", "")
        
        return None
```

**C. Adicionar modelo para armazenar referências:**
```python
# backend/app/infrastructure/db/models/content.py (adicionar)

class ExternalReference(Base, TimestampMixin):
    """Referências externas enriquecendo tópicos"""
    __tablename__ = "external_references"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id"), nullable=False)
    source: Mapped[str] = mapped_column(String(50))  # wikipedia, wikibooks, etc
    title: Mapped[str] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(Text)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    topic: Mapped["Topic"] = relationship(back_populates="references")
```

**D. Criar endpoint:**
```python
# backend/app/api/enrich.py

from fastapi import APIRouter, Depends, HTTPException
from ..infrastructure.services.wikipedia_service import WikipediaEnricherService

router = APIRouter(prefix="/topics/{topic_id}", tags=["Enrichment"])

@router.post("/{topic_id}/enrich-with-wikipedia")
async def enrich_topic_with_wikipedia(topic_id: uuid.UUID, db: Session = Depends(get_db)):
    """
    Enriquece um tópico com informações da Wikipedia
    """
    repo = TopicRepository(db)
    topic = repo.get_by_id(topic_id)
    
    if not topic:
        raise HTTPException(status_code=404, detail="Tópico não encontrado")
    
    # Buscar artigo relevante
    wiki_result = await WikipediaEnricherService.search_article(topic.title)
    
    if wiki_result:
        ref = ExternalReference(
            topic_id=topic_id,
            source="wikipedia",
            title=wiki_result["title"],
            url=wiki_result["url"],
            summary=wiki_result["description"]
        )
        db.add(ref)
        db.commit()
        
        return {"status": "success", "reference": ref}
    
    raise HTTPException(status_code=404, detail="Nenhum artigo encontrado na Wikipedia")
```

#### Benefícios
- 📚 Enriquecimento de conteúdo teórico
- 🔗 Links para referências confiáveis
- 🌐 Múltiplos idiomas suportados
- 📖 Contextualização histórica e conceitual

#### Uso Esperado no Frontend
```
[Tópico] → [Botão "Referências Externas"] → [Abrir artigos Wikipedia]
```

---

### 2️⃣ **Microsoft Graph Education API** - Sincronização de Turmas
**Status: ⭐⭐ RECOMENDADO (médio prazo)**

#### Propósito
Integrar com ecossistema Microsoft 365, permitindo que professores sincronizem turmas e tarefas diretamente do Teams/Education.

#### Como Implementar

**A. Adicionar dependência:**
```bash
pip install msgraph-core azure-identity
```

**B. Criar serviço:**
```python
# backend/app/infrastructure/services/microsoft_graph_service.py

from azure.identity import ClientSecretCredential
from msgraph.core import GraphClient
from typing import List, Optional

class MicrosoftGraphEducationService:
    """Integração com Microsoft Graph Education API"""
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self.credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        self.client = GraphClient(credential=self.credential)
    
    async def get_classes(self) -> List[dict]:
        """Obtém todas as turmas do Microsoft Teams/Education"""
        response = await self.client.get("/education/me/classes")
        return response.get("value", [])
    
    async def sync_class_to_course(self, class_id: str, course_id: str) -> dict:
        """Sincroniza uma turma do Teams como um Curso no Educador"""
        class_data = await self.client.get(f"/education/classes/{class_id}")
        
        # Mapear para estrutura do Educador
        return {
            "external_id": class_id,
            "source": "microsoft_graph",
            "course_id": course_id,
            "display_name": class_data.get("displayName"),
            "description": class_data.get("description")
        }
```

#### Benefícios
- 🏫 Integração com infraestrutura educacional existente
- 👥 Sincronização de alunos e professores
- 📋 Tarefas e avaliações sincronizadas
- 🔐 Autenticação via Azure AD

---

### 3️⃣ **OpenStax/Wikibooks + Web Scraping** - Livros Didáticos Abertos
**Status: ⭐⭐⭐ ALTAMENTE RECOMENDADO**

#### Propósito
Integrar livros didáticos abertos como fonte de teoria estruturada, especialmente para língua portuguesa e disciplinas de concursos.

#### Como Implementar

**A. Adicionar dependência:**
```bash
pip install beautifulsoup4 feedparser
```

**B. Criar serviço:**
```python
# backend/app/infrastructure/services/open_textbook_service.py

import httpx
from bs4 import BeautifulSoup
from typing import Optional, List
import asyncio

class OpenTextbookService:
    """Integração com livros didáticos abertos (OpenStax, Wikibooks, etc)"""
    
    # Mapeamento de fontes de livros
    SOURCES = {
        "openstax": "https://openstax.org/api/books/search?q=",
        "wikibooks": "https://en.wikibooks.org/w/api.php",
    }
    
    @staticmethod
    async def search_textbooks(subject: str, language: str = "pt") -> List[dict]:
        """
        Busca livros didáticos relacionados a um assunto
        
        Args:
            subject: Assunto de busca (ex: "Língua Portuguesa")
            language: Idioma (pt, en, es)
        
        Returns:
            Lista de livros encontrados
        """
        results = []
        
        # Buscar em OpenStax
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{OpenTextbookService.SOURCES['openstax']}{subject}",
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    books = data.get("results", [])[:3]  # Top 3
                    
                    for book in books:
                        results.append({
                            "source": "openstax",
                            "title": book.get("title"),
                            "url": book.get("url"),
                            "authors": book.get("authors", []),
                            "description": book.get("description"),
                            "format": "pdf"
                        })
            except Exception as e:
                print(f"Erro ao buscar OpenStax: {e}")
        
        return results
    
    @staticmethod
    async def extract_chapter(book_url: str, chapter_number: int = 1) -> Optional[str]:
        """Extrai conteúdo de um capítulo específico"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(book_url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extrair seções de capítulo
                    content = soup.find("div", class_="content")
                    return content.get_text() if content else None
        except Exception as e:
            print(f"Erro ao extrair capítulo: {e}")
        
        return None
```

**C. Integração com Topic:**
```python
# Adicionar ao schema de Topic

class TopicResponse(BaseModel):
    id: UUID
    title: str
    theory_markdown: str
    external_textbooks: List[dict] = []  # Novos livros linkados
    
    class Config:
        from_attributes = True
```

#### Benefícios
- 📖 Acesso a livros de qualidade acadêmica reconhecida
- 🆓 Conteúdo livre e aberto
- 🌐 Múltiplas fontes integradas
- 📝 Curadoria de conteúdo de excelência

---

## 📊 Comparativo de Integração

| API | Complexidade | Impacto | Tempo Est. | Prioridade |
|-----|-------------|--------|-----------|-----------|
| **Wikipedia** | ⭐ Baixa | Alto | 2-3 dias | 🔴 P1 |
| **Wikibooks/OpenStax** | ⭐⭐ Média | Altíssimo | 4-5 dias | 🔴 P1 |
| **Microsoft Graph** | ⭐⭐⭐ Alta | Muito Alto | 1-2 semanas | 🟡 P2 |

---

## 🔧 Padrão de Integração Recomendado

Aproveitar a arquitetura existente do projeto:

```
┌─────────────────┐
│   Frontend      │ (Flutter)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Backend API    │ (FastAPI)
├─────────────────┤
│  /api/v1/topics │
│  /api/v1/enrich │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    ▼         ▼        ▼          ▼
┌────────┐┌────────┐┌────────┐┌──────────┐
│  DB    ││ Wiki   ││OpenStax││MsgGraph  │
│(SQLAlch││ API    ││ API    ││  API     │
│emy)   ││        ││        ││          │
└────────┘└────────┘└────────┘└──────────┘
    ↑         ↑        ↑          ↑
    └─────────Service Layer──────┘
              (Dependency Injection)
```

---

## 📝 Plano de Implementação Proposto

### Fase 1: Wikipedia (Sprint de 1 semana) 
```
1. Criar WikipediaEnricherService
2. Adicionar modelo ExternalReference
3. Criar endpoint de enriquecimento
4. Adicionar testes unitários
5. Integrar no Frontend (botão de referências)
```

### Fase 2: Wikibooks/OpenStax (Sprint de 1-2 semanas)
```
1. Criar OpenTextbookService
2. Implementar busca e extração de capítulos
3. Adicionar campo em Topic schema
4. Criar UI para exibir livros recomendados
5. Implementar caching para otimização
```

### Fase 3: Microsoft Graph (Médio prazo)
```
1. Configurar autenticação Azure AD
2. Criar MicrosoftGraphEducationService
3. Implementar sincronização de turmas
4. Mapear estrutura Teams → Educador
5. Testes de integração
```

---

## 🚀 Benefícios Esperados

### Para Alunos
✅ Acesso a múltiplas fontes de conteúdo  
✅ Referências confiáveis e contextualizadas  
✅ Aprendizagem enriquecida e multifacetada  
✅ Links para aprofundamento  

### Para Professores
✅ Curadoria de conteúdo automatizada  
✅ Integração com ferramentas que já usam (Teams)  
✅ Sincronização de turmas simplificada  
✅ Economia de tempo na preparação  

### Para o Projeto
✅ Escalabilidade de conteúdo sem duplicação  
✅ Manutenção reduzida (conteúdo sempre atualizado)  
✅ Diferenciais competitivos claros  
✅ Conformidade com OER (Open Educational Resources)  

---

## ⚠️ Considerações Técnicas

### Tratamento de Erros
```python
# Padrão para todas as integrações
try:
    result = await external_service.fetch()
except httpx.TimeoutError:
    # Fallback para cache local
    return cached_result
except httpx.HTTPError as e:
    logger.error(f"Erro na integração: {e}")
    return {"status": "warning", "message": "Conteúdo externo indisponível"}
```

### Caching e Performance
```python
from datetime import timedelta
import hashlib

class CachedExternalService:
    CACHE_TTL = timedelta(days=7)  # Atualizar semanal
    
    @staticmethod
    def get_cache_key(query: str) -> str:
        return f"ext:{hashlib.md5(query.encode()).hexdigest()}"
```

### Rate Limiting
- Wikipedia API: Sem limite (header: User-Agent obrigatório)
- OpenStax: Respeitar documentação (típ. 100 req/min)
- Microsoft Graph: 2000 req/min (padrão)

---

## 📚 Referências Técnicas

### Documentação das APIs
- [Wikimedia REST API](https://developer.wikimedia.org/pt-br/build-tools/apis/)
- [OpenStax API](https://openstax.org/api)
- [Microsoft Graph Education](https://docs.microsoft.com/graph/education-concept-overview)

### Bibliotecas Python Recomendadas
```txt
httpx>=0.24.0          # HTTP Assincronismo
beautifulsoup4>=4.12   # Web scraping
feedparser>=6.0        # Feeds RSS/Atom
redis>=4.5             # Caching distribuído (opcional)
aiohttp>=3.8           # Alternativa httpx
```

---

## 🎬 Próximos Passos

1. **Validação**: Revisar propostas com time de desenvolvimento
2. **Prototipagem**: Iniciar Fase 1 (Wikipedia) como MVP
3. **Teste de Carga**: Validar performance com dados reais
4. **Feedback**: Coletar insights de usuários (alunos/professores)
5. **Roadmap**: Priorizar Fases 2 e 3 conforme feedback

---

## 📞 Suporte e Dúvidas

Para dúvidas sobre implementação específica de qualquer API:
- Consultar documentação oficial das APIs
- Revisar testes de integração em `/backend/tests/`
- Validar headers e rate limiting conforme necessário

---

**Data da Análise**: Julho de 2026  
**Versão do Projeto Analisado**: Última commit no repositório  
**Recomendação Geral**: ✅ VIÁVEL E ALTAMENTE BENÉFICA
