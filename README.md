# local-library
A web app for a local library using Python, SQLite, Docker & React (Vite)

## Running the app

- Building the containers:

```bash
$ docker-compose up --build -d
```

- To run the frontend:

```bash
$ cd ui
$ yarn install
$ yarn dev
```

## Testing

- Creating a virtual python environment
```bash
$ cd backend/api
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

- Running the python tests
```bash
$ cd backend
$ coverage run -m unittest discover ./api
```

## Extensions & considerations

- Given time, further testing & refactoring