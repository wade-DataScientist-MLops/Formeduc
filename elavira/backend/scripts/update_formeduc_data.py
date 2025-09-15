#!/usr/bin/env python3
"""
Script pour mettre à jour les données Formeduc avec les vraies informations du site
"""

import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chroma_client import index_documents, get_chroma_client

def get_updated_formeduc_knowledge_base():
    """Base de connaissances Formeduc mise à jour avec les vraies informations du site"""
    
    knowledge_base = [
        {
            "title": "Formeduc - Institution de formation professionnelle",
            "content": """
Formeduc est une institution spécialisée dans la formation en secourisme et les services de garde éducatifs au Québec.

COORDONNÉES:
- Adresse: 5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101
- Téléphone: 418 842-7523
- Email: info@formeduc.ca
- Site web: https://www.formeduc.ca/

MISSION: Offrir des formations de qualité en secourisme adaptées à la petite enfance et au milieu scolaire, 
ainsi que des cours de perfectionnement pour les responsables de service de garde (RSG et RSGE) et 
les éducateurs en petite enfance.

CERTIFICATIONS: Toutes nos formations sont conformes au Règlement sur les services de garde éducatifs 
en milieu scolaire et à la Loi sur l'instruction publique (chapitre l-13.3, a. 454.1).

AVANTAGES:
- Formations 100% en ligne
- Experts du terrain avec expérience pratique
- Certifications reconnues
- Contenu adapté aux professionnels
- Support technique disponible
- Accès 24h/24
            """,
            "category": "institution"
        },
        {
            "title": "Secourisme service de garde - Formations disponibles",
            "content": """
FORMATIONS EN SECOURISME POUR SERVICE DE GARDE:

1. SECOURISME ADAPTÉ À LA PETITE ENFANCE:
   - Secourisme adapté à la petite enfance en ligne, 8 heures
   - Renouvellement de secourisme adapté à la petite enfance en ligne, 6 heures

2. SECOURISME EN MILIEU SCOLAIRE:
   - Secourisme en milieu scolaire en ligne
   - Renouvellement de secourisme en milieu scolaire en ligne, 6 heures

3. SECOURISME POUR CHAUFFEUR D'AUTOBUS:
   - Secourisme adapté enfants d'âges scolaire pour chauffeur d'autobus, 8 heures

4. TROUSSE DE PREMIERS SOINS:
   - Trousse de premiers soins pour garderie

Toutes ces formations sont développées spécifiquement pour les éducatrices et éducateurs en service de garde 
en milieu familial, dans les centres à la petite enfance (CPE) ou en milieu scolaire.
            """,
            "category": "secourisme"
        },
        {
            "title": "Formations garderie - Programme 45 heures",
            "content": """
FORMATIONS GARDERIE - PROGRAMME DE 45 HEURES:

MODULES OBLIGATOIRES:
1. Le programme éducatif en service de garde
2. Le développement de l'enfant
3. Santé, sécurité et alimentation
4. Le rôle de la responsable d'un service de garde

DÉVELOPPEMENT DE L'ENFANT:
- Le développement de l'enfant
- Le développement de l'enfant assistant / remplaçant

Ces formations sont obligatoires pour les RSG (Responsables de Service de Garde) et RSGE 
(Responsables de Service de Garde Éducatif).
            """,
            "category": "formations_garderie"
        },
        {
            "title": "Cours de perfectionnement - Formations spécialisées",
            "content": """
COURS DE PERFECTIONNEMENT POUR PROFESSIONNELS:

1. DIVERSITÉ ET INCLUSION:
   - Accueillir l'enfant et sa diversité culturelle

2. SANTÉ ET SÉCURITÉ:
   - Allergies? Je réagis!
   - Bien dormir pour bien grandir
   - Briser la chaîne infectieuse
   - Exclusion en cas de maladie, aide à la décision
   - Le syndrome du bébé secoué

3. DÉVELOPPEMENT DE L'ENFANT:
   - Cultiver l'intelligence émotionnelle de l'enfant
   - Le développement langagier, acquisition et dépistage
   - Le grand défi du multi-âge
   - Le jeu libre, essentiel aux apprentissages

4. INTERVENTION ET PROTECTION:
   - De A à Z… 26 techniques d'intervention
   - La maltraitance, intervenir pour protéger l'enfant
   - Papa, maman… votre enfant m'inquiète!

5. PÉDAGOGIE ET ANIMATION:
   - L'animation par thématique
   - Miser sur l'éducatrice
   - Verbal, gestuel ou artistique? L'enfant vous parle!

6. ENVIRONNEMENT ET DÉVELOPPEMENT DURABLE:
   - Ma garderie est verte!

7. MISE À JOUR ET PRÉPARATION:
   - Mise à jour du programme éducatif
   - Préparer l'enfant à la maternelle
   - Préparer le dossier éducatif de l'enfant
            """,
            "category": "perfectionnement"
        },
        {
            "title": "Familles d'accueil - Formations spécialisées",
            "content": """
FORMATIONS POUR FAMILLES D'ACCUEIL:

FORMATIONS HYBRIDES:
- Formation Hybride en secourisme pour les Familles d'Accueil

FORMATIONS SPÉCIALISÉES FAMILLE D'ACCUEIL:
- Spécial Famille d'accueil : Allergies ? Je réagis !
- Spécial Famille d'accueil : Bien dormir pour bien grandir
- Spécial Famille d'accueil : Briser la chaîne infectieuse
- Spécial Famille d'accueil : Cultiver l'intelligence émotionnelle de l'enfant
- Spécial Famille d'accueil : Développement de l'enfant
- Spécial Famille d'accueil : Développement langagier, acquisition et dépistage
- Spécial Famille d'accueil : Le syndrome du bébé secoué
- Spécial Famille d'accueil : Verbal, gestuel ou artistique, l'enfant vous parle!

PARTENARIAT CIUSSS-CN:
Formeduc collabore avec le CIUSSS-CN (Centre Intégré Universitaire de Santé et de Services Sociaux 
de la Capitale-Nationale) pour offrir des formations spécialisées aux familles d'accueil.
            """,
            "category": "familles_accueil"
        },
        {
            "title": "Programme jeunesse - Formations pour jeunes",
            "content": """
PROGRAMME JEUNESSE - FORMATIONS POUR ADOLESCENTS ET JEUNES:

1. GARDIEN FUTÉ ET AVERTI:
   - Cours de gardien futé et averti en ligne
   - Futé : Je suis prêt à rester seul

2. SECOURISME POUR ANIMATEURS:
   - Formation en secourisme pour animateur de camp de jour et moniteur de camp de vacances

Ces formations sont conçues spécialement pour les jeunes qui souhaitent:
- Apprendre les premiers soins
- Devenir des gardiens responsables
- Acquérir des compétences en animation
- Développer leur sens des responsabilités
            """,
            "category": "jeunesse"
        },
        {
            "title": "Formations en anglais - English courses",
            "content": """
ENGLISH COURSES - FORMATIONS EN ANGLAIS:

1. CHILDCARE FIRST AID TRAINING:
   - First Aid Adapted for Childhood, 8 hour
   - First Aid Adapted for Early Childhood, 6 hour
   - First Aid in School Setting, 8 hours
   - Online renewal of first aid in a school setting, 6 hours

2. 45-HOUR TRAINING FOR CHILDCARE:
   - Child development
   - Educational program
   - Safety, health and nutrition
   - The role of the home childcare provider

3. PROFESSIONAL DEVELOPMENT:
   - Abuse: intervening to protect the child
   - Allergies? I react!
   - Breaking the chain of infection
   - Dad, Mom… your child worries me!
   - Detection and prevention of sexual abuse in children
   - Exclusion in case of illness: decision support
   - Focus on educators
   - Free play, essential to learning
   - From A to Z… 26 intervention techniques
   - My daycare is green!
   - Preparing the child for kindergarten
   - Preparing the child's educational file
   - Shaken baby syndrome: Educators, stay alert!
   - Sleep well to grow well
   - The great challenge of multi-age groups
   - Thematic animation
   - Update of the educational program
   - Verbal, gestural, or artistic, the child is speaking to you!
   - Welcoming the child and their cultural diversity
            """,
            "category": "english_courses"
        },
        {
            "title": "Avantages des formations Formeduc",
            "content": """
AVANTAGES DES FORMATIONS FORMEDUC:

1. FORMATIONS 100% EN LIGNE:
   - Accédez à vos cours où que vous soyez, à tout moment
   - Flexibilité totale dans votre apprentissage
   - Pas de déplacement nécessaire

2. EXPERTS DU TERRAIN:
   - Des formateurs passionnés avec une vraie expérience pratique
   - Connaissance approfondie du milieu de la petite enfance
   - Expertise reconnue dans le domaine

3. CERTIFICATIONS RECONNUES:
   - Valorisez vos compétences avec des attestations professionnelles
   - Conformes aux réglementations québécoises
   - Reconnaissance par les employeurs

4. SUPPORT ET ACCOMPAGNEMENT:
   - Support technique disponible
   - Accompagnement personnalisé
   - Réponses rapides à vos questions

5. PRIX COMPÉTITIFS:
   - Tarifs abordables pour tous les budgets
   - Formations de qualité à prix raisonnable
   - Meilleur rapport qualité-prix du marché
            """,
            "category": "avantages"
        },
        {
            "title": "Processus d'inscription et contact",
            "content": """
PROCESSUS D'INSCRIPTION ET CONTACT:

COMMENT S'INSCRIRE:
1. Visitez notre site web: https://www.formeduc.ca/
2. Parcourez nos formations disponibles
3. Choisissez la formation adaptée à votre profil
4. Inscrivez-vous en ligne
5. Accédez immédiatement à votre formation

CONTACT:
- Téléphone: 418 842-7523
- Email: info@formeduc.ca
- Adresse: 5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101

HEURES D'OUVERTURE:
- Support technique disponible en ligne 24h/24
- Service client du lundi au vendredi

INSCRIPTION:
- Processus simple et rapide
- Paiement sécurisé
- Accès immédiat après inscription
- Certificat délivré à la fin de la formation
            """,
            "category": "inscription"
        }
    ]
    
    return knowledge_base

def main():
    """Fonction principale pour charger les données mises à jour"""
    print("🚀 Mise à jour de la base de connaissances Formeduc avec les vraies informations du site")
    
    # Obtenir la base de connaissances mise à jour
    knowledge_base = get_updated_formeduc_knowledge_base()
    
    # Obtenir le client ChromaDB
    client = get_chroma_client()
    
    # Indexer les documents
    try:
        # Extraire les textes et métadonnées
        texts = []
        metadatas = []
        ids = []
        
        for i, doc in enumerate(knowledge_base):
            texts.append(f"{doc['title']}\n\n{doc['content']}")
            metadatas.append({
                "source": "formeduc_site",
                "category": doc["category"],
                "title": doc["title"]
            })
            ids.append(f"formeduc_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        # Utiliser la fonction index_documents existante
        from core.chroma_client import collection, embedder
        embeddings = embedder.encode(texts).tolist()
        collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)
        print("✅ Base de connaissances Formeduc mise à jour avec succès!")
        
        # Afficher un résumé
        print(f"\n📊 Résumé de la mise à jour:")
        print(f"- Nombre total de documents: {len(knowledge_base)}")
        print(f"- Collection: elavira_collection")
        print(f"- Date de mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Afficher les catégories
        categories = set(doc["category"] for doc in knowledge_base)
        print(f"- Catégories disponibles: {', '.join(sorted(categories))}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Mise à jour terminée avec succès!")
        print("Elavira peut maintenant répondre avec les vraies informations du site FormEduc.ca")
    else:
        print("\n💥 Échec de la mise à jour")
        sys.exit(1)
