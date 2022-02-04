

1. si ejecutamos nos aparecera el siguiente error 

`FileNotFoundError: [Errno 2] No such file or directory: b'liblibc.a'` 

para solucionarlo : 

```
 cd /usr/lib/x86_64-linux-gnu
 sudo ln -s -f libc.a liblibc.a
```

2. Instalar paquetes necesarios 

`pip3 install -r requirements.txt`