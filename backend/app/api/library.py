from fastapi import APIRouter

router = APIRouter(prefix="/library", tags=["Library"])

@router.get("/classics")
def get_classic_books():
    return [
        {
            "id": "1",
            "title": "Dom Casmurro",
            "author": "Machado de Assis",
            "year": 1899,
            "description": "Uma das obras mais célebres da literatura brasileira. Apresenta o dilema da traição (ou não) de Capitu sob a ótica ciumenta de Bentinho.",
            "download_url": "https://www.dominiopublico.gov.br/download/texto/ua000194.pdf",
            "cover_color": "0xFF2C3E50"
        },
        {
            "id": "2",
            "title": "Memórias Póstumas de Brás Cubas",
            "author": "Machado de Assis",
            "year": 1881,
            "description": "Narrado por um defunto-autor, a obra inaugura o realismo no Brasil com ironia, ceticismo e análises profundas da sociedade da época.",
            "download_url": "https://www.dominiopublico.gov.br/download/texto/ua000289.pdf",
            "cover_color": "0xFF8E44AD"
        },
        {
            "id": "3",
            "title": "Iracema",
            "author": "José de Alencar",
            "year": 1865,
            "description": "Clássico do romantismo indianista, narra o amor trágico entre a 'virgem dos lábios de mel' Iracema e o guerreiro colonizador português Martim.",
            "download_url": "https://www.dominiopublico.gov.br/download/texto/bn000037.pdf",
            "cover_color": "0xFFD35400"
        },
        {
            "id": "4",
            "title": "O Cortiço",
            "author": "Aluísio Azevedo",
            "year": 1890,
            "description": "Grande expoente do naturalismo brasileiro, a obra foca na vida e nas mazelas de moradores de uma habitação coletiva no Rio de Janeiro.",
            "download_url": "https://www.dominiopublico.gov.br/download/texto/ua000004.pdf",
            "cover_color": "0xFF16A085"
        },
        {
            "id": "5",
            "title": "Triste Fim de Policarpo Quaresma",
            "author": "Lima Barreto",
            "year": 1911,
            "description": "Uma sátira genial sobre o nacionalismo ingênuo de Policarpo Quaresma, que propõe o tupi-guarani como idioma oficial do Brasil.",
            "download_url": "https://www.dominiopublico.gov.br/download/texto/bn000109.pdf",
            "cover_color": "0xFF2980B9"
        }
    ]
