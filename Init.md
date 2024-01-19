🌞 **Ajouter votre utilisateur au groupe `docker`**

```
sudo usermod -aG docker $USER
exec su -l $USER
(pour mettre a jour les perms)
```

- vérifier que vous pouvez taper des commandes `docker` comme `docker ps` sans avoir besoin des droits `root`

```
docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## 4. Un premier conteneur en vif

🌞 **Lancer un conteneur NGINX**

- avec la commande suivante :

```bash
docker run -d -p 9999:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
af107e978371: Pull complete 
336ba1f05c3e: Pull complete 
8c37d2ff6efa: Pull complete 
51d6357098de: Pull complete 
782f1ecce57d: Pull complete 
5e99d351b073: Pull complete 
7b73345df136: Pull complete 
Digest: sha256:bd30b8d47b230de52431cc71c5cce149b8d5d4c87c204902acf2504435d4b4c9
Status: Downloaded newer image for nginx:latest
3169592393f96ba9453ca64e4a4d2589cf0736f0c68a97e3a74cef3d52ef643f
```

🌞 **Visitons**

- vérifier que le conteneur est actif avec une commande qui liste les conteneurs en cours de fonctionnement

```
d ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                   NAMES
3169592393f9   nginx     "/docker-entrypoint.…"   44 seconds ago   Up 43 seconds   0.0.0.0:9999->80/tcp, :::9999->80/tcp   wonderful_hawking
```

- afficher les logs du conteneur

```
d logs wonderful_hawking
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/12/21 09:38:58 [notice] 1#1: using the "epoll" event method
...
```

- afficher toutes les informations relatives au conteneur avec une commande `docker inspect`

```
d inspect wonderful_hawking
[
    {
        "Id": "3169592393f96ba9453ca64e4a4d2589cf0736f0c68a97e3a74cef3d52ef643f",
        "Created": "2023-12-21T09:38:57.86729427Z",
        "Path": "/docker-entrypoint.sh",
...
```

- afficher le port en écoute sur la VM avec un `sudo ss -lnpt`

```
sudo ss -lnpt | grep docker
LISTEN 0      4096         0.0.0.0:9999       0.0.0.0:*    users:(("docker-proxy",pid=12988,fd=4))                                                                                                                            
LISTEN 0      4096            [::]:9999          [::]:*    users:(("docker-proxy",pid=12994,fd=4))  
```

- ouvrir le port `9999/tcp` (vu dans le `ss` au dessus normalement) dans le firewall de la VM

```
sudo firewall-cmd --add-port=9999/tcp --permanent
success
sudo firewall-cmd --reload
success
sudo firewall-cmd --list-ports
9999/tcp
```

- depuis le navigateur de votre PC, visiter le site web sur `http://IP_VM:9999`

```
curl http://10.33.66.196:9999/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

🌞 **On va ajouter un site Web au conteneur NGINX**

- créez un dossier `nginx`
  - pas n'importe où, c'est ta conf caca, c'est dans ton homedir donc `/home/<TON_USER>/nginx/`
- dedans, deux fichiers : `index.html` (un site nul) `site_nul.conf` (la conf NGINX de notre site nul)
- exemple de `index.html` :

```html
<h1>MEOOOW</h1>
```

- config NGINX minimale pour servir un nouveau site web dans `site_nul.conf` :

```nginx
server {
    listen        8080;

    location / {
        root /var/www/html/index.html;
    }
}
```

- lancez le conteneur avec la commande en dessous, notez que :
  - on partage désormais le port 8080 du conteneur (puisqu'on l'indique dans la conf qu'il doit écouter sur le port 8080)
  - on précise les chemins des fichiers en entier
  - note la syntaxe du `-v` : à gauche le fichier à partager depuis ta machine, à droite l'endroit où le déposer dans le conteneur, séparés par le caractère `:`
  - c'est long putain comme commande

```bash
docker run -d -p 9999:8080 -v /home/<USER>/nginx/index.html:/var/www/html/index.html -v /home/<USER>/nginx/site_nul.conf:/etc/nginx/conf.d/site_nul.conf nginx
```

🌞 **Visitons**

- vérifier que le conteneur est actif

```
d ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                                               NAMES
94ecedda1e23   nginx     "/docker-entrypoint.…"   46 seconds ago   Up 45 seconds   80/tcp, 0.0.0.0:9999->8080/tcp, :::9999->8080/tcp   laughing_nash
```

- aucun port firewall à ouvrir : on écoute toujours port 9999 sur la machine hôte (la VM)
- visiter le site web depuis votre PC

```
curl http://10.33.66.196:9999/ 
<h1>MEOOOW</h1>
```

## 5. Un deuxième conteneur en vif

🌞 **Lance un conteneur Python, avec un shell**

```bash
docker run -it python bash
Unable to find image 'python:latest' locally
latest: Pulling from library/python
bc0734b949dc: Pull complete 
...
```

🌞 **Installe des libs Python**

- une fois que vous avez lancé le conteneur, et que vous êtes dedans avec `bash`
- installez deux libs, elles ont été choisies complètement au hasard (avec la commande `pip install`):
  - `aiohttp`
  - `aioconsole`

```
pip install aiohttp
Collecting aiohttp
...
pip install aioconsole
Collecting aioconsole
...
```

- tapez la commande `python` pour ouvrir un interpréteur Python
- taper la ligne `import aiohttp` pour vérifier que vous avez bien téléchargé la lib

```
python
Python 3.12.1 (main, Dec 19 2023, 20:14:15) [GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import aiohttp
>>> 
```
