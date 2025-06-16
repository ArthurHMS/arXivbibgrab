import requests
import feedparser
import time

def buscar_arxiv_bibtex(query, max_results=10, arquivo="arxiv_api_results.bib"):
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao conectar com a API do arXiv: {e}")
        return 0

    feed = feedparser.parse(response.text)
    total_entradas = len(feed.entries)
    print(f"🔍 Query '{query}' retornou {total_entradas} resultados.")

    if total_entradas == 0:
        return 0

    bib_entries = []
    for entry in feed.entries:
        arxiv_id = entry.id.split('/abs/')[-1]
        title = entry.title.replace('\n', ' ').strip()
        authors = " and ".join(author.name for author in entry.authors)
        year = entry.published[:4]

        bib = f"""@article{{{arxiv_id},
  title={{ {title} }},
  author={{ {authors} }},
  journal={{arXiv preprint arXiv:{arxiv_id}}},
  year={{ {year} }}
}}"""
        bib_entries.append(bib)

    # Abre o arquivo no modo append para não sobrescrever resultados anteriores
    with open(arquivo, "a", encoding="utf-8") as f:
        f.write("\n\n".join(bib_entries) + "\n\n")

    print(f"✅ {total_entradas} entradas BibTeX adicionadas em '{arquivo}'.")
    return total_entradas

if __name__ == "__main__":
    # Lista de queries simples para buscar em sequência
    queries = [
        'all:"myocardial infarction"',
        'all:"heart attack"',
        'all:"network science"',
        'all:"complex network"',
        'all:"network analysis"',
        'all:"graph theory"'
    ]

    arquivo_saida = "arxiv_api_results.bib"

    # Apaga arquivo anterior para começar do zero
    open(arquivo_saida, "w", encoding="utf-8").close()

    total_geral = 0
    for q in queries:
        total = buscar_arxiv_bibtex(q, max_results=10, arquivo=arquivo_saida)
        total_geral += total
        time.sleep(3)  # pausa para evitar bloqueio por excesso de requisições

    print(f"\n🎉 Busca finalizada. Total de entradas salvas: {total_geral}")
