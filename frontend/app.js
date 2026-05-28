const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const resultadosDiv = document.getElementById('resultados');
const tablaCuerpo = document.getElementById('tablaCuerpo');
const downloadBtn = document.getElementById('downloadBtn');

let idsActuales = [];

fileInput.addEventListener('change', () => {
    uploadBtn.disabled = fileInput.files.length === 0;
});

uploadBtn.addEventListener('click', async () => {
    const files = fileInput.files;
    if (files.length === 0) return;

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Procesando...';
    resultadosDiv.classList.remove('hidden');

    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://localhost:8000/api/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Error en ' + file.name);
            }

            const data = await response.json();
            idsActuales.push(data.id_registro);
            agregarFilaTabla(data.datos_extraidos);
            actualizarUrlDescarga();

        } catch (error) {
            console.error(error);
            alert(`Error en ${file.name}: ${error.message}`);
        }
    }

    uploadBtn.disabled = false;
    uploadBtn.textContent = 'Procesar PDFs';
    fileInput.value = '';
});

function agregarFilaTabla(datos) {
    const fila = document.createElement('tr');
    fila.innerHTML = `
        <td class="py-2 px-4 border">${datos.nombre_empleado || 'N/A'}</td>
        <td class="py-2 px-4 border">${datos.cedula || 'N/A'}</td>
        <td class="py-2 px-4 border">${datos.eps || 'N/A'}</td>
        <td class="py-2 px-4 border">${datos.fecha_inicio || 'N/A'}</td>
        <td class="py-2 px-4 border">${datos.fecha_fin || 'N/A'}</td>
        <td class="py-2 px-4 border">${datos.dias || 'N/A'}</td>
    `;
    tablaCuerpo.appendChild(fila);
}

function actualizarUrlDescarga() {
    if (idsActuales.length > 0) {
        const params = idsActuales.map(id => `ids=${id}`).join('&');
        downloadBtn.href = `http://localhost:8000/api/export-excel?${params}`;
        downloadBtn.classList.remove('opacity-50', 'pointer-events-none');
    } else {
        downloadBtn.href = '#';
        downloadBtn.classList.add('opacity-50', 'pointer-events-none');
    }
}

actualizarUrlDescarga();