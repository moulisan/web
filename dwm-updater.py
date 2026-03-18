#!/usr/bin/env python3
"""
DWM Updater - Local admin UI for managing dosawithmouli-data.json
Run: python3 dwm-updater.py
Opens browser to http://localhost:8111
"""

import json
import os
import subprocess
import webbrowser
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "dosawithmouli-data.json")
PHOTO_DIR = os.path.join(SCRIPT_DIR, "dosa-photos")
PORT = 8111

ADMIN_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DWM Updater - Admin</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --cream: #FAF8F5;
    --warm-white: #FFFEFA;
    --ink: #2C2416;
    --muted: #6B5D4D;
    --accent: #7C5E4A;
    --accent-hover: #5C4535;
    --border: #E8E2D9;
    --green: #3a7d44;
    --red: #c0392b;
    --blue: #2980b9;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Source Sans 3', sans-serif;
    background: var(--cream);
    color: var(--ink);
    padding-bottom: 80px;
}

.header {
    background: var(--warm-white);
    border-bottom: 1px solid var(--border);
    padding: 1rem 2rem;
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.header h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.4rem;
    font-weight: 600;
}

.header .entry-count {
    font-size: 0.85rem;
    color: var(--muted);
}

.container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 1.5rem 2rem;
}

/* Year groups */
.year-group {
    margin-bottom: 2rem;
}

.year-heading {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--ink);
    padding-bottom: 0.4rem;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Add entry button */
.add-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    width: 100%;
    padding: 0.5rem;
    margin-bottom: 0.75rem;
    border: 2px dashed var(--border);
    border-radius: 6px;
    background: transparent;
    color: var(--muted);
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'Source Sans 3', sans-serif;
}

.add-btn:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: rgba(124,94,74,0.04);
}

/* Entry row */
.entry-row {
    display: grid;
    grid-template-columns: 1fr 220px;
    gap: 1.25rem;
    background: var(--warm-white);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    transition: box-shadow 0.15s;
}

.entry-row:hover {
    box-shadow: 0 2px 8px rgba(44,36,22,0.07);
}

/* Left: form side */
.entry-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.field-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.field-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    width: 70px;
    flex-shrink: 0;
}

.field-value {
    font-size: 0.9rem;
    color: var(--ink);
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.field-value a {
    color: var(--blue);
    text-decoration: none;
    font-size: 0.82rem;
}

.field-value a:hover { text-decoration: underline; }

.field-input {
    flex: 1;
    font-size: 0.9rem;
    font-family: 'Source Sans 3', sans-serif;
    padding: 0.3rem 0.5rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--warm-white);
    color: var(--ink);
    min-width: 0;
}

.field-input:focus {
    outline: none;
    border-color: var(--accent);
}

.edit-icon {
    cursor: pointer;
    color: var(--muted);
    font-size: 0.8rem;
    padding: 0.15rem 0.3rem;
    border-radius: 3px;
    transition: all 0.15s;
    flex-shrink: 0;
    background: none;
    border: none;
    font-family: inherit;
}

.edit-icon:hover {
    color: var(--accent);
    background: rgba(124,94,74,0.08);
}

/* Drop zone */
.drop-zone {
    border: 2px dashed var(--border);
    border-radius: 6px;
    padding: 0.6rem;
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    cursor: pointer;
    transition: all 0.15s;
    margin-top: 0.25rem;
}

.drop-zone.dragover {
    border-color: var(--accent);
    background: rgba(124,94,74,0.06);
    color: var(--accent);
}

.entry-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.5rem;
}

.btn {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.35rem 0.75rem;
    border-radius: 4px;
    border: 1px solid;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-save {
    background: var(--green);
    border-color: var(--green);
    color: white;
}

.btn-save:hover { opacity: 0.85; }

.btn-delete {
    background: transparent;
    border-color: var(--red);
    color: var(--red);
}

.btn-delete:hover {
    background: var(--red);
    color: white;
}

.btn-cancel {
    background: transparent;
    border-color: var(--border);
    color: var(--muted);
}

.btn-cancel:hover {
    border-color: var(--muted);
    color: var(--ink);
}

/* Right: preview card */
.preview-card {
    width: 200px;
    background: var(--warm-white);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    align-self: start;
}

.preview-photo {
    width: 100%;
    aspect-ratio: 1/1;
    overflow: hidden;
    background: var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.7rem;
    color: var(--muted);
}

.preview-photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.preview-body {
    padding: 0.5rem 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 0.3rem;
}

.preview-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.preview-person {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1.3;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.preview-meta {
    font-size: 0.6rem;
    color: var(--muted);
    line-height: 1.4;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.preview-social {
    display: flex;
    gap: 0.25rem;
    flex-shrink: 0;
    padding-top: 0.1rem;
}

.preview-social a {
    color: var(--border);
    transition: color 0.15s;
}

.preview-social a:hover { color: var(--accent); }

.preview-social svg {
    width: 12px;
    height: 12px;
}

/* Sticky bottom bar */
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--warm-white);
    border-top: 1px solid var(--border);
    padding: 0.75rem 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    z-index: 100;
}

.btn-primary {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: all 0.15s;
}

.btn-save-all {
    background: var(--accent);
    color: white;
}

.btn-save-all:hover { background: var(--accent-hover); }

.btn-build {
    background: var(--ink);
    color: var(--cream);
}

.btn-build:hover { opacity: 0.85; }

.btn-primary:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Toast */
.toast {
    position: fixed;
    top: 70px;
    right: 1.5rem;
    padding: 0.75rem 1.25rem;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    z-index: 200;
    opacity: 0;
    transform: translateY(-10px);
    transition: all 0.25s;
    max-width: 500px;
    word-wrap: break-word;
    white-space: pre-wrap;
}

.toast.show {
    opacity: 1;
    transform: translateY(0);
}

.toast.success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.toast.error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.toast.info {
    background: #d1ecf1;
    color: #0c5460;
    border: 1px solid #bee5eb;
}

/* Dirty indicator */
.dirty-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--red);
    margin-left: 0.5rem;
    vertical-align: middle;
}

.dirty-dot.hidden { display: none; }

@media (max-width: 768px) {
    .entry-row {
        grid-template-columns: 1fr;
    }
    .preview-card {
        width: 100%;
        max-width: 200px;
    }
    .container {
        padding: 1rem;
    }
}
</style>
</head>
<body>

<div class="header">
    <div style="display:flex;align-items:center;gap:0.75rem">
        <h1>#DWM Updater</h1>
        <span class="entry-count" id="entryCount"></span>
        <span class="dirty-dot hidden" id="dirtyDot" title="Unsaved changes"></span>
    </div>
</div>

<div class="container" id="entriesContainer"></div>

<div class="bottom-bar">
    <button class="btn-primary btn-save-all" id="saveAllBtn" onclick="saveAll()">Save All to Disk</button>
    <button class="btn-primary btn-build" id="buildBtn" onclick="buildHtml()">Build HTML</button>
</div>

<div class="toast" id="toast"></div>

<script>
const MONTHS = {
    '01':'Jan','02':'Feb','03':'Mar','04':'Apr',
    '05':'May','06':'Jun','07':'Jul','08':'Aug',
    '09':'Sep','10':'Oct','11':'Nov','12':'Dec'
};

const X_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>';
const LI_ICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>';

let entries = [];
let dirty = false;
let editingIndex = null; // index of entry currently in edit mode

function setDirty(v) {
    dirty = v;
    document.getElementById('dirtyDot').classList.toggle('hidden', !v);
    document.getElementById('saveAllBtn').textContent = v ? 'Save All to Disk *' : 'Save All to Disk';
}

function showToast(msg, type='success', duration=3000) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast ' + type + ' show';
    clearTimeout(t._timer);
    t._timer = setTimeout(() => t.classList.remove('show'), duration);
}

function getMonthName(dateStr) {
    const parts = dateStr.split('-');
    return parts.length > 1 ? (MONTHS[parts[1]] || parts[1]) : '';
}

function getYear(dateStr) {
    return dateStr ? dateStr.split('-')[0] : '';
}

// Group entries by year, maintaining array order within each year
function groupByYear() {
    const groups = {};
    const yearOrder = [];
    entries.forEach((e, i) => {
        const y = getYear(e.date);
        if (!groups[y]) {
            groups[y] = [];
            yearOrder.push(y);
        }
        groups[y].push({ entry: e, index: i });
    });
    return { groups, yearOrder };
}

function escHtml(s) {
    if (!s) return '';
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function renderField(entry, idx, field, label, isEditing) {
    const val = entry[field] || '';
    if (isEditing) {
        return `<div class="field-row">
            <span class="field-label">${label}</span>
            <input class="field-input" data-idx="${idx}" data-field="${field}" value="${escHtml(val)}" />
        </div>`;
    }
    let display;
    if ((field === 'twitter' || field === 'linkedin') && val) {
        display = `<a href="${escHtml(val)}" target="_blank">${escHtml(val)}</a>`;
    } else {
        display = escHtml(val) || '<em style="color:var(--muted)">-</em>';
    }
    return `<div class="field-row">
        <span class="field-label">${label}</span>
        <span class="field-value">${display}</span>
    </div>`;
}

function renderPreview(entry) {
    const month = getMonthName(entry.date);
    const person = escHtml(entry.person || 'New entry');
    const venue = escHtml(entry.venue || '');
    const photo = entry.photo;

    let photoHtml;
    if (photo) {
        photoHtml = `<img src="/${escHtml(photo)}?t=${Date.now()}" alt="" onerror="this.parentElement.innerHTML='No photo'">`;
    } else {
        photoHtml = 'No photo';
    }

    let socialHtml = '';
    if (entry.twitter) {
        socialHtml += `<a href="${escHtml(entry.twitter)}" target="_blank">${X_ICON}</a>`;
    }
    if (entry.linkedin) {
        socialHtml += `<a href="${escHtml(entry.linkedin)}" target="_blank">${LI_ICON}</a>`;
    }

    return `<div class="preview-card">
        <div class="preview-photo">${photoHtml}</div>
        <div class="preview-body">
            <div class="preview-info">
                <span class="preview-person">${person}</span>
                <span class="preview-meta">${month}${month && venue ? ' &middot; ' : ''}${venue}</span>
            </div>
            <div class="preview-social">${socialHtml}</div>
        </div>
    </div>`;
}

function renderEntry(entry, idx, isEditing) {
    const fields = [
        renderField(entry, idx, 'person', 'Person', isEditing),
        renderField(entry, idx, 'date', 'Date', isEditing),
        renderField(entry, idx, 'venue', 'Venue', isEditing),
        renderField(entry, idx, 'twitter', 'Twitter', isEditing),
        renderField(entry, idx, 'linkedin', 'LinkedIn', isEditing),
    ].join('');

    const dropZone = `<div class="drop-zone" data-idx="${idx}"
        ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)"
        ondrop="handleDrop(event, ${idx})" onclick="triggerFileInput(${idx})">
        ${entry.photo ? '&#x1F4F7; Replace photo (drop or click)' : 'Drop photo here or click to upload'}
    </div>`;

    let actionsHtml;
    if (isEditing) {
        actionsHtml = `<div class="entry-actions">
            <button class="btn btn-save" onclick="saveEntry(${idx})">Save</button>
            <button class="btn btn-cancel" onclick="cancelEdit(${idx})">Cancel</button>
            <button class="btn btn-delete" onclick="deleteEntry(${idx})">Delete</button>
        </div>`;
    } else {
        actionsHtml = `<div class="entry-actions">
            <button class="btn edit-icon" onclick="startEdit(${idx})">&#x270F;&#xFE0F; Edit</button>
            <button class="btn btn-delete" onclick="deleteEntry(${idx})">Delete</button>
        </div>`;
    }

    return `<div class="entry-row" id="entry-${idx}">
        <div class="entry-form">
            ${fields}
            ${dropZone}
            ${actionsHtml}
        </div>
        ${renderPreview(entry)}
    </div>`;
}

function renderAddBtn(insertIdx, year) {
    return `<button class="add-btn" onclick="addEntry(${insertIdx}, '${year}')">+ Add entry here</button>`;
}

function render() {
    const { groups, yearOrder } = groupByYear();
    let html = '';

    document.getElementById('entryCount').textContent = entries.length + ' entries';

    yearOrder.forEach(year => {
        const items = groups[year];
        html += `<div class="year-group">
            <div class="year-heading">${year}</div>`;

        // Add button before first item in this year
        html += renderAddBtn(items[0].index, year);

        items.forEach((item, i) => {
            const isEditing = editingIndex === item.index;
            html += renderEntry(item.entry, item.index, isEditing);
            // Add button after each item
            const insertAt = item.index + 1;
            html += renderAddBtn(insertAt, year);
        });

        html += '</div>';
    });

    // If no entries at all
    if (entries.length === 0) {
        const currentYear = new Date().getFullYear().toString();
        html = renderAddBtn(0, currentYear);
    }

    document.getElementById('entriesContainer').innerHTML = html;
}

let editSnapshot = null;

function startEdit(idx) {
    editSnapshot = JSON.parse(JSON.stringify(entries[idx]));
    editingIndex = idx;
    render();
    // Focus first input
    const firstInput = document.querySelector(`[data-idx="${idx}"][data-field="person"]`);
    if (firstInput) firstInput.focus();
}

function cancelEdit(idx) {
    if (editSnapshot) {
        entries[idx] = editSnapshot;
        editSnapshot = null;
    }
    editingIndex = null;
    render();
}

function saveEntry(idx) {
    // Read values from inputs
    const inputs = document.querySelectorAll(`[data-idx="${idx}"]`);
    inputs.forEach(inp => {
        if (inp.dataset.field) {
            const val = inp.value.trim();
            entries[idx][inp.dataset.field] = val || null;
        }
    });
    editSnapshot = null;
    editingIndex = null;
    setDirty(true);
    render();
    showToast('Entry updated (in memory). Click "Save All" to write to disk.', 'info');
}

function addEntry(insertIdx, year) {
    const newEntry = {
        date: year + '-',
        person: '',
        venue: '',
        photo: null,
        twitter: null,
        linkedin: null
    };
    entries.splice(insertIdx, 0, newEntry);
    setDirty(true);
    editingIndex = insertIdx;
    editSnapshot = JSON.parse(JSON.stringify(newEntry));
    render();
    const el = document.getElementById('entry-' + insertIdx);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function deleteEntry(idx) {
    const name = entries[idx].person || 'this entry';
    if (!confirm('Delete ' + name + '?')) return;
    entries.splice(idx, 1);
    if (editingIndex === idx) {
        editingIndex = null;
        editSnapshot = null;
    } else if (editingIndex !== null && editingIndex > idx) {
        editingIndex--;
    }
    setDirty(true);
    render();
    showToast('Entry deleted (in memory). Click "Save All" to write to disk.', 'info');
}

// Photo upload
function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e, idx) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        uploadPhoto(idx, file);
    }
}

function triggerFileInput(idx) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.onchange = () => {
        if (input.files[0]) uploadPhoto(idx, input.files[0]);
    };
    input.click();
}

async function uploadPhoto(idx, file) {
    const formData = new FormData();
    formData.append('photo', file);
    try {
        const resp = await fetch('/api/upload/' + idx, { method: 'POST', body: formData });
        const result = await resp.json();
        if (result.ok) {
            entries[idx].photo = result.path;
            setDirty(true);
            render();
            showToast('Photo uploaded: ' + result.path, 'success');
        } else {
            showToast('Upload error: ' + result.error, 'error');
        }
    } catch(err) {
        showToast('Upload failed: ' + err.message, 'error');
    }
}

// Save all to disk
async function saveAll() {
    const btn = document.getElementById('saveAllBtn');
    btn.disabled = true;
    btn.textContent = 'Saving...';
    try {
        const resp = await fetch('/api/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(entries)
        });
        const result = await resp.json();
        if (result.ok) {
            setDirty(false);
            showToast('Saved ' + entries.length + ' entries to dosawithmouli-data.json', 'success');
        } else {
            showToast('Save error: ' + result.error, 'error');
        }
    } catch(err) {
        showToast('Save failed: ' + err.message, 'error');
    }
    btn.disabled = false;
    btn.textContent = dirty ? 'Save All to Disk *' : 'Save All to Disk';
}

// Build HTML
async function buildHtml() {
    const btn = document.getElementById('buildBtn');
    btn.disabled = true;
    btn.textContent = 'Building...';
    try {
        const resp = await fetch('/api/build', { method: 'POST' });
        const result = await resp.json();
        if (result.ok) {
            showToast('Build complete:\n' + result.output, 'success', 5000);
        } else {
            showToast('Build failed:\n' + result.output, 'error', 8000);
        }
    } catch(err) {
        showToast('Build failed: ' + err.message, 'error');
    }
    btn.disabled = false;
    btn.textContent = 'Build HTML';
}

// Initial load
async function loadData() {
    try {
        const resp = await fetch('/api/data');
        entries = await resp.json();
        render();
    } catch(err) {
        showToast('Failed to load data: ' + err.message, 'error');
    }
}

// Warn on page leave with unsaved changes
window.addEventListener('beforeunload', e => {
    if (dirty) {
        e.preventDefault();
        e.returnValue = '';
    }
});

loadData();
</script>

<input type="file" id="hiddenFileInput" accept="image/*" style="display:none">
</body>
</html>'''


class DWMHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quieter logging
        pass

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html):
        body = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath, content_type):
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/' or path == '':
            self._send_html(ADMIN_HTML)
            return

        if path == '/api/data':
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                self._send_json(data)
            except Exception as e:
                self._send_json({'error': str(e)}, 500)
            return

        # Serve photos
        if path.startswith('/dosa-photos/'):
            filename = path[len('/dosa-photos/'):]
            # Sanitize: no path traversal
            if '/' in filename or '..' in filename:
                self.send_response(403)
                self.end_headers()
                return
            filepath = os.path.join(PHOTO_DIR, filename)
            ext = os.path.splitext(filename)[1].lower()
            ctype = {
                '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                '.png': 'image/png', '.gif': 'image/gif',
                '.webp': 'image/webp',
            }.get(ext, 'application/octet-stream')
            self._send_file(filepath, ctype)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/save':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)
                data = json.loads(body)
                with open(DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    f.write('\n')
                self._send_json({'ok': True})
            except Exception as e:
                self._send_json({'ok': False, 'error': str(e)}, 500)
            return

        if path.startswith('/api/upload/'):
            try:
                idx_str = path[len('/api/upload/'):]
                idx = int(idx_str)

                content_type = self.headers.get('Content-Type', '')
                if 'multipart/form-data' not in content_type:
                    self._send_json({'ok': False, 'error': 'Expected multipart/form-data'}, 400)
                    return

                # Parse multipart form data manually (cgi module removed in 3.13)
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length)

                # Extract boundary from Content-Type
                boundary = None
                for part in content_type.split(';'):
                    part = part.strip()
                    if part.startswith('boundary='):
                        boundary = part[len('boundary='):].strip('"')
                        break

                if not boundary:
                    self._send_json({'ok': False, 'error': 'No boundary in Content-Type'}, 400)
                    return

                boundary_bytes = ('--' + boundary).encode()
                parts = body.split(boundary_bytes)

                file_data = None
                orig_filename = None
                for part in parts:
                    if b'Content-Disposition' not in part:
                        continue
                    # Split headers from body at double CRLF
                    header_end = part.find(b'\r\n\r\n')
                    if header_end < 0:
                        continue
                    header_section = part[:header_end].decode('utf-8', errors='replace')
                    file_body = part[header_end + 4:]
                    # Strip trailing \r\n-- or \r\n
                    if file_body.endswith(b'\r\n'):
                        file_body = file_body[:-2]

                    if 'name="photo"' in header_section:
                        # Extract filename
                        for token in header_section.split(';'):
                            token = token.strip()
                            if token.startswith('filename='):
                                orig_filename = token[len('filename='):].strip('"')
                        file_data = file_body

                if file_data is None or not orig_filename:
                    self._send_json({'ok': False, 'error': 'No file uploaded'}, 400)
                    return

                # Read current data to generate filename from person name
                with open(DATA_FILE, 'r') as f:
                    current_data = json.load(f)

                # Determine filename
                ext = os.path.splitext(orig_filename)[1].lower()
                if not ext:
                    ext = '.jpg'

                if idx < len(current_data) and current_data[idx].get('person'):
                    base = current_data[idx]['person'].lower().replace(' ', '-')
                    base = ''.join(c for c in base if c.isalnum() or c == '-')
                else:
                    base = 'photo-' + uuid.uuid4().hex[:8]

                filename = base + ext
                filepath = os.path.join(PHOTO_DIR, filename)
                os.makedirs(PHOTO_DIR, exist_ok=True)

                with open(filepath, 'wb') as f:
                    f.write(file_data)

                rel_path = 'dosa-photos/' + filename
                self._send_json({'ok': True, 'path': rel_path})
            except Exception as e:
                self._send_json({'ok': False, 'error': str(e)}, 500)
            return

        if path == '/api/build':
            try:
                result = subprocess.run(
                    ['python3', 'build-dosawithmouli.py'],
                    cwd=SCRIPT_DIR,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                output = result.stdout + result.stderr
                self._send_json({
                    'ok': result.returncode == 0,
                    'output': output.strip(),
                })
            except Exception as e:
                self._send_json({'ok': False, 'output': str(e)}, 500)
            return

        self.send_response(404)
        self.end_headers()


def main():
    os.makedirs(PHOTO_DIR, exist_ok=True)
    server = HTTPServer(('localhost', PORT), DWMHandler)
    url = f'http://localhost:{PORT}'
    print(f'DWM Updater running at {url}')
    print('Press Ctrl+C to stop')
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
        server.server_close()


if __name__ == '__main__':
    main()
