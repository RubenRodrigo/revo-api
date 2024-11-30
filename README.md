# Pasos para levantar el backend

Hola amiguito! Acompañame a esta aventura sobre como levantar nuestro backend de la hackathon para ganar el primer premio 🤑

1. Primero debes crear tu bd y agregar la variable de entorno `DATABASE_URL` en el archivo `.env`
2. Luego, debes agregar la variable `JWT_SECRET` para cuestiones de autenticacion
3. Por ultimo debes instalar las librerias en tu entorno virtual, para crear un entorno virtual corre el siguiente comando 😉

```
$ py -m venv entorno
```

4. Luego, levanta el entorno:

```
$ source entorno/bin/activate
```

5. Por ultimo:

```
$ pip install -r requirements.txt
```

6. Y una vez que ya tengamos las librerias instaladas ahora **AH LLEGADO EL MOMENTO!** 🚀

```
$ py app.py
```

**DISCLAIMER:** Documentacion no disponible ni ahora ni nunca 💀
