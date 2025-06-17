# local-library
A web app for a local library using Python, SQLite, Docker & React (Vite)


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