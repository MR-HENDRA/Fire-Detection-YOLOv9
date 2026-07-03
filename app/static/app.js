/**
 * Fire Detection App — Frontend Logic
 * =====================================
 * Mengatur interaksi drag-and-drop upload, panggilan API deteksi,
 * dan render hasil pada antarmuka web.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ========================
    // Element References
    // ========================
    const tabButtons = document.querySelectorAll('.nav-tab');
    const tabPanels = document.querySelectorAll('.tab-panel');

    const dropzone = document.getElementById('dropzone');
    const dropzoneContent = document.getElementById('dropzone-content');
    const fileInput = document.getElementById('file-input');
    const previewImage = document.getElementById('preview-image');

    const confidenceSlider = document.getElementById('confidence-slider');
    const confidenceValue = document.getElementById('confidence-value');

    const btnDetect = document.getElementById('btn-detect');
    const btnLoader = document.getElementById('btn-loader');
    const btnText = document.querySelector('.btn-text');
    const btnIcon = document.querySelector('.btn-icon');

    const resultPlaceholder = document.getElementById('result-placeholder');
    const resultImageContainer = document.getElementById('result-image-container');
    const resultImage = document.getElementById('result-image');
    const resultStatus = document.getElementById('result-status');
    const detectionStats = document.getElementById('detection-stats');
    const statCount = document.getElementById('stat-count');
    const statAvgConf = document.getElementById('stat-avg-conf');
    const detectionTableWrapper = document.getElementById('detection-table-wrapper');
    const detectionTableBody = document.getElementById('detection-table-body');

    let selectedFile = null;

    // ========================
    // Tab Navigation
    // ========================
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.dataset.tab;

            // Update active tab button
            tabButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Show target panel
            tabPanels.forEach(panel => panel.classList.remove('active'));
            document.getElementById(`panel-${targetTab}`).classList.add('active');

            // Lazy load dataset stats when tab is clicked
            if (targetTab === 'stats') {
                loadDatasetStats();
            }
        });
    });

    // ========================
    // Dropzone & File Upload
    // ========================
    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-over');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('drag-over');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('⚠️ Mohon pilih file gambar (JPG, PNG, WEBP).');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('⚠️ Ukuran file terlalu besar! Maksimum 10MB.');
            return;
        }

        selectedFile = file;

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            previewImage.classList.remove('hidden');
            dropzoneContent.classList.add('hidden');
        };
        reader.readAsDataURL(file);

        // Enable detect button
        btnDetect.disabled = false;

        // Reset results
        resetResults();
    }

    // ========================
    // Confidence Slider
    // ========================
    confidenceSlider.addEventListener('input', () => {
        confidenceValue.textContent = `${confidenceSlider.value}%`;
    });

    // ========================
    // Detection
    // ========================
    btnDetect.addEventListener('click', async () => {
        if (!selectedFile) return;

        // Show loading state
        setLoading(true);

        try {
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('confidence', (parseInt(confidenceSlider.value) / 100).toString());

            const response = await fetch('/api/detect', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                displayResults(data.data);
            } else {
                resultStatus.textContent = `❌ Error: ${data.error}`;
                resultStatus.style.color = '#ff4444';
            }
        } catch (error) {
            resultStatus.textContent = `❌ Koneksi gagal: ${error.message}`;
            resultStatus.style.color = '#ff4444';
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            btnDetect.classList.add('loading');
            btnDetect.disabled = true;
            btnText.textContent = 'Memproses...';
            btnIcon.classList.add('hidden');
            btnLoader.classList.remove('hidden');
            resultStatus.textContent = '⏳ Sedang memproses gambar dengan AI...';
            resultStatus.style.color = '';
        } else {
            btnDetect.classList.remove('loading');
            btnDetect.disabled = false;
            btnText.textContent = 'Mulai Deteksi';
            btnIcon.classList.remove('hidden');
            btnLoader.classList.add('hidden');
        }
    }

    function displayResults(data) {
        // Hide placeholder, show result image
        resultPlaceholder.classList.add('hidden');
        resultImageContainer.classList.remove('hidden');
        resultImage.src = `data:image/jpeg;base64,${data.annotated_image_base64}`;

        // Update stats
        detectionStats.classList.remove('hidden');
        statCount.textContent = data.count;

        if (data.count > 0) {
            const avgConf = data.detections.reduce((sum, d) => sum + d.confidence, 0) / data.count;
            statAvgConf.textContent = `${avgConf.toFixed(1)}%`;
            resultStatus.textContent = `🔥 ${data.count} api terdeteksi!`;
            resultStatus.style.color = '#ff7800';
        } else {
            statAvgConf.textContent = '—';
            resultStatus.textContent = '✅ Tidak ada api terdeteksi.';
            resultStatus.style.color = '#22c55e';
        }

        // Build detection table
        if (data.count > 0) {
            detectionTableWrapper.classList.remove('hidden');
            detectionTableBody.innerHTML = '';

            data.detections.forEach((det, idx) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${idx + 1}</td>
                    <td style="color: var(--fire-orange); font-weight: 600;">🔥 ${det.label}</td>
                    <td style="color: var(--accent-green); font-weight: 700;">${det.confidence}%</td>
                    <td style="font-family: monospace; font-size: 12px;">(${det.x1}, ${det.y1}, ${det.x2}, ${det.y2})</td>
                `;
                detectionTableBody.appendChild(row);
            });
        } else {
            detectionTableWrapper.classList.add('hidden');
        }
    }

    function resetResults() {
        resultPlaceholder.classList.remove('hidden');
        resultImageContainer.classList.add('hidden');
        detectionStats.classList.add('hidden');
        detectionTableWrapper.classList.add('hidden');
        resultStatus.textContent = 'Menunggu gambar untuk diproses...';
        resultStatus.style.color = '';
    }

    // ========================
    // Dataset Stats (Lazy Load)
    // ========================
    let statsLoaded = false;

    async function loadDatasetStats() {
        if (statsLoaded) return;

        try {
            const response = await fetch('/api/dataset-stats');
            const data = await response.json();

            if (data.success) {
                const stats = data.data;
                document.getElementById('ds-train-img').textContent = stats.train.images.toLocaleString();
                document.getElementById('ds-train-lbl').textContent = stats.train.labels.toLocaleString();
                document.getElementById('ds-valid-img').textContent = stats.valid.images.toLocaleString();
                document.getElementById('ds-valid-lbl').textContent = stats.valid.labels.toLocaleString();
                document.getElementById('ds-test-img').textContent = stats.test.images.toLocaleString();
                document.getElementById('ds-test-lbl').textContent = stats.test.labels.toLocaleString();
                statsLoaded = true;
            }
        } catch (error) {
            console.error('Gagal memuat statistik dataset:', error);
        }
    }

    // ========================
    // Allow re-upload by clicking preview
    // ========================
    previewImage.addEventListener('click', (e) => {
        e.stopPropagation();
        previewImage.classList.add('hidden');
        dropzoneContent.classList.remove('hidden');
        selectedFile = null;
        btnDetect.disabled = true;
        fileInput.value = '';
        resetResults();
    });
});
