document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');
    const fileNameDisplay = document.getElementById('file-name');

    // Drag & Drop handlers
    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    let currentFile = null;

    function handleFile(file) {
        if (!file.name.endsWith('.py')) {
            alert('Please upload a Python (.py) file.');
            return;
        }
        currentFile = file;
        fileNameDisplay.textContent = `Selected: ${file.name}`;
        analyzeBtn.disabled = false;

        // Reset results
        resultsSection.classList.add('hidden');
    }

    // Analyze Click
    analyzeBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        analyzeBtn.innerText = 'Analyzing...';
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                renderResults(data.results);
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        } finally {
            analyzeBtn.innerHTML = '<i class="ri-radar-line"></i> Run Analysis';
            analyzeBtn.disabled = false;
        }
    });

    function renderResults(results) {
        resultsSection.classList.remove('hidden');
        document.getElementById('status-badge').innerText = 'Complete';

        const vulnList = document.getElementById('vuln-list');
        const safeList = document.getElementById('safe-list');

        vulnList.innerHTML = '';
        safeList.innerHTML = '';

        // Add Vulnerabilities
        if (results.vulnerabilities && results.vulnerabilities.length > 0) {
            results.vulnerabilities.forEach(msg => {
                const li = document.createElement('li');
                li.innerText = msg.replace('⚠️', '').trim();
                vulnList.appendChild(li);
            });
            document.getElementById('vuln-card').style.display = 'block';
        } else {
            const li = document.createElement('li');
            li.innerText = 'No vulnerabilities detected.';
            li.style.color = '#fff';
            li.style.borderLeftColor = '#aaa';
            vulnList.appendChild(li);
        }

        // Add Safe checks
        if (results.safe && results.safe.length > 0) {
            results.safe.forEach(msg => {
                const li = document.createElement('li');
                li.innerText = msg.replace('✅', '').trim();
                safeList.appendChild(li);
            });
        }
    }
});
