function handleSelect(dni)
{
  var url = "liquidacion/0".replace('0', dni);
  nueva = window.location.href.replace('agentes_a_cargo', url)
  window.location.href = nueva;
}

function handleSelect(dni)
{
  var url = "{% url 'liquidaciones_agente' documento=0 %}".replace('0', dni);
  window.location.href = url;
}
