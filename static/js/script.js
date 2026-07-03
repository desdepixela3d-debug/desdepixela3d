let productos = document.querySelectorAll('.producto');

productos.forEach(function(producto) {
  producto.addEventListener('click', function() {

    let detalle = producto.querySelector('.detalle');
    let estaAbierto = detalle.style.display === 'block';

    // Primero cerrá y desresaltá todos
    productos.forEach(function(p) {
      p.style.backgroundColor = '#633806';
      p.querySelector('.detalle').style.display = 'none';
    });

    // Si estaba cerrado, abrilo y resaltalo
    // Si estaba abierto, quedó cerrado con el paso anterior
    if (!estaAbierto) {
      detalle.style.display = 'block';
      producto.style.backgroundColor = '#854F0B';
    }

  });
});