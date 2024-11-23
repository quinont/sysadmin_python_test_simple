
# IMPORTANTE:

ESTO ESTA EN CONSTRUCCION, POR FAVOR NO ME'KEME


# Revisión de ConfigMaps en Kubernetes

## Propósito
- Desarrollar un script que verifique si ciertos ConfigMaps con un label particular, distribuidos en varios namespaces, cumplen con un formato esperado. Si no lo cumplen, actualizar su contenido.

## Detalles sobre los ConfigMaps
- **Distribución:** Los ConfigMaps están distribuidos en múltiples namespaces.  
- **Label relevante:** Solo se deben modificar los ConfigMaps que tienen el label `syntax-checking` con un valor `true`.  
  - Si no tienen este label o su valor no es `true`, se deben ignorar.  
- **Tipos de configuración:** Cada ConfigMap tiene un label adicional llamado `config-type`, que define su tipo de contenido.  

### Validaciones según el `config-type`:
1. **ConfigMaps tipo "file":**
   - No deben contener líneas vacías en su contenido.
   - Solo pueden tener **una configuración**, que corresponde a un archivo.
   - ConfigMaps con más de un archivo o sin ninguno no son válidos. 
        - En caso de tener mas de un archivo, solo dejar el primero.
        - En caso de no tener ninguna entrada, generar una que se llame index.html con una sola linea que diga "archivo nuevo"

2. **ConfigMaps tipo "env":**
   - Las claves (nombres) deben estar en **MAYÚSCULAS**.
   - Los valores no deben contener saltos de línea.
   - Pueden incluir múltiples configuraciones, pero no deben estar vacíos.
       - En caso de estar vacios, generar una entrada con nombre "CLAVE" y valor "MI VALOR"

## Registro de modificaciones
- Cada vez que se realiza una modificación, se debe registrar en un log con el nombre del ConfigMap afectado.
    - No es necesario indicar que se modifico, como quedo el configmap ni tampoco cual fue el error. 

---

## Cambios importantes y solicitudes adicionales

### 1. **Mejorar el manejo de errores**
   - Los errores actuales son poco claros. Se debe refactorizar el script para mostrar mensajes de error más informativos, indicando el problema exacto (cual fue el error que se tubo) y el ConfigMap afectado.

### 2. **Compatibilidad con Argo CD**
   - Se identificó que en entornos gestionados por Argo CD, las modificaciones directas en los ConfigMaps son revertidas automáticamente.
   - **Solución:**  
     - Crear un modo adicional en el script para trabajar con archivos YAML estáticos.  
     - Estos archivos estarán organizados en carpetas por namespace, y cada archivo representará un ConfigMap en formato YAML.  
     - **Nuevo comportamiento:**  
       - Agregar un flag al script que permita especificar si se trabajará directamente en el clúster de Kubernetes o con archivos YAML.  
       - Si se selecciona el modo YAML, el flag también debe indicar la ubicación de las carpetas correspondientes.

### 3. **Reiniciar el Deployment tras una modificación**
   - Para los casos de modificación directa en Kubernetes, se debe reiniciar el Deployment asociado al ConfigMap afectado.  
   - **Preguntas pendientes:**  
     - ¿Cómo se puede manejar este caso en entornos con Argo CD? ¿Es posible automatizar el proceso de reinicio del Deployment desde Argo CD?

### 4. **Notificaciones en Slack**
   - Cada vez que se aplique un cambio, ya sea en Kubernetes o en archivos YAML para Argo CD, se debe enviar una notificación a Slack.  
   - La notificación debe incluir:
     - Tipo de modificación (Kubernetes directo o YAML estático).
     - Nombre del ConfigMap modificado.

### 5. **Integración con Jira**
   - Para registrar los cambios en el backlog, se debe crear un ticket automáticamente en Jira cada vez que se aplique una modificación.  
   - **Detalles del ticket:**
     - Tipo de cambio: Kubernetes directo o YAML para Argo CD.
     - Nombre del ConfigMap.
     - El dashboard donde se debe crear el ticket estará especificado en un label del ConfigMap.  

---

## Próximos pasos
- Refactorizar el script actual para integrar las nuevas funcionalidades progresivamente.
- Establecer un plan para gestionar las validaciones, notificaciones, y el manejo dual (Kubernetes y YAML estático).
- Diseñar pruebas unitarias y de integración para garantizar la calidad del código y cubrir todos los casos de uso.

