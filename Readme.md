# Aplicación de Cobranzas

## Roles y facultades de cada tipo de usuario
La aplicación te permite ejecutar los siguientes roles:
- Administrador: puede ver todos los agendamientos asociados a un profesional incluyendo el estado de pago de estos; puede marcar como pagado o no pagado cualquier agendamiento de un profesional; se puede registrar desde el inicio de la aplicación; se puede loguear con sus credenciales desde el inicio de la aplicación.
- Cliente: puede ver todos sus agendamientos junto al nombre del profesional al que se asocia cada uno; uede pagar cada uno de estos agendamientos. Este pago tiene una 80% de probabilidad de ser exitoso y 20% de probabilidad de ser rechazado, y tanto el pago exitoso como el pago rechazado te redirigen a una vista atingente al resultado de la operación. Además, se puede registrar desde el inicio de la aplicación; y se puede loguear con sus credenciales desde el inicio de la aplicación.
- Profesional: puede ver todos sus agendamientos incluyendo el estado de pago de estos junto al nombre del cliente al que se asocia cada uno; y puede marcar como pagado o no pagado cada uno de estos agendamientos. 


## Instalación

1. **Clonar el repositorio**
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto

2. **Configurar el entorno virtual**
    python3 -m venv env
    . env/bin/activate

3. **Instalar dependencias**
    pip3 install -r requirements.txt

4. **Resetear base de datos, ejecutar migraciones y crear usuario administrador de Django**
    make reset

5. **Poblar la base de datos local con data definida en el archivo populate_local_db situado en la raíz del repositorio**
    make populate

6. **Ejecutar aplicación**
    make run


## Consideraciones adicionales del proyecto
- Se utilizó Tailwind CSS para el manejo de estilos.
- Se crearon los modelos Professional, Customer, Scheduling y Payment para modelar las especificaciones pedidas a nivel de lógica de la aplicación y manejo de la base de datos.
- Para simular el pago exitoso o rechazado de un agendamiento, se utilizó una función que da un 80% de probabilidad al pago exitoso y un 20% de probabilidad al pago rechazado.
- Se permite registrar administradores, clientes y profesionales.
- Se permite loguear a cualquiera de los roles anteriores con las credenciales seteadas en sus respectivos registros.
- Cuando se desee dejar de correr el entorno virtual, ejecutar `deactivate`
- Se puede pagar tanto en pesos chilenos como en dólares estadounidenses (moneda extranjera). La conversión de dolar a peso considera que 1 dolar estadounidense = 926 pesos chilenos.


## Puntos que faltó abordar
- Hacer un deploy de la aplicación.
- Restringir el acceso a las distintas vistas según un correcto manejo de autorización de permisos por cada rol (administrador, cliente y profesional).