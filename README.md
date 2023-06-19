# transformer service


## Steps to Setups Server ##

- INSTALL python 3.7.

```
sudo apt update
sudo apt install python3.7
sudo apt install python3-pip
```

- Create or Update the credential and other required things .env file in config.


- Create a Virtual Environment outside Project folder

```
virtualenv -p python3 venv
```

- Activate the Virtual Environment.

```
 > source venv/bin/activate (Linux)
 > venv\Scripts\Activate (Windows)
```

- Install required python library.

```
pip install -r requirements.txt
```



## Env Structure

```
# Kafka Configuration

KAFKA_SERVER=
TRANSFORMER_CHANNEL=
AGGREGATOR_CHANNEL=
DYNAMODB_KEY=
```