# PySilverse

### Local

```
export PYTHONPATH=/path/to/pysilverse:$PYTHONPATH
```

### Docker

0. Buid local **development** docker image

```
bash development.sh
```

1. Run **development** image with local source

```
sudo docker run \
  -it \
  --name pysilverse --rm \
  -v /home/ermiry/Documents/Work/pysilverse:/home/pysilverse \
  itsilverse/pysilverse:development /bin/bash
```

2. Handle **pysilverse** module

```
export PYTHONPATH=$pwd:$PYTHONPATH
```
