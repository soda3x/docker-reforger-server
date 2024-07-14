# Arma Reforger Dedicated Server

Containerised Arma Reforger Dedicated Server

1. Create a server config (see: [here](https://community.bistudio.com/wiki/Arma_Reforger:Server_Config)).

    >Be sure to keep the server's ports as defaults (2001, 17777 and 19999) and instead use port mappings to change them

2. Place your server config in your `configs` directory (mapped to `/home/reforger/configs`) and set the `CONFIG` environment variable to the name of the file without the extension.

3. Your mods will be downloaded and stored in the `workshop` folder and your profile including your save games, and configurations for certain mods are in the `profile` folder.

4. All of `configs`, `workshop` and `profile` should be mapped to a location on the Host for persistence.

## Experimental Branch

If you would like to host a server using the experimental branch, set the `USE_EXPERIMENTAL` environment variable to `true`

## Example Docker Compose

```yaml
version: '3.8'
services:
  arma-reforger:
    image: soda3x/docker-reforger-server:latest
    platform: linux/amd64
    container_name: arma-reforger
    build:
      context: .
    ports:
      - "2001:2001/udp"
      - "17777:17777/udp"
      - "19999:19999/udp" # RCON
    volumes:
      - ./reforger/configs:/home/reforger/configs
      - ./reforger/profile:/home/reforger/profile
      - ./reforger/workshop:/home/reforger/workshop
    environment:
      - CONFIG="myconfig" # Name of your config (without path or .json extension)
      - USE_EXPERIMENTAL=false # Set to true to use Experimental branch of Reforger server
```
