# III. Docker compose

🌞 **Créez un fichier `docker-compose.yml`**

- dans un nouveau dossier dédié `/home/<USER>/compose_test`
```
pwd
/home/abel/compose_test
```
```
ls
docker-compose.yml
```

- le contenu est le suivant :

```yml
version: "3"

services:
  conteneur_nul:
    image: debian
    entrypoint: sleep 9999
  conteneur_flopesque:
    image: debian
    entrypoint: sleep 9999
```

🌞 **Lancez les deux conteneurs** avec `docker compose`

- déplacez-vous dans le dossier `compose_test` qui contient le fichier `docker-compose.yml`
- go exécuter `docker compose up -d`

> Si tu mets pas le `-d` tu vas perdre la main dans ton terminal, et tu auras les logs des deux conteneurs. `-d` comme *daemon* : pour lancer en tâche de fond.

```
docker compose up -d 
[+] Running 3/3
 ✔ conteneur_nul Pulled                                                                        3.1s 
 ✔ conteneur_flopesque 1 layers [⣿]      0B/0B      Pulled                                     3.1s 
   ✔ bc0734b949dc Already exists                                                               0.0s 
[+] Running 3/3
 ✔ Network compose_test_default                  Created                                       0.2s 
 ✔ Container compose_test-conteneur_nul-1        S...                                          0.0s 
 ✔ Container compose_test-conteneur_flopesque-1  Started                                       0.0s 
```

🌞 **Vérifier que les deux conteneurs tournent**

- toujours avec une commande `docker`
- tu peux aussi use des trucs comme `docker compose ps` ou `docker compose top` qui sont cools dukoo
  - `docker compose --help` pour voir les bails

```
d compose ps
NAME                                 IMAGE     COMMAND        SERVICE               CREATED         STATUS         PORTS
compose_test-conteneur_flopesque-1   debian    "sleep 9999"   conteneur_flopesque   2 minutes ago   Up 2 minutes   
compose_test-conteneur_nul-1         debian    "sleep 9999"   conteneur_nul         2 minutes ago   Up 2 minutes   
```

🌞 **Pop un shell dans le conteneur `conteneur_nul`**

- référez-vous au mémo Docker
- effectuez un `ping conteneur_flopesque` (ouais ouais, avec ce nom là)
  - un conteneur est aussi léger que possible, aucun programme/fichier superflu : t'auras pas la commande `ping` !
  - il faudra installer un paquet qui fournit la commande `ping` pour pouvoir tester
```
apt update -y
apt install iputils-ping
```
  - juste pour te faire remarquer que les conteneurs ont pas besoin de connaître leurs IP : les noms fonctionnent
```
ping conteneur_flopesque
PING conteneur_flopesque (172.18.0.2) 56(84) bytes of data.
```
