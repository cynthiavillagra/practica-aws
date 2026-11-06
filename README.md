# Práctica AWS: consumir un modelo publicado en la nube

Un modelo de scikit-learn (clasificador de flores iris) empaquetado en Docker, guardado en **Amazon ECR** y servido con **AWS Lambda** mediante una **Function URL** pública. Las y los estudiantes lo consumen con un `POST` HTTP, sin necesitar una cuenta de AWS.

```
cliente (requests / curl)  --POST JSON-->  Function URL  -->  Lambda (contenedor)  -->  modelo .joblib
                                                                   ^
                                                     imagen guardada en ECR
```

Costo: $0 dentro de la capa gratuita (Lambda: 1 millón de pedidos por mes; ECR: 500 MB de almacenamiento privado durante el primer año). Solo se publica **sklearn**, porque las imágenes de TensorFlow y PyTorch superan 1 GB y no entran en los 500 MB gratis.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `train_*.py` | Scripts que entrenan los modelos |
| `deployment/sklearn/` | `dockerfile`, `lambda_function.py`, modelo y `requirements.txt` con versiones fijas |
| `cliente/consumir_modelo.py` | Script que usan las y los estudiantes |

## Parte docente: publicar el modelo (una vez)

Requisitos: Docker Desktop abierto y AWS CLI v2 configurada con `aws configure` (las claves NO van al repo).

```powershell
cd deployment\sklearn

$CUENTA = "438172062742"
$REGION = "us-east-2"
$REPO   = "$CUENTA.dkr.ecr.$REGION.amazonaws.com/ml-sklearn"

# 1. Construir la imagen (--provenance=false es obligatorio para Lambda)
docker buildx build --platform linux/amd64 --provenance=false -t ml-sklearn .

# 2. (Opcional) Probarla en la PC antes de subirla
docker run -p 9000:8080 ml-sklearn
#   en otra terminal:
#   curl.exe -X POST http://localhost:9000/2015-03-31/functions/function/invocations -d '{\"body\": \"{\\\"features\\\": [5.1,3.5,1.4,0.2]}\"}'

# 3. Loguearse en ECR y subirla
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$CUENTA.dkr.ecr.$REGION.amazonaws.com"
docker tag ml-sklearn:latest "${REPO}:latest"
docker push "${REPO}:latest"
```

### Crear la Lambda (consola web, región Ohio / us-east-2)

1. **Lambda → Crear función → Imagen de contenedor**.
2. Nombre: `iris-sklearn`. URI de la imagen: **Examinar imágenes** → `ml-sklearn:latest`. Arquitectura: **x86_64**.
3. Crear. Después, en **Configuración → Configuración general → Editar**: memoria **512 MB** y tiempo de espera **30 s** (el primer arranque carga sklearn).
4. **Configuración → URL de la función → Crear URL de función**: tipo de autenticación **NONE**. En **CORS**, activarlo con origen `*` si se va a consumir desde una página web.
5. Copiar la URL (`https://xxxx.lambda-url.us-east-2.on.aws/`) y pasársela al curso.

Si se cambia el modelo: repetir `build` + `push` y en Lambda **Implementar nueva imagen**.

## Parte estudiantes: consumir el modelo

**Python:**

```bash
pip install requests
python cliente/consumir_modelo.py
```

**curl (PowerShell):**

```powershell
curl.exe -X POST "https://xxxx.lambda-url.us-east-2.on.aws/" -H "Content-Type: application/json" -d '{\"features\": [5.1, 3.5, 1.4, 0.2]}'
```

**Respuesta:**

```json
{"prediction": 0, "clase": "setosa", "probabilities": [0.9808, 0.0192, 0.0]}
```

Si el JSON está mal o no tiene 4 valores, la API responde **400** con un mensaje que explica el formato.

## Cuidado con los costos

- Billing → **Budgets** → crear un "Zero spend budget", para recibir un aviso apenas haya un gasto.
- La URL es pública: cualquiera que la tenga puede llamarla. Al terminar la cursada, borrar la URL o la función.
