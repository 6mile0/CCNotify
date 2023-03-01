# CCNotify

This API retrieves the latest information from the university's website calendar and returns it in JSON format.

## Usage

### 1. Clone this repository

```bash
$ git clone git@github.com:6mile0/CCNotify.git
```

### 2. Install Docker

If you are using a new host, you can install Docker using [docker-installer](https://github.com/6mile0/docker-installer).

### 3. Add .env file

Please enter your system ID email address and password respectively.

```bash
$ cd CCNotify
$ cp .env.example .env
$ vi .env
```

Sapmle:

```bash
$ cat .env
EMAIL="xxxxxxx@edu.teu.ac.jp"
PASS="xxxxxxxx"
DATADIR="/data"
```

You can select a location to store the acquired data in `DATA_DIR`. (Optional)

### 4. Run Docker

```bash
$ cd CCNotify
$ docker-compose up -d
```
