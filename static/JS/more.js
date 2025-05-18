function mostrarPoema(id) {
    document.getElementById('resumen-' + id).style.display = 'none';
    document.getElementById('completo-' + id).style.display = 'block' ;
  }

document.addEventListener('DOMContentLoaded', function(){
  const form = document.getElementById('filtro-form');
  const select = document.getElementById('filtro_etiqueta');
  const contenedor = document.getElementById('lista-poemas');

  select.addEventListener('change', ()=>{
    const valor = select.value; 

    fetch(`/filtrar?etiqueta=${encodeURIComponent(valor)}`)
      .then(res => res.text())
      .then(html =>{
        contenedor.innerHTML = html;
      })
      .catch(err => console.error('Error al filtrar:', err));

  })
})