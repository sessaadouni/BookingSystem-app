# Projet BookingSystem

## Objectif

Ce projet est une application de migration de données d'une base de données SQL vers une base de données NoSQL.

## Prérequis

- Docker (Docker-compose)
- make

## Installation

### Cloner le projet

```bash
git clone https://github.com/sessaadouni/Bookingsystem.git
```

Ouvrir le terminal et aller dans le dossier du projet

```bash
cd Bookingsystem
```

### Mise en place des fichiers d'environnement

Copier les fichiers `.env.mongo.example`,  `.env.redis.example` et `.env.example` dans le dossier `.docker/mongo`, `.docker/redis` et `.env` respectivement.

Remplacer les valeurs par les bonnes.

```bash
cp .docker/mongo/.env.mongo.example .docker/mongo/.env.mongo
cp .docker/redis/.env.redis.example .docker/redis/.env.redis
cp .env.example .env
```

### Mise en place de l'environnement de développement

Pour mettre en place l'environnement de développement, il faut build les images Docker.

```bash
make compose-up
```

### Mise en place du replica-set MongoDB

Pour mettre en place le replica-set MongoDB, il faut exécuter la commande suivante dans le terminal.

```bash
make replica-init
```

### Dénormalisation des données

Pour dénormaliser les données, il faut exécuter la commande suivante dans le terminal.

```bash
make denormalize
```

### Injection des données

Pour injecter les données, il faut exécuter la commande suivante dans le terminal.

```bash
make inject-redis
make inject-mongo
```

### Verifier les données

Pour vérifier les données, il faut exécuter les commandes suivantes dans le terminal.

> Pour Redis:

```bash
make redis-cli

> AUTH "Mot de passe de la base de données"
> KEYS *
> QUIT [ou Ctrl+C]
```

> Pour Mongo:

```bash
make mongo-shell

> show dbs
> use BookingSystem
> db.clients.find()
> db.vols.find()
> db.reservations.find()
> quit() [Or Ctrl+C]
```

### Tester les requêtes

Pour tester les requêtes, il faut exécuter les commandes suivantes dans le terminal.

```bash
make python file=src/api/request_json.py
make python file=src/api/request_redis.py
make python file=src/api/request_mongo.py
```
