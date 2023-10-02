const dropZone = document.getElementById('drop-zone');
const result = document.getElementById('result');

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.border = '2px dashed #000';
});

dropZone.addEventListener('dragleave', () => {
    dropZone.style.border = '2px dashed #ccc';
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.border = '2px dashed #ccc';

    const files = e.dataTransfer.files;
    const formData = new FormData();

    for (const file of files) {
        formData.append('csv_files', file);
    }

    fetch('/upload', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        const preElement = document.createElement('pre');
        preElement.textContent = data.message;
        result.innerHTML = '';
        result.appendChild(preElement);
    });
    
});
