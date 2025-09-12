#!/usr/bin/env python3
"""
Script pour charger les données spécifiques de Formeduc dans ChromaDB
Basé sur le contenu du site https://www.formeduc.ca/
"""

import sys
import os
import json
from typing import List, Dict

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chroma_client import index_documents, get_chroma_client

def get_formeduc_data() -> List[Dict[str, str]]:
    """Retourne les données structurées de Formeduc"""
    
    data = [
        {
            "title": "Formeduc - Formations en secourisme et garderie",
            "content": """
Formeduc est une institution spécialisée dans la formation en secourisme et les services de garde éducatifs.

ADRESSE: 5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101
TÉLÉPHONE: 418 842-7523
EMAIL: info@formeduc.ca

MISSION: Offrir des formations de qualité en secourisme adaptées à la petite enfance et au milieu scolaire, 
ainsi que des cours de perfectionnement pour les responsables de service de garde (RSG et RSGE) et 
les éducateurs en petite enfance.

CERTIFICATIONS: Toutes nos formations sont conformes au Règlement sur les services de garde éducatifs 
en milieu scolaire et à la Loi sur l'instruction publique (chapitre l-13.3, a. 454.1).
            """,
            "category": "institution"
        },
        {
            "title": "Secourisme service de garde - Formations disponibles",
            "content": """
FORMATIONS EN SECOURISME POUR SERVICE DE GARDE:

1. Secourisme adapté à la petite enfance en ligne (8 heures)
   - Formation complète pour les éducatrices et éducateurs
   - Certificat conforme aux réglementations
   - Formation 100% en ligne

2. Renouvellement de secourisme adapté à la petite enfance en ligne (6 heures)
   - Pour le renouvellement de certification
   - Mise à jour des connaissances
   - Formation en ligne flexible

3. Secourisme en milieu scolaire en ligne
   - Spécialement conçu pour le personnel scolaire
   - Adaptation aux situations d'urgence en milieu scolaire
   - Formation certifiante

4. Renouvellement de secourisme en milieu scolaire en ligne (6 heures)
   - Renouvellement de certification
   - Mise à jour des protocoles
   - Formation continue

5. Secourisme adapté enfants d'âges scolaire pour chauffeur d'autobus (8 heures)
   - Formation spécialisée pour les chauffeurs
   - Gestion des urgences en transport scolaire
   - Protocoles spécifiques

6. Trousse de premiers soins pour garderie
   - Équipement et matériel de premiers soins
   - Guide d'utilisation
   - Conformité réglementaire
            """,
            "category": "secourisme"
        },
        {
            "title": "Formations garderie - Programme 45 heures",
            "content": """
PROGRAMME DE 45 HEURES POUR RSG (RESPONSABLE DE SERVICE DE GARDE):

1. Le programme éducatif en service de garde
   - Développement et mise en œuvre du programme éducatif
   - Planification des activités
   - Évaluation des apprentissages

2. Le développement de l'enfant
   - Étapes du développement de 0 à 12 ans
   - Besoins spécifiques selon l'âge
   - Observation et évaluation

3. Santé, sécurité et alimentation
   - Protocoles de sécurité
   - Nutrition adaptée à l'âge
   - Prévention des accidents
   - Gestion des allergies

4. Le rôle de la responsable d'un service de garde
   - Responsabilités légales et éthiques
   - Communication avec les parents
   - Gestion administrative
   - Partenariat avec les familles

DÉVELOPPEMENT DE L'ENFANT:
- Le développement de l'enfant (formation complète)
- Le développement de l'enfant assistant/remplaçant
            """,
            "category": "garderie"
        },
        {
            "title": "Cours de perfectionnement - Thématiques disponibles",
            "content": """
COURS DE PERFECTIONNEMENT POUR ÉDUCATEURS:

1. Accueillir l'enfant et sa diversité culturelle
   - Inclusion et diversité
   - Adaptation des pratiques éducatives
   - Sensibilisation culturelle

2. Allergies? Je réagis!
   - Identification des allergies
   - Protocoles d'urgence
   - Prévention et gestion

3. Bien dormir pour bien grandir
   - Rythmes de sommeil selon l'âge
   - Aménagement des espaces de repos
   - Troubles du sommeil

4. Briser la chaîne infectieuse
   - Prévention des infections
   - Hygiène et désinfection
   - Protocoles sanitaires

5. Cultiver l'intelligence émotionnelle de l'enfant
   - Développement émotionnel
   - Gestion des émotions
   - Techniques d'accompagnement

6. De A à Z… 26 techniques d'intervention
   - Stratégies d'intervention éducative
   - Gestion des comportements
   - Techniques de communication

7. Exclusion en cas de maladie, aide à la décision
   - Critères d'exclusion
   - Protocoles de retour
   - Communication avec les parents

8. L'animation par thématique
   - Planification d'activités thématiques
   - Adaptation selon l'âge
   - Évaluation des apprentissages

9. La maltraitance, intervenir pour protéger l'enfant
   - Identification des signes
   - Protocoles d'intervention
   - Signalement et suivi

10. Le développement langagier, acquisition et dépistage
    - Étapes du développement du langage
    - Techniques de stimulation
    - Dépistage précoce

11. Le grand défi du multi-âge
    - Gestion des groupes multi-âges
    - Adaptation des activités
    - Défis et opportunités

12. Le jeu libre, essentiel aux apprentissages
    - Importance du jeu libre
    - Aménagement des espaces
    - Rôle de l'éducateur

13. Le syndrome du bébé secoué
    - Prévention et sensibilisation
    - Signes d'alerte
    - Éducation des parents

14. Ma garderie est verte!
    - Éducation environnementale
    - Pratiques écologiques
    - Sensibilisation des enfants

15. Mise à jour du programme éducatif
    - Évolution des pratiques
    - Nouvelles approches
    - Intégration des changements

16. Miser sur l'éducatrice
    - Développement professionnel
    - Bien-être au travail
    - Motivation et engagement

17. Papa, maman… votre enfant m'inquiète!
    - Communication avec les parents
    - Gestion des inquiétudes
    - Collaboration famille-garderie

18. Préparer l'enfant à la maternelle
    - Transition vers l'école
    - Compétences préscolaires
    - Collaboration école-garderie

19. Préparer le dossier éducatif de l'enfant
    - Documentation des observations
    - Évaluation continue
    - Communication avec les parents

20. Verbal, gestuel ou artistique? L'enfant vous parle!
    - Communication non verbale
    - Expression artistique
    - Observation et interprétation
            """,
            "category": "perfectionnement"
        },
        {
            "title": "Familles d'accueil - Formations spécialisées",
            "content": """
FORMATIONS SPÉCIALISÉES POUR FAMILLES D'ACCUEIL:

1. Formation Hybride en secourisme pour les Familles d'Accueil
   - Formation combinée en ligne et en présentiel
   - Adaptation aux besoins spécifiques
   - Certification complète

2. Spécial Famille d'accueil: Allergies? Je réagis!
   - Gestion des allergies en famille d'accueil
   - Protocoles d'urgence adaptés
   - Communication avec les services sociaux

3. Spécial Famille d'accueil: Bien dormir pour bien grandir
   - Rythmes de sommeil en famille d'accueil
   - Adaptation aux nouveaux environnements
   - Gestion des troubles du sommeil

4. Spécial Famille d'accueil: Briser la chaîne infectieuse
   - Prévention en milieu familial
   - Protocoles sanitaires adaptés
   - Protection de tous les enfants

5. Spécial Famille d'accueil: Cultiver l'intelligence émotionnelle
   - Accompagnement émotionnel spécialisé
   - Gestion des traumatismes
   - Techniques de réparation

6. Spécial Famille d'accueil: Développement de l'enfant
   - Développement en contexte d'accueil
   - Adaptation aux changements
   - Observation et évaluation

7. Spécial Famille d'accueil: Développement langagier
   - Stimulation du langage en accueil
   - Gestion des retards de développement
   - Techniques d'intervention

8. Spécial Famille d'accueil: Le syndrome du bébé secoué
   - Prévention spécialisée
   - Éducation et sensibilisation
   - Protocoles d'intervention

9. Spécial Famille d'accueil: Verbal, gestuel ou artistique
   - Communication en contexte d'accueil
   - Expression des émotions
   - Techniques d'observation
            """,
            "category": "famille_accueil"
        },
        {
            "title": "Programmes jeunesse - Formations pour jeunes",
            "content": """
PROGRAMMES SPÉCIALISÉS POUR LES JEUNES:

1. Cours de gardien futé et averti en ligne
   - Formation pour adolescents
   - Compétences de gardiennage
   - Sécurité et responsabilité

2. Futé: Je suis prêt à rester seul
   - Préparation à l'autonomie
   - Sécurité à la maison
   - Gestion des situations d'urgence

3. Formation en secourisme pour animateur de camp de jour et moniteur de camp de vacances
   - Secourisme adapté aux activités de plein air
   - Gestion des urgences en camp
   - Protocoles spécifiques aux activités
            """,
            "category": "jeunesse"
        },
        {
            "title": "Formations en anglais - English courses",
            "content": """
ENGLISH COURSES AVAILABLE:

CHILDCARE FIRST AID TRAINING:
1. First Aid Adapted for Childhood (8 hour)
2. First Aid Adapted for Early Childhood (6 hour)
3. First Aid in School Setting (8 hours)
4. Online renewal of first aid in a school setting (6 hours)

45-HOUR TRAINING FOR CHILDCARE:
1. Child development
2. Educational program
3. Safety, health and nutrition
4. The role of the home childcare provider

PROFESSIONAL DEVELOPMENT:
1. Abuse: intervening to protect the child
2. Allergies? I react!
3. Breaking the chain of infection
4. Dad, Mom… your child worries me!
5. Detection and prevention of sexual abuse in children
6. Exclusion in case of illness: decision support
7. Focus on educators
8. Free play, essential to learning
9. From A to Z… 26 intervention techniques
10. My daycare is green!
11. Preparing the child for kindergarten
12. Preparing the child's educational file
13. Shaken baby syndrome: Educators, stay alert!
14. Sleep well to grow well
15. The great challenge of multi-age groups
16. Thematic animation
17. Update of the educational program
18. Verbal, gestural, or artistic, the child is speaking to you!
19. Welcoming the child and their cultural diversity
            """,
            "category": "english"
        },
        {
            "title": "Avantages des formations Formeduc",
            "content": """
AVANTAGES DES FORMATIONS FORMEDUC:

1. FORMATIONS 100% EN LIGNE
   - Accès où que vous soyez, à tout moment
   - Flexibilité des horaires
   - Apprentissage à votre rythme

2. EXPERTS DU TERRAIN
   - Formateurs passionnés avec expérience pratique
   - Connaissance approfondie du milieu
   - Approche pédagogique adaptée

3. CERTIFICATIONS RECONNUES
   - Attestations professionnelles valorisantes
   - Conformité aux réglementations
   - Reconnaissance par les employeurs

4. CONTENU ADAPTÉ
   - Spécialement conçu pour les éducateurs
   - Approche pratique et concrète
   - Mise à jour régulière du contenu

5. SUPPORT TECHNIQUE
   - Assistance technique disponible
   - Plateforme intuitive
   - Ressources d'aide complètes

6. PRIX COMPÉTITIFS
   - Tarifs abordables
   - Formations de qualité
   - Excellent rapport qualité-prix
            """,
            "category": "avantages"
        }
    ]
    
    return data

def main():
    """Fonction principale pour charger les données Formeduc"""
    print("🚀 Chargement des données Formeduc dans ChromaDB")
    
    # Récupérer les données
    formeduc_data = get_formeduc_data()
    
    # Préparer les documents pour ChromaDB
    documents = []
    for item in formeduc_data:
        doc = f"""
Titre: {item['title']}
Catégorie: {item['category']}

Contenu:
{item['content']}

---
Source: Site officiel Formeduc.ca
Institution: Formeduc
Adresse: 5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101
Téléphone: 418 842-7523
Email: info@formeduc.ca
"""
        documents.append(doc.strip())
    
    # Indexer dans ChromaDB
    print("🔄 Indexation dans ChromaDB...")
    try:
        # Initialiser ChromaDB
        chroma_client = get_chroma_client()
        
        # Indexer les documents
        ids = index_documents(documents)
        
        print(f"✅ {len(ids)} documents Formeduc indexés dans ChromaDB")
        
        # Sauvegarder les métadonnées
        metadata = {
            'loaded_at': '2025-01-12',
            'total_documents': len(documents),
            'source': 'formeduc.ca',
            'categories': list(set(item['category'] for item in formeduc_data))
        }
        
        with open('/app/formeduc_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print("✅ Métadonnées sauvegardées")
        print("🎉 Chargement des données Formeduc terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation: {e}")

if __name__ == "__main__":
    main()
