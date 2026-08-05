# `deploy/` — cómo se levanta TEAPP en la nube

> 🚨 **Esta carpeta es lo único que sobrevive.** La cuenta de AWS del plan
> gratuito **se va a cerrar** a los 6 meses (`[C-003]`), y con ella la máquina y
> todo lo que se hubiera configurado a mano. `[C-004]` lo dice sin rodeos: lo
> que solo existe porque se hizo clic a clic, está perdido de antemano.
>
> 📌 **La cuenta es desechable. Esto no.**

## Qué hay aquí

| archivo | qué es |
|---|---|
| `console_steps.md` | 🚨 **los clics que no se pueden escribir**, en orden. Incluye la lista de **ESTO NUNCA SE TOCA** |
| `install.sh` | instala todo en una Ubuntu recién creada. No pregunta nada |
| `teapp.service` | el arranque automático, para que la app vuelva sola tras un reinicio |
| `Caddyfile.template` | el servidor de delante: HTTPS y tope de tamaño del cuerpo |

## El orden

1. **Leer `console_steps.md` entero.** Se entra a la consola de AWS a
   **ejecutar** esa lista, no a decidir dentro de ella.
2. Hacer sus pasos 1 a 4 (cuenta + alarma, DuckDNS, máquina, cortafuegos).
3. Copiar el repo a `/opt/teapp` en la máquina.
4. Correr el instalador:

   ```bash
   sudo TEAPP_DOMAIN=teapp.duckdns.org bash deploy/install.sh
   ```

5. Crear la primera cuenta — el instalador imprime cómo. ⚠️ Con el servidor
   **parado**: el script y el servidor a la vez son dos procesos escribiendo
   `data/`, y el candado no los ve (`[A-002]`).

## El dibujo

```
   internet ──HTTPS(443)──►  Caddy  ──HTTP──►  uvicorn (127.0.0.1:8000)
                               │                    │
                          certificado          TEAPP (FastAPI)
                          de Let's Encrypt          │
                                                  data/
```

🔑 **Dos servidores y no uno, por una razón concreta:** uvicorn sabe contestar
peticiones pero no sabe de certificados. Caddy sí, y los saca y renueva solo.

## El instalador comprueba, no anuncia

Al final, `install.sh` hace **tres** comprobaciones, y son tres cosas distintas:

| qué mira | qué demuestra |
|---|---|
| `systemctl is-active` | que systemd **lanzó** el proceso |
| `curl` a `127.0.0.1:8000` | que **la app contesta** |
| `curl` a `https://<dominio>` | que **se llega desde fuera, con certificado** |

🚨 **La primera sola no basta, y por poco se quedó sola.** Si uvicorn arranca y
revienta medio segundo después —un `.env` que no puede leer—, `Restart=always`
lo relanza y `is-active` lo ve `active`. El guion habría dicho "Listo" sobre una
app muerta. Ver `[L-017]`.

⚠️ **El último `curl` sale a internet, y está bien que salga.** `[C-001]` habla
de la suite de tests y del cierre, no de un despliegue a mano. **No lo quites
"por coherencia"**: sin él, el mensaje final vuelve a ser una promesa en vez de
un resultado.

## Lo que hay que mirar cuando algo falle

```bash
sudo systemctl status teapp        # ¿está viva?
sudo journalctl -u teapp -f        # el log de TEAPP, en directo
sudo journalctl -u caddy -n 50     # el log de Caddy (certificados)
```

## Lo que todavía no está probado

⚠️ Nada de esta carpeta se ha corrido nunca — no hay máquina. Hasta `T-069`,
**"está todo escrito" es una afirmación sin medir** (`[D-030]`).

`T-069` es la prueba, y va **pronto, no al final**: con TEAPP arriba y
funcionando, borrar la máquina y levantarla otra vez **solo desde aquí**. Cuesta
céntimos y deja meses de margen para arreglar lo que falte.
