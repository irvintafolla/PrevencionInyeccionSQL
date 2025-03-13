/*!
* Start Bootstrap - Creative v7.0.7 (https://startbootstrap.com/theme/creative)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});


document.addEventListener('DOMContentLoaded', function () {
    
    const API_URL = "https://prevencioninyeccionsql.onrender.com";
    //const API_URL = "http://127.0.0.1:8000";
    let lastResult = null;


    document.getElementById("btn-analizar").addEventListener("click", subirArchivo);
    document.getElementById("btn-descargar-zip").addEventListener("click", descargarZip);
    document.getElementById("verResultadosbtn").addEventListener("click", mostrarResultados);
    

    function ShowLoading() {
        document.getElementById("loading").style.display = "flex";
    }

    function HideLoading() {
        document.getElementById("loading").style.display = "none";
    }

    async function subirArchivo() {
        let input = document.getElementById("fileInput");
        let resultado = document.getElementById("resultado");
        let verResultadosbtn = document.getElementById("verResultadosbtn");

        if (input.files.length === 0) {
            alert("Seleccione un archivo antes de verificar el código.");
            return;
        }

        ShowLoading();
        verResultadosbtn.style.display = "none";

        let formData = new FormData();
        formData.append("file", input.files[0]);

        try {
            let response = await fetch(`${API_URL}/analizar/`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                let errorText = await response.text();
                throw new Error(`Error en la API: ${response.status} - ${errorText}`);
            }

            let data = await response.json();
            lastResult = data;

            setTimeout(() => {
                HideLoading();
                verResultadosbtn.style.display = "block";
                formatRecommendations(data);
            }, 3000);

        } catch (error) {
            console.error("Error:", error);
            resultado.textContent = "Error: " + error;
            HideLoading();
        }
    }

    function mostrarResultados() {
        let jsonDoc = new Blob([JSON.stringify(lastResult, null, 4)], { type: "application/json" });
        let url = document.createElement("a");
        url.href = URL.createObjectURL(jsonDoc);
        url.download = "resultado.json";
        url.click();
    }

    function formatRecommendations(data) {
        let resultadoContainer = document.getElementById("resultado-container");
        let resultado = document.getElementById("resultado");

        resultado.innerHTML = "";
        resultadoContainer.style.display = "flex";

        if (data.resultado === "Tu codigo es seguro") {
            let card = document.createElement("div");
            card.style.border = "1px solid #ccc";
            card.style.padding = "15px";
            card.style.margin = "10px 0"; /* Margen vertical */
            card.style.borderRadius = "8px";
            card.style.backgroundColor = "#f9f9f9";
            card.style.boxShadow = "2px 2px 5px rgba(0,0,0,0.1)";
            card.style.width = "90%"; /* Ocupa todo el ancho disponible */
            card.style.maxWidth = "1000px"; /* Establece un ancho máximo */
            card.style.textAlign = "left"; /* Alinea el texto a la izquierda dentro de la tarjeta */
        
            let mensaje = document.createElement("p");
            mensaje.style.color = "green";
            mensaje.style.fontWeight = "bold";
            mensaje.textContent = data.resultado;
        
            let explicacion = document.createElement("p");
            explicacion.textContent = "No se encontraron vulnerabilidades conocidas.";
        
            card.appendChild(mensaje);
            card.appendChild(explicacion);
            resultado.appendChild(card);
            return;
        }

        if (!data.recomendaciones || data.recomendaciones.length === 0) {
            let card = document.createElement("div");
            card.style.border = "1px solid #ccc";
            card.style.padding = "15px";
            card.style.margin = "10px 0"; /* Margen vertical */
            card.style.borderRadius = "8px";
            card.style.backgroundColor = "#f9f9f9";
            card.style.boxShadow = "2px 2px 5px rgba(0,0,0,0.1)";
            card.style.width = "90%"; /* Ocupa todo el ancho disponible */
            card.style.maxWidth = "1000px"; /* Establece un ancho máximo */
            card.style.textAlign = "left"; /* Alinea el texto a la izquierda dentro de la tarjeta */
        
            let mensaje = document.createElement("p");
            mensaje.style.color = "green";
            mensaje.style.fontWeight = "bold";
            mensaje.textContent = data.resultado;
        
            let explicacion = document.createElement("p");
            explicacion.textContent = "No se encontraron vulnerabilidades conocidas.";
        
            card.appendChild(mensaje);
            card.appendChild(explicacion);
            resultado.appendChild(card);
            return;
        }

        data.recomendaciones.forEach((rec) => {
            let card = document.createElement("div");
            card.style.border = "1px solid #ccc";
            card.style.padding = "15px";
            card.style.margin = "10px auto"; // Centra la tarjeta horizontalmente
            card.style.borderRadius = "8px";
            card.style.backgroundColor = "#f9f9f9";
            card.style.boxShadow = "2px 2px 5px rgba(0,0,0,0.1)";
            card.style.width = "90%"; // Asegura que la tarjeta no sea demasiado ancha
            card.style.maxWidth = "1000px"; // Establece un ancho máximo para la tarjeta
            card.style.textAlign = "left"; // Alinea el texto a la izquierda dentro de la tarjeta
        
            let mensaje = document.createElement("h3");
            mensaje.style.color = "#D9534F";
            mensaje.textContent = rec.mensaje;
        
            let explicacion = document.createElement("p");
            explicacion.style.color = "#5A5A5A";
            explicacion.textContent = rec.explicacion || "No se proporcionó explicación.";
        
            let codeBlock = document.createElement("pre");
            codeBlock.style.backgroundColor = "#272822";
            codeBlock.style.color = "#FFF";
            codeBlock.style.padding = "10px";
            codeBlock.style.borderRadius = "5px";
            codeBlock.style.overflowX = "auto";
            codeBlock.textContent = rec.ejemplo_corregido;
        
            card.appendChild(mensaje);
            card.appendChild(explicacion);
            card.appendChild(codeBlock);
            resultado.appendChild(card);
        });
    }

    async function descargarZip() {
        let Zip = document.getElementById("Zip").value;

        ShowLoading();

        try {
            let response = await fetch(`${API_URL}/Obtener_Recomendaciones/?tipo=${Zip}`, {
                method: 'GET'
            });

            if (!response.ok) {
                let errorText = await response.text();
                throw new Error(`Error en la API: ${response.status} - ${errorText}`);
            }

            let blob = await response.blob();
            let url = window.URL.createObjectURL(blob);
            let a = document.createElement("a");
            a.href = url;
            a.download = `Recomendaciones_${Zip}.zip`;
            document.body.appendChild(a);
            HideLoading();
            a.click();
            document.body.removeChild(a);

        } catch (error) {
            console.error("Error:", error);
            alert("Error descargando el archivo: " + error.message);
            HideLoading();
        }
    }    
});
