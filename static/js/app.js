// Utilidades generales y helpers para la aplicación web
console.log("[*] NetSec Cifrado iniciado.");

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("Copiado al portapapeles!");
  });
}
