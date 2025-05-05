# fork from origin project

## feature

- env file for secret
- more platform support
- APIs for current streamer status

## run and build

```bash
bash render_config.sh
docker build -t aio-chz-dynamic-push:latest .
docker run -d --name my-notify -p 5001:5001 -v ./config.final.yml:/mnt/config.yml aio-chz-dynamic-push:latest 
docker restart my-notify
```
