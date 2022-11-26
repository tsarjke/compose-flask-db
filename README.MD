# Counter app with postgres and docker-compose

```
docker swarm init
docker service create --name registry --publish published=6001,target=6001 registry:2
```

And to check it run:
```
docker service ls
```

Next:
```
docker-compose push
docker stack deploy --compose-file docker-compose.yml counterdb
```

Check it by:
```
docker ps
```

And make 4 instances:
```
docker service scale counterdb_app=4
```

To leave it run:
```
docker swarm leave --force
```