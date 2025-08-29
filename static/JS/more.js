document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('filtro-form');
  const select = document.getElementById('filtro_etiqueta');
  const contenedor = document.getElementById('lista-poemas');

  function activarBotones() {
    document.querySelectorAll('[id^="btn-"]').forEach(btn => {
      const id = btn.id.split('-')[1];
      btn.onclick = () => mostrarPoema(id);
     });
   }

  select.addEventListener('change', () => {
    const valor = select.value;

    fetch(`/filtrar?etiqueta=${encodeURIComponent(valor)}`)
      .then(res => res.text())
      .then(html => {
        contenedor.innerHTML = html;
        activarBotones(); // reactivar eventos después del render
      })
       .catch(err => console.error('Error al filtrar:', err));
         });

   activarBotones(); // activar al inicio también
 });

// function mostrarPoema(id) {
//   const resumen = document.getElementById(`resumen-${id}`);
//   const completo = document.getElementById(`completo-${id}`);
//   const btn = document.getElementById(`btn-${id}`);
//   if (completo.style.display === 'none') {
//     completo.style.display = 'block';
//     resumen.style.display = 'none';
//     btn.textContent = 'Ver menos';
//   } else {
//     completo.style.display = 'none';
//     resumen.style.display = 'block';
//     btn.textContent = 'Ver más';
//   }
// }

document.addEventListener('DOMContentLoaded', function () {
  // Delegación de eventos para cualquier botón con la clase .btn-ver-mas
  document.body.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-ver-mas')) {
      const boton = e.target;
      const article = boton.closest('article');
      const resumen = article.querySelector('[id^="resumen-"]');
      const completo = article.querySelector('[id^="completo-"]');

      if (completo.style.display === 'none' || completo.style.display === '') {
        completo.style.display = 'block';
        resumen.style.display = 'none';
        boton.textContent = 'Ver menos';
      } else {
        completo.style.display = 'none';
        resumen.style.display = 'block';
        boton.textContent = 'Ver más';
      }
    }
  });
});
