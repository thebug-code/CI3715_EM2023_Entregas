# Iteracion 1

## Plan de iteracion

- Como Usuario, puedo Generar diferentes proyectos automotrices en el Sistema para Gestionar el Portafolio de Proyectos de un Taller Automotriz en Particular (Épica).

  - Como Gerente, puedo Ingresar los parámetros de un Proyecto en el Sistema para Gestionar el Portafolio de Proyectos de un Taller Automotriz en Particular (INVEST).
    ​

### Nota

- Los datos de los Proyectos son ID, Descripción, Inicio (Fecha) y Cierre (Fecha).

---

- Como Sistema, puedo Registrar los diferentes eventos del sistema en un Logger para Auditar el Sistema (Historia).

### Nota

- Registrar implica agregar, buscar y eliminar eventos. El Logger (bitácora) esta conformada por el Usuario que genero el evento, el evento, fecha, hora. Los eventos que se deben generar son agregar, buscar, modificar, eliminar, etc. En vista que los eventos del sistema ocurren en los diferentes módulos del sistema. El Logger (bitácora) de eventos debe agregarse en las líneas de código donde estas ocurren p.e. agregar, eliminar y modificar usuario.
