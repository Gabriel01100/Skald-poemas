function mostrarPoema(id) {
  const resumen = document.getElementById(`resumen-${id}`);
  const completo = document.getElementById(`completo-${id}`);
  const btn = document.getElementById(`btn-${id}`);

  if (completo.style.display === 'none') {
    completo.style.display = 'block';
    resumen.style.display = 'none';
    btn.textContent = 'Ver menos';
  } else {
    completo.style.display = 'none';
    resumen.style.display = 'block';
    btn.textContent = 'Ver más';
  }
}




// AJAX para los filtros del poema
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('filtro-form');
  const select = document.getElementById('filtro_etiqueta');
  const contenedor = document.getElementById('lista-poemas');

  select.addEventListener('change', () => {
    const valor = select.value;

    fetch(`/filtrar?etiqueta=${encodeURIComponent(valor)}`)
      .then(res => res.text())
      .then(html => {
        contenedor.innerHTML = html;

        document.querySelectorAll('[id^="btn-"]').forEach(btn => {
          const id = btn.id.split('-')[1];
          btn.onclick = () => mostrarPoema(id);
        });
      })
      .catch(err => console.error('Error al filtrar:', err));
  });
});
