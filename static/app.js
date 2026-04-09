// Global variables
let uploadedFilename = null;
let currentData = null;

// Initialize
$(document).ready(function () {
    setupUploadArea();
    setupOperationCheckboxes();
    setupButtons();
});

// Setup upload area drag & drop
function setupUploadArea() {
    const uploadArea = $('#uploadArea');
    const fileInput = $('#fileInput');

    uploadArea.on('click', function () {
        fileInput.click();
    });

    uploadArea.on('dragover', function (e) {
        e.preventDefault();
        uploadArea.addClass('dragover');
    });

    uploadArea.on('dragleave', function () {
        uploadArea.removeClass('dragover');
    });

    uploadArea.on('drop', function (e) {
        e.preventDefault();
        uploadArea.removeClass('dragover');
        const files = e.originalEvent.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    fileInput.on('change', function () {
        if (this.files.length > 0) {
            handleFileUpload(this.files[0]);
        }
    });
}

// Handle file upload
function handleFileUpload(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Only CSV files are supported');
        return;
    }

    if (file.size > 50 * 1024 * 1024) {
        showError('File size exceeds 50MB limit');
        return;
    }

    showSpinner();

    const formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: '/upload',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            hideSpinner();
            uploadedFilename = response.filename;
            currentData = response;

            // Display preview
            displayDataPreview(response);

            // Show preview and operations sections
            showSection('previewSection');
            showSection('operationsSection');
        },
        error: function (xhr) {
            hideSpinner();
            showError(xhr.responseJSON?.error || 'Error uploading file');
        }
    });
}

// Display data preview
function displayDataPreview(response) {
    $('#statsRows').text(response.stats.rows);
    $('#statsColumns').text(response.stats.columns);
    $('#statsDuplicates').text(response.stats.duplicates);
    $('#statsMissing').text(response.stats.missing_count);

    // Build table
    const thead = $('#dataPreview thead');
    const tbody = $('#dataPreview tbody');

    thead.empty();
    tbody.empty();

    const headerRow = $('<tr class="table-dark">');
    response.columns.forEach(col => {
        headerRow.append(`<th>${escapeHtml(col)}</th>`);
    });
    thead.append(headerRow);

    response.preview.forEach(row => {
        const rowElem = $('<tr>');
        response.columns.forEach(col => {
            const value = row[col];
            rowElem.append(`<td>${escapeHtml(String(value))}</td>`);
        });
        tbody.append(rowElem);
    });
}

// Setup operation checkboxes
function setupOperationCheckboxes() {
    $(document).on('change', '.operation', function () {
        const value = $(this).val();
        const isChecked = $(this).is(':checked');

        // Show/hide operation-specific options
        if (value === 'handle_missing' && isChecked) {
            $(this).parent().find('[id^="missing"]').parent().show();
        } else if (value === 'remove_outliers' && isChecked) {
            $(this).parent().find('[id^="outlier"]').parent().show();
        }

        // Hide when unchecked
        if (value === 'handle_missing' && !isChecked) {
            $(this).parent().find('[id^="missing"]').parent().hide();
        } else if (value === 'remove_outliers' && !isChecked) {
            $(this).parent().find('[id^="outlier"]').parent().hide();
        }
    });
}

// Setup buttons
function setupButtons() {
    $('#sanitizeBtn').on('click', performSanitization);
    $('#resetBtn').on('click', function () {
        location.reload();
    });
    $('#downloadBtn').on('click', downloadCleanedData);
    $('#newFileBtn').on('click', function () {
        location.reload();
    });
}

// Perform sanitization
function performSanitization() {
    const operations = [];

    $('.operation:checked').each(function () {
        const value = $(this).val();
        const op = { type: value };

        if (value === 'handle_missing') {
            op.strategy = $('#missingStrategy').val();
        } else if (value === 'remove_outliers') {
            op.method = $('#outlierMethod').val();
            op.threshold = parseFloat($('#outlierThreshold').val());
        }

        operations.push(op);
    });

    if (operations.length === 0) {
        showError('Please select at least one operation');
        return;
    }

    showSpinner();
    hideSection('operationsSection');

    $.ajax({
        url: '/sanitize',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            filename: uploadedFilename,
            operations: operations
        }),
        success: function (response) {
            hideSpinner();
            displayResults(response);
            showSection('resultsSection');
        },
        error: function (xhr) {
            hideSpinner();
            showSection('operationsSection');
            showError(xhr.responseJSON?.error || 'Error during sanitization');
        }
    });
}

// Display results
function displayResults(response) {
    const comparison = response.comparison;
    $('#resultRowsRemoved').text(comparison.rows_removed);
    $('#resultDuplicatesRemoved').text(comparison.duplicates_removed);
    $('#resultMemorySaved').text(comparison.memory_saved_mb.toFixed(2));

    // Display cleaning log
    const logDiv = $('#cleaningLog');
    logDiv.empty();

    response.cleaning_log.forEach((log, idx) => {
        let logText = `<div class="mb-2"><strong>${idx + 1}. ${log.action}</strong>`;

        if (log.rows_affected !== undefined) {
            logText += ` - ${log.rows_affected} rows affected`;
        }
        if (log.rows_removed !== undefined) {
            logText += ` - ${log.rows_removed} rows removed`;
        }
        if (log.columns !== undefined && typeof log.columns === 'number') {
            logText += ` - ${log.columns} columns`;
        }
        if (log.columns !== undefined && Array.isArray(log.columns)) {
            logText += ` - Columns: ${log.columns.join(', ')}`;
        }

        logText += '</div>';
        logDiv.append(logText);
    });

    // Display result preview
    const resultPreview = $('#resultPreview');
    resultPreview.html(response.preview);

    // Store cleaned filename for download
    uploadedFilename = response.cleaned_filename;
}

// Download cleaned data
function downloadCleanedData() {
    window.location.href = `/download/${uploadedFilename}`;
}

// Utility functions
function showSection(sectionId) {
    $('.section').removeClass('active');
    $(`#${sectionId}`).addClass('active');
    $('html, body').animate({ scrollTop: 0 }, 'smooth');
}

function hideSection(sectionId) {
    $(`#${sectionId}`).removeClass('active');
}

function showSpinner() {
    $('#spinnerContainer').show();
}

function hideSpinner() {
    $('#spinnerContainer').hide();
}

function showError(message) {
    const errorDiv = $('#uploadError');
    errorDiv.text(message).show();
    setTimeout(() => errorDiv.fadeOut(), 5000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
