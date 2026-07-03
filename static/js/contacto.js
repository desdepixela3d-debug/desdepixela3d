let btnEnviar = document.getElementById('btnEnviar');

btnEnviar.addEventListener('click', function() {

  let nombre = document.getElementById('nombre').value.trim();
  let email = document.getElementById('email').value.trim();
  let mensaje = document.getElementById('mensaje').value.trim();

  // Validar que todos los campos estén completos
  if (nombre === '' || email === '' || mensaje === '') {
    alert('Por favor completá todos los campos antes de enviar.');
    return;
  }

  // Validar formato de email
  if (!email.includes('@') || !email.includes('.')) {
    alert('Por favor ingresá un email válido.');
    return;
  }

  // Si todo está bien, mostrar confirmación
  document.getElementById('confirmacion').style.display = 'block';
  btnEnviar.style.display = 'none';

});