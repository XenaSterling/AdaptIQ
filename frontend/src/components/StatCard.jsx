/**
 * Módulo: StatCard.jsx
 * Descripción: Muestra una tarjeta con el título y el valor
 *              de una estadística, junto con información opcional.
 * Autor: Raquel Del Castillo Pérez
 */


/**
 * Renderiza una tarjeta estadística.
 *
 * @param {Object} props - Propiedades del componente.
 * @param {string} props.title - Título de la estadística.
 * @param {string|number} props.value - Valor de la estadística.
 * @param {string} [props.tooltip] - Texto informativo opcional.
 * @returns {JSX.Element} Tarjeta con la información estadística.
 */
export default function StatCard({
  title,
  value,
  tooltip
}) {
  return (
    <div className="card">
      <h3
        style={{
          display: "flex",
          alignItems: "center",
          gap: "6px",
          marginTop: 0
        }}
      >
        {title}

        {tooltip && (
          <span
            className="info-icon"
            title={tooltip}
          >
            ⓘ
          </span>
        )}
      </h3>

      <p
        style={{
          fontSize: "28px",
          fontWeight: "bold",
        }}
      >
        {value}
      </p>
    </div>
  );
}