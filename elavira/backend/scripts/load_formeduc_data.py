#!/usr/bin/env python3
"""
Script pour charger les données Formeduc dans ChromaDB pour Elavira
"""

import sys
import os
import json
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.chroma_client import index_documents, get_chroma_client

def get_formeduc_knowledge_base():
    """Base de connaissances Formeduc pour Elavira"""
    
    knowledge_base = [
        {
            "title": "Formeduc - Institution de formation",
            "content": """
Formeduc est une institution spécialisée dans la formation en secourisme et les services de garde éducatifs.

COORDONNÉES:
- Adresse: 5121 ave Chauveau Ouest, Québec, QC G2E 5A6 local 101
- Téléphone: 418 842-7523
- Email: info@formeduc.ca

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
- Prix compétitifs
            """,
            "category": "institution"
        },
        {
            "title": "Secourisme service de garde - Formations disponibles",
            "content": """
FORMATIONS EN SECOURISME POUR SERVICE DE GARDE:

1. SECOURISME ADAPTÉ À LA PETITE ENFANCE EN LIGNE (8 heures)
   - Formation complète pour les éducatrices et éducateurs
   - Certificat conforme aux réglementations
   - Formation 100% en ligne
   - Accès flexible 24h/24

2. RENOUVELLEMENT DE SECOURISME ADAPTÉ À LA PETITE ENFANCE EN LIGNE (6 heures)
   - Pour le renouvellement de certification
   - Mise à jour des connaissances
   - Formation en ligne flexible
   - Contenu actualisé

3. SECOURISME EN MILIEU SCOLAIRE EN LIGNE
   - Spécialement conçu pour le personnel scolaire
   - Adaptation aux situations d'urgence en milieu scolaire
   - Formation certifiante
   - Protocoles spécifiques

4. RENOUVELLEMENT DE SECOURISME EN MILIEU SCOLAIRE EN LIGNE (6 heures)
   - Renouvellement de certification
   - Mise à jour des protocoles
   - Formation continue
   - Contenu actualisé

5. SECOURISME ADAPTÉ ENFANTS D'ÂGES SCOLAIRE POUR CHAUFFEUR D'AUTOBUS (8 heures)
   - Formation spécialisée pour les chauffeurs
   - Gestion des urgences en transport scolaire
   - Protocoles spécifiques
   - Certification valide

6. TROUSSE DE PREMIERS SOINS POUR GARDERIE
   - Équipement et matériel de premiers soins
   - Guide d'utilisation complet
   - Conformité réglementaire
   - Formation à l'utilisation
            """,
            "category": "secourisme"
        },
        {
            "title": "Formations garderie - Programme 45 heures",
            "content": """
PROGRAMME DE 45 HEURES POUR RSG (RESPONSABLE DE SERVICE DE GARDE):

MODULE 1: LE PROGRAMME ÉDUCATIF EN SERVICE DE GARDE
- Développement et mise en œuvre du programme éducatif
- Planification des activités selon l'âge
- Évaluation des apprentissages
- Adaptation aux besoins individuels

MODULE 2: LE DÉVELOPPEMENT DE L'ENFANT
- Étapes du développement de 0 à 12 ans
- Besoins spécifiques selon l'âge
- Observation et évaluation
- Signes de retard de développement

MODULE 3: SANTÉ, SÉCURITÉ ET ALIMENTATION
- Protocoles de sécurité en garderie
- Nutrition adaptée à l'âge
- Prévention des accidents
- Gestion des allergies alimentaires
- Hygiène et désinfection

MODULE 4: LE RÔLE DE LA RESPONSABLE D'UN SERVICE DE GARDE
- Responsabilités légales et éthiques
- Communication avec les parents
- Gestion administrative
- Partenariat avec les familles
- Collaboration avec les professionnels

DÉVELOPPEMENT DE L'ENFANT - FORMATIONS SPÉCIALISÉES:
- Le développement de l'enfant (formation complète)
- Le développement de l'enfant assistant/remplaçant
            """,
            "category": "garderie"
        },
        {
            "title": "Cours de perfectionnement - Thématiques disponibles",
            "content": """
COURS DE PERFECTIONNEMENT POUR ÉDUCATEURS:

SANTÉ ET SÉCURITÉ:
- Allergies? Je réagis! - Gestion des allergies et protocoles d'urgence
- Briser la chaîne infectieuse - Prévention des infections et hygiène
- Bien dormir pour bien grandir - Rythmes de sommeil et aménagement
- Le syndrome du bébé secoué - Prévention et sensibilisation

DÉVELOPPEMENT DE L'ENFANT:
- Le développement de l'enfant - Étapes et besoins selon l'âge
- Le développement langagier, acquisition et dépistage - Stimulation et intervention
- Cultiver l'intelligence émotionnelle de l'enfant - Gestion des émotions
- Verbal, gestuel ou artistique? L'enfant vous parle! - Communication non verbale

INTERVENTION ET PÉDAGOGIE:
- De A à Z… 26 techniques d'intervention - Stratégies éducatives
- L'animation par thématique - Planification d'activités
- Le jeu libre, essentiel aux apprentissages - Importance du jeu
- Le grand défi du multi-âge - Gestion des groupes mixtes

GESTION ET COMMUNICATION:
- Exclusion en cas de maladie, aide à la décision - Protocoles sanitaires
- Papa, maman… votre enfant m'inquiète! - Communication avec les parents
- Préparer l'enfant à la maternelle - Transition scolaire
- Préparer le dossier éducatif de l'enfant - Documentation

DIVERSITÉ ET INCLUSION:
- Accueillir l'enfant et sa diversité culturelle - Inclusion et adaptation
- Ma garderie est verte! - Éducation environnementale
- Mise à jour du programme éducatif - Évolution des pratiques
- Miser sur l'éducatrice - Développement professionnel

PROTECTION DE L'ENFANCE:
- La maltraitance, intervenir pour protéger l'enfant - Identification et intervention
            """,
            "category": "perfectionnement"
        },
        {
            "title": "Familles d'accueil - Formations spécialisées",
            "content": """
FORMATIONS SPÉCIALISÉES POUR FAMILLES D'ACCUEIL:

FORMATION PRINCIPALE:
- Formation Hybride en secourisme pour les Familles d'Accueil
  * Formation combinée en ligne et en présentiel
  * Adaptation aux besoins spécifiques des familles d'accueil
  * Certification complète et reconnue

FORMATIONS THÉMATIQUES SPÉCIALISÉES:
- Spécial Famille d'accueil: Allergies? Je réagis!
  * Gestion des allergies en contexte d'accueil
  * Protocoles d'urgence adaptés
  * Communication avec les services sociaux

- Spécial Famille d'accueil: Bien dormir pour bien grandir
  * Rythmes de sommeil en famille d'accueil
  * Adaptation aux nouveaux environnements
  * Gestion des troubles du sommeil

- Spécial Famille d'accueil: Briser la chaîne infectieuse
  * Prévention en milieu familial d'accueil
  * Protocoles sanitaires adaptés
  * Protection de tous les enfants

- Spécial Famille d'accueil: Cultiver l'intelligence émotionnelle
  * Accompagnement émotionnel spécialisé
  * Gestion des traumatismes
  * Techniques de réparation et de soutien

- Spécial Famille d'accueil: Développement de l'enfant
  * Développement en contexte d'accueil
  * Adaptation aux changements
  * Observation et évaluation spécialisées

- Spécial Famille d'accueil: Développement langagier
  * Stimulation du langage en accueil
  * Gestion des retards de développement
  * Techniques d'intervention adaptées

- Spécial Famille d'accueil: Le syndrome du bébé secoué
  * Prévention spécialisée
  * Éducation et sensibilisation
  * Protocoles d'intervention

- Spécial Famille d'accueil: Verbal, gestuel ou artistique
  * Communication en contexte d'accueil
  * Expression des émotions
  * Techniques d'observation
            """,
            "category": "famille_accueil"
        },
        {
            "title": "Programmes jeunesse - Formations pour jeunes",
            "content": """
PROGRAMMES SPÉCIALISÉS POUR LES JEUNES:

1. COURS DE GARDIEN FUTÉ ET AVERTI EN LIGNE
   - Formation pour adolescents (12-17 ans)
   - Compétences de gardiennage sécuritaire
   - Gestion des situations d'urgence
   - Responsabilités et sécurité
   - Formation 100% en ligne

2. FUTÉ: JE SUIS PRÊT À RESTER SEUL
   - Préparation à l'autonomie (8-12 ans)
   - Sécurité à la maison
   - Gestion des situations d'urgence
   - Règles de sécurité personnelle
   - Développement de l'autonomie

3. FORMATION EN SECOURISME POUR ANIMATEUR DE CAMP DE JOUR ET MONITEUR DE CAMP DE VACANCES
   - Secourisme adapté aux activités de plein air
   - Gestion des urgences en camp
   - Protocoles spécifiques aux activités
   - Certification pour animateurs
   - Formation pratique et théorique
            """,
            "category": "jeunesse"
        },
        {
            "title": "Formations en anglais - English courses",
            "content": """
ENGLISH COURSES AVAILABLE:

CHILDCARE FIRST AID TRAINING:
1. First Aid Adapted for Childhood (8 hour)
   - Complete training for educators
   - Certification compliant with regulations
   - Online training available

2. First Aid Adapted for Early Childhood (6 hour)
   - Renewal training
   - Updated knowledge and protocols
   - Flexible online format

3. First Aid in School Setting (8 hours)
   - Specialized for school personnel
   - School emergency management
   - Certified training

4. Online renewal of first aid in a school setting (6 hours)
   - Certification renewal
   - Updated protocols
   - Continuous training

45-HOUR TRAINING FOR CHILDCARE:
1. Child development
2. Educational program
3. Safety, health and nutrition
4. The role of the home childcare provider

PROFESSIONAL DEVELOPMENT:
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
            "category": "english"
        },
        {
            "title": "Règlementations et certifications",
            "content": """
RÉGLEMENTATIONS ET CERTIFICATIONS FORMEDUC:

CONFORMITÉ RÉGLEMENTAIRE:
- Règlement sur les services de garde éducatifs en milieu scolaire
- Loi sur l'instruction publique (chapitre l-13.3, a. 454.1)
- Normes de sécurité et d'hygiène
- Protocoles d'urgence établis

CERTIFICATIONS RECONNUES:
- Attestations professionnelles valorisantes
- Reconnaissance par les employeurs
- Validité réglementaire
- Mise à jour continue

PROCÉDURES DE CERTIFICATION:
- Évaluation continue pendant la formation
- Examen final de validation
- Attestation de réussite
- Certificat conforme aux normes

RENOUVELLEMENT DE CERTIFICATION:
- Formations de mise à jour disponibles
- Période de validité respectée
- Contenu actualisé
- Procédures simplifiées
            """,
            "category": "reglementation"
        }
    ]
    
    return knowledge_base

def main():
    """Fonction principale pour charger les données Formeduc dans ChromaDB"""
    print("🚀 Chargement de la base de connaissances Formeduc pour Elavira")
    
    # Récupérer les données
    knowledge_base = get_formeduc_knowledge_base()
    
    # Préparer les documents pour ChromaDB
    documents = []
    for item in knowledge_base:
        doc = f"""
Titre: {item['title']}
Catégorie: {item['category']}

Contenu:
{item['content']}

---
Source: Site officiel Formeduc.ca
Institution: Formeduc
Spécialisation: Formations en secourisme et services de garde éducatifs
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
        print("🎯 Base de connaissances Elavira mise à jour avec les données Formeduc")
        
        # Sauvegarder les métadonnées
        metadata = {
            'loaded_at': datetime.now().isoformat(),
            'total_documents': len(documents),
            'source': 'formeduc.ca',
            'categories': list(set(item['category'] for item in knowledge_base)),
            'assistant': 'Elavira',
            'purpose': 'Formations en secourisme et services de garde éducatifs'
        }
        
        with open('/app/formeduc_metadata.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print("✅ Métadonnées sauvegardées")
        print("🎉 Base de connaissances Formeduc chargée avec succès pour Elavira!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation: {e}")

if __name__ == "__main__":
    main()
