# Piscine Django Day 06 - Gestion des Utilisateurs et Permissions

## Description des Exercices

Ce document décrit une série d'exercices avancés Django axés sur la gestion des utilisateurs, l'authentification, et la mise en œuvre des permissions. Les exercices vont de la création de sessions anonymes, la gestion des utilisateurs avec inscription et connexion, à l'implémentation de fonctionnalités comme les upvotes/downvotes, la personnalisation des permissions, et l'introduction d'un système de réputation pour les utilisateurs basé sur les interactions. Chaque exercice requiert la mise en place de modèles, de vues, et de templates Django spécifiques, avec une attention particulière portée à la sécurité et à l'expérience utilisateur.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ex
python manage.py makemigrations myapp
python manage.py migrate
python manage.py runserver
```