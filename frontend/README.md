# Frontend

- Aplicación web desarrollada con React y Vite para la autenticación de usuarios y la gestión de evaluaciones, recomendaciones y recursos educativos.
- Autor: rdelcasti26@alumno.uned.es

## Tecnologías

- **React 19**: Interfaz de usuario.
- **Vite 8**: Servidor de desarrollo y herramienta de compilación.
- **React Router 7**: Navegación y gestión de rutas.
- **Axios**: Comunicación HTTP con el backend.
- **JWT Decode**: Lectura de tokens JWT.
- **Chart.js y react-chartjs-2**: Representación de datos mediante gráficos.
- **i18next y react-i18next**: Internacionalización.
- **ESLint**: Análisis estático del código.

## Funcionalidades

- **Autenticación:** Inicio y cierre de sesión mediante tokens JWT.
- **Dashboard:** Página principal con información relevante para el usuario.
- **Evaluaciones:** Acceso a evaluaciones y consulta de resultados.
- **Recomendaciones:** Consulta de recomendaciones personalizadas.
- **Gestión de preguntas:** Sección para profesorado y administradores.
- **Recursos educativos:** Consulta y gestión de recursos.
- **Gestión de usuarios:** Administración de usuarios según los permisos asignados.

El acceso a determinadas rutas está protegido según el estado de autenticación y el rol del usuario.

## Requisitos previos

- Node.js y npm.
- Acceso al backend de la aplicación, cuando sea necesario.

## Instalación y ejecución

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd frontend
```
Instalar las dependencias:

```bash
npm install
```

Iniciar el servidor de desarrollo:

```bash
npm run dev
```
Vite mostrará en la terminal la dirección local para acceder a la aplicación.

## Comandos disponibles

| Comando | Descripción |
|---|---|
| `npm run dev` | Inicia el servidor de desarrollo. |
| `npm run build` | Genera la versión de producción en `dist/`. |
| `npm run preview` | Permite comprobar localmente la versión compilada. |
| `npm run lint` | Ejecuta ESLint para analizar el código. |

## Compilación

Generar la versión de producción:

```bash
npm run build
```
Los archivos generados se guardan en el directorio dist/.

La configuración de Vite utiliza una ruta base relativa (base: './'), lo que facilita servir los recursos desde distintas ubicaciones.

## Autenticación

- La autenticación se gestiona mediante un contexto de React (AuthContext).
- El token JWT se almacena en localStorage y permite recuperar el estado de la sesión. La aplicación obtiene del token el identificador y el rol del usuario para gestionar el acceso a las distintas secciones.
- La autorización efectiva de las operaciones debe validarse también en el backend.

## Archivos de traducción JSON

La carpeta `i18n` contiene los archivos de configuración e internacionalización de la aplicación, permitiendo mostrar la interfaz en español e inglés mediante las librerías `i18next` y `react-i18next`.

### Estructura de los archivos

Los archivos JSON se organizan en dos subcarpetas, una para cada idioma:

- `es/`: contiene las traducciones al español.
- `en/`: contiene las traducciones al inglés.

Cada subcarpeta contiene archivos JSON que agrupan las traducciones según la funcionalidad de la aplicación:

| Archivo | Descripción |
|---|---|
| `common.json` | Textos comunes, mensajes generales, botones, estados y etiquetas de tablas. |
| `dashboard.json` | Títulos, indicadores, niveles de competencia y textos de los paneles de estudiante, profesor y administrador. |
| `tooltips.json` | Descripciones de ayuda para los indicadores y gráficos de los paneles. |
| `login.json` | Textos de la pantalla de inicio de sesión. |
| `teacher.json` | Traducciones de la gestión de preguntas y recursos educativos por parte del profesor. |
| `admin.json` | Textos de la gestión de usuarios y sus roles. |
| `evaluation.json` | Textos relacionados con las evaluaciones, los resultados y el rendimiento académico. |
| `recommendations.json` | Textos de las recomendaciones personalizadas de preguntas y recursos educativos. |
| `navbar.json` | Etiquetas de navegación del menú principal. |
| `questions.json` | Traducciones de preguntas y respuestas utilizadas en la aplicación. |

### Funcionamiento

El archivo `index.js` importa los archivos JSON de ambos idiomas y los registra en la configuración de `i18next`, agrupándolos en espacios de nombres (*namespaces*).

El idioma inicial se determina siguiendo este orden:

1. Se utiliza el idioma guardado en `localStorage`, si existe.
2. Si no hay ninguna preferencia guardada, se comprueba el idioma del navegador.
3. Si el navegador utiliza español o inglés, se selecciona el idioma correspondiente.
4. Para cualquier otro idioma, se establece el español como idioma predeterminado.

Además, se configura el español como idioma de reserva (`fallbackLng`), de modo que se utilice cuando no esté disponible una traducción en el idioma activo.

Los componentes de React acceden a las traducciones mediante el hook `useTranslation`, indicando el espacio de nombres correspondiente cuando es necesario. Por ejemplo:

\`\`\`jsx
const { t } = useTranslation("admin");

<h1>{t("title")}</h1>
\`\`\`

En este caso, la clave `title` se obtiene del archivo `admin.json` correspondiente al idioma activo.

El hook personalizado `useLanguage.js` permite consultar el idioma actual y cambiarlo desde la aplicación. Cuando se selecciona un nuevo idioma, se actualiza la configuración de `i18next` y se guarda la preferencia en `localStorage`.

### Mantenimiento de las traducciones

Para añadir o modificar traducciones, se deben seguir estas pautas:

- Mantener las mismas claves en los archivos JSON equivalentes de español e inglés.
- Utilizar claves descriptivas y organizadas por secciones para facilitar su identificación.
- Registrar los nuevos archivos de traducción en `index.js`, tanto para español como para inglés, e incluir sus espacios de nombres en la configuración.
- Acceder a los textos mediante `t("clave")` en lugar de escribir directamente los textos de la interfaz en los componentes.
- Respetar la sintaxis JSON, incluyendo las comillas dobles, las comas y la estructura de los objetos.
- Utilizar interpolación para los textos que incluyan valores dinámicos, como `{{step}}` o `{{tag}}`.

Esta organización centraliza los textos de la interfaz, facilita el mantenimiento de las traducciones y permite incorporar nuevos idiomas sin tener que modificar directamente los textos de cada componente.


## React + Vite BASIC README INFO

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

### React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

### Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
