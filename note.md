# fork from origin project

## feature

- env file for secret
- more platform support
- APIs for current streamer status

## run and build

```bash
bash render_config.sh
docker run -d -p 5001:5001 -v ./config.final.yml:/mnt/config.yml aio-chz-dynamic-push:latest
```
