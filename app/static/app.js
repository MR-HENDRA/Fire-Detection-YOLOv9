/**
 * Fire Detection App — Professional Frontend Logic
 * =================================================
 * Mengatur interaksi drag-and-drop upload, panggilan API deteksi,
 * animasi smooth, toast notifications, dan render hasil.
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

  const toast = document.getElementById('toast');

  let selectedFile = null;

  // ========================
  // Toast Notification System
  // ========================
  function showToast(message, type = 'success', duration = 3000) {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');

    setTimeout(() => {
      toast.classList.remove('show');
    }, duration);
  }

  // ========================
  // Tab Navigation
  // ========================
  tabButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetTab = btn.dataset.tab;

      // Update active tab button
      tabButtons.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');

      // Show target panel
      tabPanels.forEach((panel) => panel.classList.remove('active'));
      document.getElementById(`panel-${targetTab}`).classList.add('active');

      // Lazy load dataset stats and model info when tab is clicked
      if (targetTab === 'stats') {
          loadDatasetStats();
          loadModelInfo();
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
      showToast('⚠️ Mohon pilih file gambar (JPG, PNG, WEBP).', 'error');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      showToast('⚠️ Ukuran file terlalu besar! Maksimum 10MB.', 'error');
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

    // Show success toast
    showToast(`✅ Gambar "${file.name}" siap diproses!`);
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
        showToast(`✅ Deteksi selesai! ${data.data.count} api ditemukan.`, 'success');
      } else {
        resultStatus.textContent = `❌ Error: ${data.error}`;
        resultStatus.style.color = '#ff4444';
        showToast(`❌ Error: ${data.error}`, 'error');
      }
    } catch (error) {
      resultStatus.textContent = `❌ Koneksi gagal: ${error.message}`;
      resultStatus.style.color = '#ff4444';
      showToast(`❌ Koneksi gagal: ${error.message}`, 'error');
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

      // Build detection table
      detectionTableWrapper.classList.remove('hidden');
      detectionTableBody.innerHTML = '';

      data.detections.forEach((det, idx) => {
        const row = document.createElement('tr');
        row.innerHTML = `
                    <td>${idx + 1}</td>
                    <td style="color: var(--fire-orange); font-weight: 600;">🔥 ${det.label}</td>
                    <td style="color: var(--accent-green); font-weight: 700;">${det.confidence}%</td>
                    <td style="font-family: var(--font-mono); font-size: 12px;">(${det.x1}, ${det.y1}, ${det.x2}, ${det.y2})</td>
                `;
        detectionTableBody.appendChild(row);
      });
    } else {
      statAvgConf.textContent = '—';
      resultStatus.textContent = '✅ Tidak ada api terdeteksi.';
      resultStatus.style.color = '#22c55e';
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
    let modelInfoLoaded = false;

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
            showToast('⚠️ Gagal memuat statistik dataset', 'error');
        }
    }

    // ========================
    // Model Info (Lazy Load)
    // ========================
    async function loadModelInfo() {
        if (modelInfoLoaded) return;

        try {
            const response = await fetch('/api/model-info');
            const data = await response.json();

            if (data.success) {
                const info = data.data;

                // Update metric cards
                document.getElementById('mi-map50').textContent = (info.mAP50 * 100).toFixed(1);
                document.getElementById('mi-map50-95').textContent = (info.mAP50_95 * 100).toFixed(1);
                document.getElementById('mi-precision').textContent = (info.precision * 100).toFixed(1);
                document.getElementById('mi-recall').textContent = (info.recall * 100).toFixed(1);
                document.getElementById('mi-f1').textContent = (info.f1_score * 100).toFixed(1);

                // Update model details
                document.getElementById('mi-model-name').textContent = info.model_name;
                document.getElementById('mi-model-type').textContent = info.model_type;
                document.getElementById('mi-epochs').textContent = info.training_epochs;
                document.getElementById('mi-image-size').textContent = `${info.image_size}px`;
                document.getElementById('mi-batch-size').textContent = info.batch_size;
                document.getElementById('mi-eval-time').textContent = info.evaluation_time;

                modelInfoLoaded = true;
            }
        } catch (error) {
            console.error('Gagal memuat informasi model:', error);
            showToast('⚠️ Gagal memuat informasi model', 'error');
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

  // ========================
  // Keyboard Shortcuts
  // ========================
  document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus file input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      fileInput.click();
    }

    // Escape to clear selection
    if (e.key === 'Escape' && selectedFile) {
      previewImage.classList.add('hidden');
      dropzoneContent.classList.remove('hidden');
      selectedFile = null;
      btnDetect.disabled = true;
      fileInput.value = '';
      resetResults();
    }
  });

  // ========================
  // Smooth scroll for anchor links
  // ========================
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      }
    });
  });

  // ========================
  // Add loading animation to cards
  // ========================
  const cards = document.querySelectorAll('.card');
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    },
    { threshold: 0.1 },
  );

  cards.forEach((card) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(card);
  });

  // ========================
  // Console welcome message
  // ========================
  console.log('%c🔥 Fire Detection App — YOLOv9 AI %c✨', 'color: #ff8c00; font-size: 20px; font-weight: bold;', 'color: #ff4727; font-size: 20px;');
  console.log('%cDibuat oleh Hendra — A3-HXCODE © 2026', 'color: #a0a0b0; font-size: 12px;');
});
