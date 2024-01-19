## 1. Images publiques

🌞 **Récupérez des images**

- avec la commande `docker pull`
- récupérez :
  - l'image `python` officielle en version 3.11 (`python:3.11` pour la dernière version)
```
d pull python:3.11
3.11: Pulling from library/python
bc0734b949dc: Already exists 
...
```
  - l'image `mysql` officielle en version 5.7
```
d pull mysql:5.7
5.7: Pulling from library/mysql
20e4dcae4c69: Pull complete 
...
```
  - l'image `wordpress` officielle en dernière version
```
d pull wordpress
Using default tag: latest
latest: Pulling from library/wordpress
...
docker.io/library/wordpress:latest
```
    - c'est le tag `:latest` pour récupérer la dernière version
    - si aucun tag n'est précisé, `:latest` est automatiquement ajouté
  - l'image `linuxserver/wikijs` en dernière version
```
d pull linuxserver/wikijs
Using default tag: latest
latest: Pulling from linuxserver/wikijs
8b16ab80b9bd: Pull complete 
...
```
- listez les images que vous avez sur la machine avec une commande `docker`

```
d images
REPOSITORY           TAG               IMAGE ID       CREATED        SIZE
linuxserver/wikijs   latest            869729f6d3c5   5 days ago     441MB
mysql                5.7               5107333e08a8   8 days ago     501MB
python               latest            fc7a60e86bae   13 days ago    1.02GB
wordpress            latest            fd2f5a0c6fba   2 weeks ago    739MB
python               3.11              22140cbb3b0c   2 weeks ago    1.01GB
python               3.11-alpine3.18   8b683f39f4af   2 weeks ago    52.1MB
nginx                latest            d453dd892d93   8 weeks ago    187MB
hello-world          latest            d2c94e258dcb   7 months ago   13.3kB
```

🌞 **Lancez un conteneur à partir de l'image Python**

- lancez un terminal `bash` ou `sh`
```
docker run -it python:3.11 bash
```

- vérifiez que la commande `python` est installée dans la bonne version

```
root@cc1d9c90ae8f:/# python -V
Python 3.11.7
```
## 2. Construire une image

Pour construire une image il faut :

- créer un fichier `Dockerfile`
- exécuter une commande `docker build` pour produire une image à partir du `Dockerfile`

🌞 **Ecrire un Dockerfile pour une image qui héberge une application Python**

- l'image doit contenir
  - une base debian (un `FROM`)
  - l'installation de Python (un `RUN` qui lance un `apt install`)
    - il faudra forcément `apt update` avant
    - en effet, le conteneur a été allégé au point d'enlever la liste locale des paquets dispos
    - donc nécessaire d'update avant de install quoique ce soit
  - l'installation de la librairie Python `emoji` (un `RUN` qui lance un `pip install`)
  - ajout de l'application (un `COPY`)
  - le lancement de l'application (un `ENTRYPOINT`)
- le code de l'application :

```python
import emoji

print(emoji.emojize("Cet exemple d'application est vraiment naze :thumbs_down:"))
```

- pour faire ça, créez un dossier `python_app_build`
  - pas n'importe où, c'est ton Dockerfile, ton caca, c'est dans ton homedir donc `/home/<USER>/python_app_build`
  - dedans, tu mets le code dans un fichier `app.py`
  - tu mets aussi `le Dockerfile` dedans

> *J'y tiens beaucoup à ça, comprenez que Docker c'est un truc que le user gère. Sauf si vous êtes un admin qui vous en servez pour faire des trucs d'admins, ça reste dans votre `/home`. Les dévs quand vous bosserez avec Windows, vous allez pas stocker vos machins dans `C:/Windows/System32/` si ? Mais plutôt dans `C:/Users/<TON_USER>/TonCaca/` non ? Alors pareil sous Linux please.*

🌞 **Build l'image**

- déplace-toi dans ton répertoire de build `cd python_app_build`
- `docker build . -t python_app:version_de_ouf`
  - le `.` indique le chemin vers le répertoire de build (`.` c'est le dossier actuel)
  - `-t python_app:version_de_ouf` permet de préciser un nom d'image (ou *tag*)
- une fois le build terminé, constater que l'image est dispo avec une commande `docker`

```
d build . -t python_app_build
[+] Building 15.2s (11/11) FINISHED   
```

🌞 **Lancer l'image**

- lance l'image avec `docker run` :

```bash
docker run python_app_build:latest 
Cet exemple d'application est vraiment naze 👎
```

