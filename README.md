
# 🎓 LearnVerse API - Plateforme de Cours en Ligne (Django + DRF)

LearnVerse API est une application backend RESTful construite avec Django et Django REST Framework. Elle permet de gérer une plateforme de cours en ligne : ajout de cours, gestion des formateurs, inscription des utilisateurs, etc.

---

## 🎯 Objectifs

- Développer une API REST professionnelle pour des cours en ligne.
- Offrir une gestion complète des cours, formateurs et étudiants.
- Ajouter des fonctionnalités de recherche, filtrage, pagination.
- Intégrer l’authentification via JWT.
- Documenter l'API avec Swagger.

---

## 🧱 Stack technique

- **Langage** : Python 3.x  
- **Frameworks** : Django, Django REST Framework  
- **Base de données** : SQLite (par défaut), PostgreSQL (optionnel)  
- **Tests** : Unittest / Pytest  
- **Authentification** : JWT (`djangorestframework-simplejwt`)  
- **Documentation API** : Swagger (via `drf-yasg` ou `drf-spectacular`)  
- **Déploiement** : Docker / Render / Heroku

---

## 📚 Modèle principal : `Course`

| Champ          | Type      | Description                                 |
|----------------|-----------|---------------------------------------------|
| `id`           | UUID      | Identifiant unique                          |
| `title`        | string    | Titre du cours                              |
| `description`  | text      | Description détaillée du cours              |
| `duration`     | integer   | Durée en heures                             |
| `level`        | string    | Niveau (`beginner`, `intermediate`, `expert`) |
| `price`        | decimal   | Prix du cours                               |
| `language`     | string    | Langue d’enseignement                       |
| `instructor`   | FK        | Référence au formateur (modèle `Instructor`) |
| `created_at`   | datetime  | Date de création                            |
| `updated_at`   | datetime  | Dernière mise à jour                        |

Modèles secondaires :
- `Instructor` (nom, bio, email)
- `Student` (nom, email, cours suivis)

---

## 🗂️ Structure du projet

```
learnverse/
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── tests/
├── learnverse/
│   └── settings.py
├── manage.py
└── README.md
```


## 🔑 Authentification

L’API utilise JSON Web Token (JWT).  
Obtenir un token via `/api/token/` puis inclure le header :

```
Authorization: Bearer <votre-token>
```

---

## 📬 Endpoints principaux

| Méthode | Endpoint              | Description                     |
|---------|------------------------|---------------------------------|
| POST    | /api/token/            | Authentification, retourne un JWT |
| POST    | /api/token/refresh/    | Rafraîchit un access token      |
| GET     | /api/courses/          | Liste tous les cours            |
| POST    | /api/courses/          | Crée un nouveau cours           |
| GET     | /api/courses/{id}/     | Détails d’un cours              |
| PUT     | /api/courses/{id}/     | Met à jour un cours             |
| DELETE  | /api/courses/{id}/     | Supprime un cours               |
| GET     | /api/instructors/      | Liste des formateurs            |

---

## 🧪 Tests

```bash
pytest  # ou python manage.py test
```

---

## 🌐 Déploiement

> Configuration Docker en cours. Le projet peut être déployé sur Render, Heroku, ou sur un VPS.

---

## 📄 Licence

Projet open-source sous licence MIT.

---

## ✍️ Auteur

**N'STOUAGLO Kokou Gawonou**  
Développeur Backend Python | APIs REST | Génie Logiciel | Éducation Tech
