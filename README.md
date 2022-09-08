# tipping-bot
Normal Bot to tip tokens

## How to docker
!! Be aware that this docker-compose file does **not** push docker to a repo !! 

Bot uses the following vars

- `MONGODB_USERNAME` -> Mongodb username
- `MONGODB_PASSWORD` -> Mongodb password
- `DISCORD_API_KEY` -> API Key from discord
#### Step 1. Exposure of env vars 

#### Use of hosting provider
Rely on provider, e.g. AWS' Parameter store
#### Using shell
`export MONGODB_USERNAME=<username>`

`export MONGODB_PASSWORD=<password>`

`export DISCORD_API_KEY=<api token>`
#### Using .env file
Create a `.env` file with contents of
```
MONGODB_USERNAME=<username>
MONGODB_PASSWORD=<password>
DISCORD_API_KEY=<api token>
```
### Step 2. Run docker-compose
In the case of exposing environmental vars through the .env file, docker-compose needs to run as 

```
docker-compose --env-file <location of env file> -f docker-compose.build.yml up --build -d
```
In any other case:
```
docker-compose -f docker-compose.build.yml up --build -d
```

### Step 3. Validation
Executing `docker ps` should report two dockers `tipping_bot` and `tipping_bot_db`

