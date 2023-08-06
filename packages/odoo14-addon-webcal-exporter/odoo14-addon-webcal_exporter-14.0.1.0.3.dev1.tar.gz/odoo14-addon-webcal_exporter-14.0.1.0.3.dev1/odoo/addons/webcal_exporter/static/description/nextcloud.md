# Sincronizar calendario de Odoo con Nextcloud

## Obtener URL privada de calendario Nextcloud

1. Inicia sesión en Nextcloud y abre la aplicación de calendario.
2. Haz clic en los tres puntos junto al calendario deseado y selecciona "Copiar enlace privado" para obtener la URL privada.
3. Anota tu nombre de usuario en Nextcloud, que se encuentra en el menú que se despliega en la esquina superior derecha.
4. Ve a "Configuración" > "Seguridad" > "Crear nueva contraseña de aplicación" para generar una contraseña de aplicación. Llámala "odoo" y guárdala en un lugar seguro.

## Configurar el addon `webcal_exporter` en Odoo

1. Instala el addon `webcal_exporter` en tu instancia de Odoo.
2. Ve a tu perfil de usuario en Odoo y selecciona la pestaña "Calendario Nextcloud".
3. Ingresa la URL privada del calendario, el nombre de usuario de Nextcloud y la contraseña de aplicación generada previamente.
4. Comprueba tus credenciales haciendo clic en el botón "Comprobar credenciales" y guarda los cambios.

Ahora, el calendario de Nextcloud se sincronizará con Odoo cada hora.
