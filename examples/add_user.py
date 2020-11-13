import requests

# https://requests.readthedocs.io/es/latest/

host = "http://localhost:5000/v1/user"

payload = dict(
    user="lucio5",
    pwd="123456",
    email="luciondiaz@alumno.eestn4garin.edu.ar",
    )


r = requests.post("http://localhost:5000/v1/user", json=payload)

print(r.content)
