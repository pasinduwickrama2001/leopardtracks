/**
 * Discoveryala Admin - Automatic Image Compressor
 * Prevents Vercel 413 FUNCTION_PAYLOAD_TOO_LARGE (4.5 MB request body limit).
 * Automatically optimizes high-res camera/phone photos before uploading.
 */
(function () {
  'use strict';

  const COMPRESSION_THRESHOLD = 1.5 * 1024 * 1024; // 1.5 MB threshold to trigger compression
  const HARD_MAX_PAYLOAD = 4.0 * 1024 * 1024;      // 4.0 MB hard limit before blocking submit
  const MAX_DIMENSION = 1920;                      // Max width/height (Full HD retina quality)
  const QUALITY = 0.82;                            // 82% JPEG quality (visually lossless, compact)

  let activeCompressions = 0;

  function formatSize(bytes) {
    if (!bytes || bytes <= 0) return '0 B';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  }

  function getStatusElement(input) {
    let container = input.closest('.form-row') || input.parentNode;
    let status = container.querySelector('.img-compressor-status');
    if (!status) {
      status = document.createElement('div');
      status.className = 'img-compressor-status';
      status.style.cssText = 'margin-top: 8px; font-size: 13px; font-weight: 600; border-radius: 6px; padding: 6px 12px; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); transition: all 0.2s ease;';
      if (input.nextSibling) {
        input.parentNode.insertBefore(status, input.nextSibling);
      } else {
        input.parentNode.appendChild(status);
      }
    }
    return status;
  }

  function setStatus(input, text, type) {
    const status = getStatusElement(input);
    status.style.display = 'inline-flex';
    if (type === 'loading') {
      status.style.background = '#e0f2fe';
      status.style.color = '#0369a1';
      status.style.border = '1px solid #bae6fd';
      status.innerHTML = '<span>⏳</span> ' + text;
    } else if (type === 'success') {
      status.style.background = '#dcfce7';
      status.style.color = '#15803d';
      status.style.border = '1px solid #bbf7d0';
      status.innerHTML = '<span>✓</span> ' + text;
    } else if (type === 'warning') {
      status.style.background = '#fef3c7';
      status.style.color = '#b45309';
      status.style.border = '1px solid #fde68a';
      status.innerHTML = '<span>⚠</span> ' + text;
    } else if (type === 'error') {
      status.style.background = '#fee2e2';
      status.style.color = '#b91c1c';
      status.style.border = '1px solid #fecaca';
      status.innerHTML = '<span>✕</span> ' + text;
    }
  }

  function compressImage(file, callback) {
    const reader = new FileReader();
    reader.onerror = function () {
      callback(file, new Error('Failed to read file'));
    };
    reader.onload = function (e) {
      const img = new Image();
      img.onerror = function () {
        callback(file, new Error('Failed to load image'));
      };
      img.onload = function () {
        let width = img.width;
        let height = img.height;

        // Scale proportionally if exceeding MAX_DIMENSION
        if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
          if (width > height) {
            height = Math.round((height * MAX_DIMENSION) / width);
            width = MAX_DIMENSION;
          } else {
            width = Math.round((width * MAX_DIMENSION) / height);
            height = MAX_DIMENSION;
          }
        }

        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        const mimeType = file.type === 'image/webp' ? 'image/webp' : 'image/jpeg';

        canvas.toBlob(
          function (blob) {
            if (!blob) {
              return callback(file, new Error('Canvas toBlob failed'));
            }

            // If compressed blob is unexpectedly larger than original and original is safe:
            if (blob.size >= file.size && file.size < HARD_MAX_PAYLOAD) {
              return callback(file);
            }

            const extension = mimeType === 'image/webp' ? '.webp' : '.jpg';
            const baseName = file.name.replace(/\.[^/.]+$/, '');
            const newName = baseName + extension;

            const compressedFile = new File([blob], newName, {
              type: mimeType,
              lastModified: Date.now(),
            });

            callback(compressedFile);
          },
          mimeType,
          QUALITY
        );
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }

  function handleFileInput(input) {
    if (!input.files || input.files.length === 0) return;
    const file = input.files[0];

    // Only process image files
    if (!file.type || !file.type.startsWith('image/')) {
      if (file.size > HARD_MAX_PAYLOAD) {
        setStatus(input, `File is ${formatSize(file.size)}. Vercel limit is 4.5 MB. Please upload a smaller file.`, 'error');
      }
      return;
    }

    // Already small enough to safely upload without compression
    if (file.size <= COMPRESSION_THRESHOLD) {
      setStatus(input, `Image size: ${formatSize(file.size)} (Safe for Vercel cloud upload)`, 'success');
      return;
    }

    // Compress large image
    activeCompressions++;
    setStatus(input, `Optimizing high-res image (${formatSize(file.size)}) for Vercel upload...`, 'loading');

    compressImage(file, function (optimizedFile, err) {
      activeCompressions--;
      if (err || !optimizedFile) {
        if (file.size > HARD_MAX_PAYLOAD) {
          setStatus(input, `Image (${formatSize(file.size)}) exceeds Vercel 4.5 MB limit. Please select a smaller photo.`, 'error');
        } else {
          setStatus(input, `Original size: ${formatSize(file.size)}`, 'warning');
        }
        return;
      }

      try {
        const dt = new DataTransfer();
        dt.items.add(optimizedFile);
        input.files = dt.files;
        setStatus(
          input,
          `Optimized: ${formatSize(file.size)} ➔ ${formatSize(optimizedFile.size)} (Ready to Save)`,
          'success'
        );
      } catch (dtError) {
        console.warn('DataTransfer not supported by this browser:', dtError);
        if (file.size > HARD_MAX_PAYLOAD) {
          setStatus(input, `Image exceeds 4.5 MB Vercel limit. Please resize photo to under 4MB before selecting.`, 'error');
        }
      }
    });
  }

  // Delegated change listener for file inputs
  document.addEventListener('change', function (e) {
    if (e.target && e.target.matches && e.target.matches('input[type="file"]')) {
      handleFileInput(e.target);
    }
  });

  // Guard form submissions against payload too large & in-progress compressions
  document.addEventListener('submit', function (e) {
    if (activeCompressions > 0) {
      e.preventDefault();
      alert('Please wait a moment — image optimization is in progress...');
      return false;
    }

    const form = e.target;
    if (!form || !form.querySelectorAll) return;

    const fileInputs = form.querySelectorAll('input[type="file"]');
    let totalSize = 0;
    let hasOversized = false;

    fileInputs.forEach(function (input) {
      if (input.files) {
        for (let i = 0; i < input.files.length; i++) {
          totalSize += input.files[i].size;
          if (input.files[i].size > HARD_MAX_PAYLOAD) {
            hasOversized = true;
          }
        }
      }
    });

    if (hasOversized || totalSize > HARD_MAX_PAYLOAD) {
      e.preventDefault();
      alert(
        'Upload Payload Too Large!\n\n' +
        'Total payload size is ' + formatSize(totalSize) + '.\n' +
        'Vercel Serverless Functions enforce a strict 4.5 MB limit per request.\n\n' +
        'Please wait for auto-compression to finish or select a smaller image.'
      );
      return false;
    }
  });
})();
