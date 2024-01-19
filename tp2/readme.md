# TP2 Commun : Stack PHP

```
d pull php:latest
latest: Pulling from library/php
d pull mysql
Using default tag: latest
d pull mysql
Using default tag: latest
```

➜ **ensuite on run les bails**

- vous pouvez jouer avec des `docker run` un peu pour utiliser les images et voir comment elles fonctionnent
- rapidement passer à la rédaction d'un `docker-compose.yml` qui lance les trois
- lisez bien les README de vos images, y'a tout ce qu'il faut

Pour ce qui est du contenu du `docker-compose.yml`, à priori :

- **il déclare 3 conteneurs**
  - **PHP + Apache**
    - un volume qui place votre code PHP dans le conteneur
    - partage de port pour accéder à votre site
  - **MySQL**
    - définition d'un user, son mot de passe, un nom de database à créer avec des variables d'environnement
    - injection d'un fichier `.sql`
      - pour créer votre schéma de base au lancement du conteneur
      - injecter des données simulées je suppose ?
  - **PHPMyAdmin**
    - dépend de l'image que vous utilisez
    - partage de port pour accéder à l'interface de PHPMyAdmin
- en fin de TP1, vous avez vu que vous pouviez `ping <NOM_CONTENEUR>`
  - **donc dans ton code PHP, faut changer l'IP de la base de données à laquelle tu te co**
  - ça doit être vers le nom du conteneur de base de données

> *Donc : dès qu'un conteneur est déclaré dans un `docker-compose.yml` il peut joindre tous les autres via leurs noms sur le réseau. Et c'est bien pratique. **Nik les adresses IPs.***

Bon j'arrête de blabla, voilà le soleil.

🌞 **`docker-compose.yml`**

- genre `tp2/php/docker-compose.yml` dans votre dépôt git de rendu
- votre code doit être à côté dans un dossier `src` : `tp2/php/src/tous_tes_bails.php`
- s'il y a un script SQL qui est injecté dans la base à son démarrage, il doit être dans `tp2/php/sql/seed.sql`
  - on appelle ça "seed" une database quand on injecte le schéma de base et éventuellement des données de test
- bah juste voilà ça doit fonctionner : je git clone ton truc, je `docker compose up` et ça doit fonctionne :)
- ce serait cool que l'app affiche un truc genre `App is ready on http://localhost:80` truc du genre dans les logs !

➜ **Un environnement de dév local propre avec Docker**

- 3 conteneurs, donc environnement éphémère/destructible
- juste un **`docker-compose.yml`** donc facilement transportable
- TRES facile de mettre à jour chacun des composants si besoin
  - oh tiens il faut ajouter une lib !
  - oh tiens il faut une autre version de PHP !
  - tout ça c'est np

![save urself](img/save_urself.png)

