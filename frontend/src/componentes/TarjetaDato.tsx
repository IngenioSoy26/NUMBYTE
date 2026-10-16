function TarjetaDato({ etiqueta, valor }: { etiqueta: string; valor: string | number }) {
  return (
    <div className="tarjeta-dato">
      <span>{etiqueta}</span>
      <strong>{valor}</strong>
    </div>
  )
}

export default TarjetaDato
