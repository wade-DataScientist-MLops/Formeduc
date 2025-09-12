#!/usr/bin/env python3
"""
Script pour extraire et indexer le contenu du site Formeduc.ca dans ChromaDB
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from typing import List, Dict
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chroma_client import index_documents, get_chroma_client

class FormeducScraper:
    def __init__(self):
        self.base_url = "https://www.formeduc.ca"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_content = []
        
    def scrape_page(self, url: str) -> Dict[str, str]:
        """Scrape une page et extrait le contenu pertinent"""
        try:
            print(f"🔄 Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire le titre principal
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else "Formeduc - Formation en secourisme"
            
            # Extraire le contenu principal
            content_parts = []
            
            # Extraire les sections principales
            sections = soup.find_all(['h2', 'h3', 'h4', 'p', 'li'])
            
            for section in sections:
                text = section.get_text().strip()
                if text and len(text) > 10:  # Filtrer les textes trop courts
                    content_parts.append(text)
            
            # Extraire les liens de navigation
            nav_links = soup.find_all('a', href=True)
            for link in nav_links:
                link_text = link.get_text().strip()
                if link_text and len(link_text) > 3:
                    content_parts.append(f"Lien: {link_text}")
            
            content = " ".join(content_parts)
            
            return {
                'url': url,
                'title': title_text,
                'content': content,
                'word_count': len(content.split())
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du scraping de {url}: {e}")
            return None
    
    def get_all_pages(self) -> List[str]:
        """Récupère toutes les URLs à scraper"""
        try:
            print("🔄 Récupération de la page d'accueil...")
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            urls = set([self.base_url])  # Commencer par la page d'accueil
            
            # Extraire tous les liens internes
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    full_url = self.base_url + href
                    urls.add(full_url)
                elif href.startswith(self.base_url):
                    urls.add(href)
            
            return list(urls)
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des URLs: {e}")
            return [self.base_url]
    
    def scrape_all(self) -> List[Dict[str, str]]:
        """Scrape toutes les pages du site"""
        urls = self.get_all_pages()
        print(f"📄 {len(urls)} pages à scraper")
        
        scraped_data = []
        
        for i, url in enumerate(urls[:20]):  # Limiter à 20 pages pour commencer
            print(f"📄 Page {i+1}/{min(20, len(urls))}")
            
            page_data = self.scrape_page(url)
            if page_data and page_data['word_count'] > 50:  # Filtrer les pages avec peu de contenu
                scraped_data.append(page_data)
                print(f"✅ {page_data['title'][:50]}... ({page_data['word_count']} mots)")
            
            time.sleep(1)  # Pause entre les requêtes pour être respectueux
        
        return scraped_data
    
    def prepare_documents_for_chroma(self, scraped_data: List[Dict[str, str]]) -> List[str]:
        """Prépare les données scrapées pour l'indexation dans ChromaDB"""
        documents = []
        
        for page in scraped_data:
            # Créer un document structuré
            doc = f"""
Titre: {page['title']}
URL: {page['url']}

Contenu:
{page['content']}

---
Ce contenu provient du site officiel Formeduc.ca et concerne les formations en secourisme, 
les services de garde, et l'éducation à la petite enfance.
"""
            documents.append(doc.strip())
        
        return documents

def main():
    """Fonction principale"""
    print("🚀 Début du scraping de Formeduc.ca")
    
    # Initialiser le scraper
    scraper = FormeducScraper()
    
    # Scraper le site
    scraped_data = scraper.scrape_all()
    
    if not scraped_data:
        print("❌ Aucune donnée récupérée")
        return
    
    print(f"✅ {len(scraped_data)} pages scrapées avec succès")
    
    # Préparer les documents pour ChromaDB
    documents = scraper.prepare_documents_for_chroma(scraped_data)
    
    # Indexer dans ChromaDB
    print("🔄 Indexation dans ChromaDB...")
    try:
        # Initialiser ChromaDB
        chroma_client = get_chroma_client()
        
        # Indexer les documents
        ids = index_documents(documents)
        
        print(f"✅ {len(ids)} documents indexés dans ChromaDB")
        
        # Sauvegarder les métadonnées
        metadata = {
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_pages': len(scraped_data),
            'total_documents': len(documents),
            'source': 'formeduc.ca'
        }
        
        with open('/app/formeduc_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print("✅ Métadonnées sauvegardées")
        print("🎉 Scraping et indexation terminés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation: {e}")

if __name__ == "__main__":
    main()
