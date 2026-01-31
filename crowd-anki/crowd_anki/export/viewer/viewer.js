
// Logic to handle deck viewing

class DeckViewer {
    constructor() {
        this.manifest = window.deckManifest;
        this.currentDeck = null;
        this.models = {};
        this.cache = {}; // Cache for fetched JSON data
        this.renderMode = 'raw'; // 'raw' or 'model'
        this.deferredScripts = new Set(); // Store unique script content to execute post-render

        this.els = {
            deckList: document.getElementById('deck-list'),
            header: document.getElementById('deck-title'),
            container: document.getElementById('cards-container'),
            controls: document.getElementById('controls'),
            renderModeSelect: document.getElementById('render-mode')
        };
    }

    async init() {
        if (!this.manifest) {
            console.error("No manifest found. Ensure manifest.js is loaded.");
            return;
        }

        this.els.renderModeSelect.addEventListener('change', (e) => {
            this.renderMode = e.target.value;
            if (this.currentDeck) {
                this.selectDeck(this.currentDeck, document.querySelector('.nav-link.active'));
            }
        });

        // Load root models.json immediately as a baseline
        try {
            const rootModels = await this.fetchJSON('models.json');
            if (rootModels && rootModels.note_models) {
                rootModels.note_models.forEach(model => {
                    if (model.crowdanki_uuid) {
                        this.models[model.crowdanki_uuid] = model;
                    }
                    if (model.id) {
                        this.models[model.id] = model;
                    }
                });

                // Preload libraries for Raw Mode availability
                this.preloadLibraries(rootModels.note_models);
            }
        } catch (e) {
            console.warn("Could not load root models.json, models might be missing if not in subdecks:", e);
        }

        this.renderSidebar(this.manifest, this.els.deckList);
    }

    renderSidebar(node, container) {
        const item = document.createElement('div');
        item.className = 'nav-item';

        const link = document.createElement('div');
        link.className = 'nav-link';
        link.textContent = node.name;
        link.onclick = (e) => {
            e.stopPropagation();
            this.selectDeck(node, link);
        };
        item.appendChild(link);

        if (node.children && node.children.length > 0) {
            const childrenContainer = document.createElement('div');
            childrenContainer.className = 'nav-children';
            node.children.forEach(child => this.renderSidebar(child, childrenContainer));
            item.appendChild(childrenContainer);
        }

        container.appendChild(item);
    }

    async selectDeck(node, linkElement) {
        // Update active state in sidebar
        if (linkElement) {
            document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
            linkElement.classList.add('active');
        }

        this.currentDeck = node;
        this.els.header.textContent = node.name;
        this.els.controls.style.display = 'block';
        this.els.container.innerHTML = 'Loading...';

        try {
            // Load deck data concurrently
            const [deckData, notesData] = await Promise.all([
                this.fetchJSON(node.deckPath),
                this.fetchJSON(node.notesPath)
            ]);

            // Attempt to load models. Try current deck folder first, else look at root/manifest if defined?
            // Actually, for hierarchical export, models are often in models.json in the deck folder 
            // OR passed down. For simplicity, we check for models.json in deck dir.
            let modelsData = null;
            if (node.modelsPath) {
                modelsData = await this.fetchJSON(node.modelsPath).catch(() => null);
            }

            if (modelsData && modelsData.note_models) {
                modelsData.note_models.forEach(model => {
                    if (model.crowdanki_uuid) {
                        this.models[model.crowdanki_uuid] = model;
                    }
                    if (model.id) {
                        this.models[model.id] = model;
                    }
                });

                // Preload libraries for Raw Mode availability
                this.preloadLibraries(modelsData.note_models);
            }

            this.renderCards(notesData, deckData);
        } catch (error) {
            console.error("Error loading deck:", error);
            this.els.container.innerHTML = `<div class="error">Error loading deck: ${error.message}.<br>Note: Browser security blocks local file access (file://). Use a local server (python -m http.server).</div>`;
        }
    }

    preloadLibraries(models) {
        models.forEach(model => {
            if (model.tmpls) {
                model.tmpls.forEach(tmpl => {
                    // Extract from qfmt and afmt
                    // We only want to preload libraries, so we pass true
                    this.hoistResources(tmpl.qfmt || "", true);
                    this.hoistResources(tmpl.afmt || "", true);
                });
            }
        });
    }

    async fetchJSON(path) {
        if (!path) return null;
        if (this.cache[path]) return this.cache[path];

        const response = await fetch(path);
        if (!response.ok) throw new Error(`HTTP ${response.status} at ${path}`);
        const data = await response.json();
        this.cache[path] = data;
        return data;
    }

    renderCards(notes, deckData) {
        this.els.container.innerHTML = '';
        this.deferredScripts.clear(); // Reset deferred scripts for this render

        if (!notes || notes.length === 0) {
            this.els.container.innerHTML = '<p>No notes in this deck.</p>';
            return;
        }

        notes.forEach(note => {
            let model = this.models[note.note_model_uuid];
            if (!model && note.note_model_id) {
                model = this.models[note.note_model_id];
            }
            const cardEl = document.createElement('div');
            cardEl.className = 'card-container';

            if (this.renderMode === 'model' && model) {
                this.renderNoteWithModel(cardEl, note, model);
            } else {
                this.renderNoteRaw(cardEl, note, model);
            }

            this.els.container.appendChild(cardEl);
        });

        // Execute unique deferred scripts ONCE after all cards are rendered
        if (this.deferredScripts.size > 0) {
            this.deferredScripts.forEach(scriptContent => {
                const newScript = document.createElement('script');
                newScript.textContent = scriptContent;
                document.body.appendChild(newScript);
            });
        }

        if (window.hljs) {
            window.hljs.highlightAll();
        }
    }

    renderNoteRaw(container, note, model) {
        const rawContent = document.createElement('div');
        rawContent.className = 'card-render card-raw';

        const table = document.createElement('table');
        table.style.width = '100%';
        table.style.borderCollapse = 'collapse';

        note.fields.forEach((fieldValue, idx) => {
            const row = document.createElement('tr');

            const th = document.createElement('th');
            th.style.textAlign = 'left';
            th.style.width = '150px';
            th.style.padding = '8px';
            th.style.borderBottom = '1px solid #eee';
            th.style.verticalAlign = 'top';

            let fieldName = `Field ${idx + 1}`;
            if (model && model.flds && model.flds[idx]) {
                fieldName = model.flds[idx].name;
            }
            th.textContent = fieldName;

            const td = document.createElement('td');
            td.style.padding = '8px';
            td.style.borderBottom = '1px solid #eee';
            td.innerHTML = fieldValue;

            row.appendChild(th);
            row.appendChild(td);
            table.appendChild(row);
        });

        rawContent.appendChild(table);
        container.appendChild(rawContent);

        // Tags
        if (note.tags && note.tags.length) {
            const tagsBar = document.createElement('div');
            tagsBar.className = 'card-tags';
            note.tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'tag';
                tagSpan.textContent = tag;
                tagsBar.appendChild(tagSpan);
            });
            container.appendChild(tagsBar);
        }
    }

    renderNoteWithModel(container, note, model) {
        // Use standard div instead of shadow DOM to allow global styles/scripts
        const cardRender = document.createElement('div');
        cardRender.className = 'card-render';

        // First template usually used (Card 1)
        const tmpl = model.tmpls[0];

        const css = model.css || "";
        const qfmt = tmpl.qfmt;
        const afmt = tmpl.afmt;

        // Prepare context for template
        const context = {};
        note.fields.forEach((fieldValue, idx) => {
            const fieldDef = model.flds[idx];
            if (fieldDef) {
                context[fieldDef.name] = fieldValue;
            }
        });

        // Add Tags
        context['Tags'] = (note.tags || []).join(' ');

        // Simple replacements
        let frontHtml = this.applyTemplate(qfmt, context);
        let backHtml = this.applyTemplate(afmt, context);

        // In Anki, {{FrontSide}} in back template is replaced by front content
        backHtml = backHtml.replace(/\{\{FrontSide\}\}/g, frontHtml);

        // Combine for visualization: Front <hr> Back
        let fullHtml = `
            <style>
                ${css}
                .card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }
                hr#answer { border: 0; border-top: 1px dashed #ccc; margin: 15px 0; }
            </style>
            <div class="card">
                ${frontHtml}
                <hr id="answer">
                ${backHtml}
            </div>
        `;

        // Hoist resources (Scripts/Links) to global scope
        fullHtml = this.hoistResources(fullHtml);

        // Set content directly
        cardRender.innerHTML = fullHtml;
        container.appendChild(cardRender);

        // Tags bar
        if (note.tags && note.tags.length) {
            const tagsBar = document.createElement('div');
            tagsBar.className = 'card-tags';
            note.tags.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'tag';
                tagSpan.textContent = tag;
                tagsBar.appendChild(tagSpan);
            });
            container.appendChild(tagsBar);
        }
    }

    hoistResources(htmlContent, librariesOnly = false) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlContent, 'text/html');
        let modified = false;

        // Hoist CSS Links
        doc.querySelectorAll('link[rel="stylesheet"]').forEach(link => {
            const href = link.getAttribute('href');
            if (href) {
                if (!document.querySelector(`link[href="${href}"]`)) {
                    const newLink = document.createElement('link');
                    newLink.rel = 'stylesheet';
                    newLink.href = href;
                    document.head.appendChild(newLink);
                }
                link.remove();
                modified = true;
            }
        });

        // Hoist Scripts
        doc.querySelectorAll('script').forEach(script => {
            const src = script.getAttribute('src');
            if (src) {
                // External script
                if (!document.querySelector(`script[src="${src}"]`)) {
                    const newScript = document.createElement('script');
                    newScript.src = src;
                    document.body.appendChild(newScript);
                }
                script.remove();
                modified = true;
            } else if (!librariesOnly) {
                // Inline script - DEFER execution
                const content = script.textContent;
                if (content && content.trim().length > 0) {
                    this.deferredScripts.add(content);
                }
                script.remove();
                modified = true;
            }
        });

        return modified ? doc.body.innerHTML : htmlContent;
    }

    applyTemplate(template, context) {
        if (!template) return "";
        let result = template;

        // Replace {{FieldName}}
        // Regex to match {{...}}
        result = result.replace(/\{\{([^{}]+?)\}\}/g, (match, content) => {
            const key = content.trim();
            if (context[key] !== undefined) {
                return context[key];
            }
            return match;
        });

        return result;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const viewer = new DeckViewer();
    viewer.init();
});
