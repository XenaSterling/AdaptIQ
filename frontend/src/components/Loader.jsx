/**
 * Módulo: Loader.jsx
 * Descripción: Muestra un mensaje durante la carga de datos
 *              o la ejecución de una operación.
 * Autor: Raquel Del Castillo Pérez
 */


/**
 * Muestra un indicador textual de carga.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {string} [props.text="Loading..."] - Mensaje de carga.
 * @returns {JSX.Element} Elemento con el mensaje de carga.
 */
export default function Loader({
  text = "Loading..."
}) {
  return (
    <div className="loading">
      <p>{text}</p>
    </div>
  );
}