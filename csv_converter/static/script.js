// Global State
let currentSessionId = null;
let currentData = {
    columns: [],
    rows: []
};

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadSection = document.getElementById('uploadSection');
const dataSection = document.getElementById('dataSection');
const fileNameDisplay = document.getElementById('fileName');
const displayFileName = document.getElementById('displayFileName');
const rowCountDisplay = document.getElementById('rowCount');
const colCountDisplay = document.getElementById('colCount');
const headerRow = document.getElementById('headerRow');
const tableBody = document.getElementById('tableBody');
const backBtn = document.getElementById('backBtn');
const addRowBtn = document.getElementById('addRowBtn');
const addColBtn = document.getElementById('addColBtn');
const downloadExcelBtn = document.getElementById('downloadExcelBtn');
const downloadCSVBtn = document.getElementById('downloadCSVBtn');
const toast = document.getElementById('toast');

// File Upload Handling
const uploadBox = document.querySelector('.upload-box');

// Click to select file
uploadBox.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        if (file.type !== 'text/csv') {
            showToast('Only CSV files are allowed!', 'error');
            return;
        }
        uploadFile(file);
    }
});

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = '#70AD47';
    uploadBox.style.background = '#F0FFF4';
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.style.borderColor = '#2E75B6';
    uploadBox.style.background = '#F0F4FF';
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.style.borderColor = '#2E75B6';
    uploadBox.style.background = '#F0F4FF';
    
    const files = e.dataTransfer.files;
    if (files[0]) {
        uploadFile(files[0]);
    }
});

// Upload file function
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    uploadBox.classList.add('loading');
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        uploadBox.classList.remove('loading');
        
        if (data.success) {
            currentSessionId = data.sessionId;
            currentData = {
                columns: data.columns,
                rows: data.rows
            };
            
            fileNameDisplay.textContent = `✓ ${data.stats.filename} loaded`;
            displayFileName.textContent = data.stats.filename;
            
            renderTable();
            switchSection('data');
            showToast(`Loaded ${data.stats.rows} rows and ${data.stats.columns} columns`, 'success');
        } else {
            showToast(data.error || 'Upload failed', 'error');
        }
    })
    .catch(error => {
        uploadBox.classList.remove('loading');
        showToast('Error uploading file', 'error');
        console.error('Error:', error);
    });
}

// Render table
function renderTable() {
    // Clear existing content
    headerRow.innerHTML = '';
    tableBody.innerHTML = '';
    
    // Render header
    const headerCells = currentData.columns.map((col, idx) => {
        return `<th contenteditable="true" data-col="${idx}" class="editable-header">${col}</th>`;
    });
    headerRow.innerHTML = headerCells.join('') + '<th style="width: 80px; text-align: center;">Action</th>';
    
    // Update stats
    rowCountDisplay.textContent = currentData.rows.length;
    colCountDisplay.textContent = currentData.columns.length;
    
    // Render rows
    currentData.rows.forEach((row, rowIdx) => {
        const cells = currentData.columns.map((col, colIdx) => {
            const value = row[colIdx] || '';
            return `<td><input type="text" value="${escapeHtml(value)}" data-row="${rowIdx}" data-col="${colIdx}" class="cell-input"></td>`;
        });
        
        const deleteBtn = `<td style="text-align: center;"><button class="delete-btn" data-row="${rowIdx}">Delete</button></td>`;
        
        const tr = document.createElement('tr');
        tr.innerHTML = cells.join('') + deleteBtn;
        tableBody.appendChild(tr);
    });
    
    // Attach event listeners
    attachTableListeners();
}

// Attach table event listeners
function attachTableListeners() {
    // Cell input change
    document.querySelectorAll('.cell-input').forEach(input => {
        input.addEventListener('change', (e) => {
            const rowIdx = parseInt(e.target.dataset.row);
            const colIdx = parseInt(e.target.dataset.col);
            currentData.rows[rowIdx][colIdx] = e.target.value;
        });
    });
    
    // Delete row buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const rowIdx = parseInt(e.target.dataset.row);
            if (confirm('Are you sure you want to delete this row?')) {
                deleteRow(rowIdx);
            }
        });
    });
    
    // Header column rename
    document.querySelectorAll('.editable-header').forEach(header => {
        header.addEventListener('blur', (e) => {
            const colIdx = parseInt(e.target.dataset.col);
            const newName = e.target.textContent.trim();
            if (newName && newName !== currentData.columns[colIdx]) {
                currentData.columns[colIdx] = newName;
            }
        });
    });
}

// Add row
addRowBtn.addEventListener('click', () => {
    const newRow = Array(currentData.columns.length).fill('');
    currentData.rows.push(newRow);
    renderTable();
    showToast('Row added', 'success');
});

// Delete row
function deleteRow(rowIdx) {
    currentData.rows.splice(rowIdx, 1);
    renderTable();
    showToast('Row deleted', 'success');
}

// Add column
addColBtn.addEventListener('click', () => {
    const colName = prompt('Column name:', 'New Column');
    if (colName) {
        if (currentData.columns.includes(colName)) {
            showToast('Column already exists', 'error');
            return;
        }
        currentData.columns.push(colName);
        currentData.rows.forEach(row => row.push(''));
        renderTable();
        showToast('Column added', 'success');
    }
});

// Download Excel
downloadExcelBtn.addEventListener('click', () => {
    if (!currentSessionId) return;
    
    const filename = prompt('Filename:', displayFileName.textContent.replace('.csv', '.xlsx'));
    if (!filename) return;
    
    updateDataOnServer().then(() => {
        fetch('/api/download-excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sessionId: currentSessionId,
                filename: filename.endsWith('.xlsx') ? filename : filename + '.xlsx'
            })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename.endsWith('.xlsx') ? filename : filename + '.xlsx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showToast('Excel file downloaded', 'success');
        })
        .catch(error => {
            showToast('Error downloading file', 'error');
            console.error('Error:', error);
        });
    });
});

// Download CSV
downloadCSVBtn.addEventListener('click', () => {
    if (!currentSessionId) return;
    
    const filename = prompt('Filename:', displayFileName.textContent);
    if (!filename) return;
    
    updateDataOnServer().then(() => {
        fetch('/api/download-csv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sessionId: currentSessionId,
                filename: filename.endsWith('.csv') ? filename : filename + '.csv'
            })
        })
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename.endsWith('.csv') ? filename : filename + '.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            showToast('CSV file downloaded', 'success');
        })
        .catch(error => {
            showToast('Error downloading file', 'error');
            console.error('Error:', error);
        });
    });
});

// Update data on server
function updateDataOnServer() {
    return fetch('/api/update-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sessionId: currentSessionId,
            columns: currentData.columns,
            rows: currentData.rows
        })
    })
    .then(response => response.json());
}

// Back button
backBtn.addEventListener('click', () => {
    currentSessionId = null;
    currentData = { columns: [], rows: [] };
    fileInput.value = '';
    fileNameDisplay.textContent = '';
    switchSection('upload');
});

// Switch sections
function switchSection(section) {
    if (section === 'upload') {
        uploadSection.style.display = 'grid';
        dataSection.style.display = 'none';
    } else {
        uploadSection.style.display = 'none';
        dataSection.style.display = 'block';
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
console.log('CSV to Excel Converter Web App loaded');
