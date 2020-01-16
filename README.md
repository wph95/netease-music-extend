
```bash
docker run -d --name mcli wph95/netease-music:latest
docker exec -it mcli pipenv run python3 myli.py -u {phone} -p {password} follow
# see all follower with user_id 

docker exec -it mcli pipenv run python3 mcli.py -u {phone} -p {password} union {other_user_id}
# create a private playlist to save union record list

docker kill mcli 
```