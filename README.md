# portfolio-rest-abaqus
Prueba técnica Abaqus DRF para manejar portafolios de inversión.

# Preguntas realizadas

Se realizaron las preguntas de la 1 a la 4 (sin Bonus 1-2). También se vió el video de Django-Styleguide de HackSoft y se utilizó el patrón de services usando transactions, type hints y only keyword arguments (muy interesante el video, aprendí mucho).

# Setup

1. Instalar dependencias (en su entorno virtual favorito):
```bash
pip install -r requirements.txt
```
2. Aplicar migraciones:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
3. Seedear la base de datos con weights y precios (se puede dar --file-path si se desea para dar una ruta diferente):
```bash
python manage.py load_weights_prices
```
4. Calcular los cantidades iniciales:
```bash
python manage.py calculate_initial_quantities
```
5. Iniciar el servidor:
```bash
python manage.py runserver
```
6. Probar la API (portafolios disponibles: "portafolio 1", "portafolio 2"):
```bash
curl "http://127.0.0.1:8000/api/v1/portfolio-metrics/?fecha_inicio=2022-02-15&fecha_fin=2023-02-16&portfolio=portafolio%201"
```
# Estilo del código
Se siguió el estilo de código de HackSoft dentro de lo posible y se utilizó Black para formatear el código. También se utilizó isort para ordenar las importaciones.

# TODOS o Cosas que me hubiera gustado hacer

En el código dejé TODOS sin completar, pero básicamente son cosas que me hubiera gustado hacer si tuviera más tiempo. Algunas de ellas son:
- Páginar la API y crear serializers
- Hacer constraints en la base de datos
- Añadir deleted_at (aunque no era necesario aquí ya que no hay mutation methods)
- Añadir tests
- Dockerizar la aplicación
- Añadir un README más completo.
- Añadir pre-commit hooks para formatear el código y hacer linting.