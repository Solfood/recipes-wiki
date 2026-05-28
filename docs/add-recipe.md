---
title: Add a Recipe
---

# Add a Recipe

Fill in the form below to generate recipe markdown in the Willowbrook format. Once generated, **copy** the output and save it to the path shown.

<div id="rb-form">

<div class="rb-section">
<h2 class="rb-h2">Basic Info</h2>

<div class="rb-row">
<div class="rb-field rb-full">
<label class="rb-label" for="rb-title">Title <span class="rb-req">*</span></label>
<input class="rb-input" id="rb-title" type="text" placeholder="e.g. Honey Garlic Chicken" autocomplete="off">
</div>
</div>

<div class="rb-row">
<div class="rb-field rb-full">
<label class="rb-label" for="rb-subtitle">Subtitle <span class="rb-opt">(optional)</span></label>
<input class="rb-input" id="rb-subtitle" type="text" placeholder="e.g. Crispy · Weeknight · One-Pan" autocomplete="off">
</div>
</div>

<div class="rb-row">
<div class="rb-field rb-half">
<label class="rb-label" for="rb-category">Category <span class="rb-req">*</span></label>
<select class="rb-input" id="rb-category">
<option value="">— select —</option>
<option value="beef">Beef</option>
<option value="fermentation">Fermentation</option>
<option value="pizza">Pizza</option>
<option value="poultry">Poultry</option>
<option value="sauces">Sauces</option>
<option value="seafood">Seafood</option>
<option value="sides">Sides</option>
<option value="other">Other (new category)</option>
</select>
</div>
<div class="rb-field rb-half" id="rb-newcat-wrap" style="display:none">
<label class="rb-label" for="rb-newcat">New Category Name</label>
<input class="rb-input" id="rb-newcat" type="text" placeholder="e.g. desserts" autocomplete="off">
</div>
</div>

</div>

<div class="rb-section">
<h2 class="rb-h2">Recipe Details</h2>

<div class="rb-row">
<div class="rb-field rb-quarter">
<label class="rb-label" for="rb-yield">Yield <span class="rb-req">*</span></label>
<input class="rb-input" id="rb-yield" type="text" placeholder="4 servings" autocomplete="off">
</div>
<div class="rb-field rb-quarter">
<label class="rb-label" for="rb-prep">Prep Time</label>
<input class="rb-input" id="rb-prep" type="text" placeholder="15 mins" autocomplete="off">
</div>
<div class="rb-field rb-quarter">
<label class="rb-label" for="rb-cook">Cook Time</label>
<input class="rb-input" id="rb-cook" type="text" placeholder="30 mins" autocomplete="off">
</div>
<div class="rb-field rb-quarter">
<label class="rb-label" for="rb-texture">Texture Target <span class="rb-opt">(opt.)</span></label>
<input class="rb-input" id="rb-texture" type="text" placeholder="e.g. Crispy outside" autocomplete="off">
</div>
</div>

</div>

<div class="rb-section">
<h2 class="rb-h2">Ingredients</h2>
<div id="rb-groups"></div>
<button type="button" class="rb-btn-add" id="rb-add-group">+ Add Group</button>
</div>

<div class="rb-section">
<h2 class="rb-h2">Method</h2>
<div id="rb-steps"></div>
<button type="button" class="rb-btn-add" id="rb-add-step">+ Add Step</button>
</div>

<div class="rb-section">
<h2 class="rb-h2">Chef's Notes <span class="rb-opt">(optional)</span></h2>
<div id="rb-notes"></div>
<button type="button" class="rb-btn-add" id="rb-add-note">+ Add Note</button>
</div>

<div class="rb-actions">
<button type="button" class="rb-btn-generate" id="rb-generate">Generate Markdown</button>
</div>

</div>

<div id="rb-output" style="display:none">
<div class="rb-output-bar">
<span class="rb-output-label">Generated Markdown</span>
<code class="rb-filepath" id="rb-filepath"></code>
<button type="button" class="rb-btn-copy" id="rb-copy">Copy</button>
</div>
<pre class="rb-pre" id="rb-pre"><code id="rb-code"></code></pre>
</div>

<script>
(function () {
  var form = document.getElementById('rb-form');
  if (!form || form.dataset.init) return;
  form.dataset.init = '1';

  var gid = 0, iid = 0, sid = 0;

  function slug(s) {
    return s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }

  function esc(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function addGroup(defaultName) {
    gid++;
    var g = gid;
    var wrap = document.getElementById('rb-groups');
    var div = document.createElement('div');
    div.className = 'rb-group';
    div.innerHTML =
      '<div class="rb-group-hdr">' +
        '<input class="rb-gname" type="text" placeholder="Group name (e.g. Sauce)" value="' + esc(defaultName || '') + '">' +
        '<button type="button" class="rb-btn-remove">Remove group</button>' +
      '</div>' +
      '<div class="rb-ings" id="rb-ings-' + g + '"></div>' +
      '<button type="button" class="rb-btn-add-sm" data-g="' + g + '">+ Ingredient</button>';
    wrap.appendChild(div);
    div.querySelector('.rb-btn-remove').addEventListener('click', function () { div.remove(); });
    div.querySelector('[data-g]').addEventListener('click', function () { addIng(g); });
    addIng(g);
  }

  function addIng(g) {
    iid++;
    var list = document.getElementById('rb-ings-' + g);
    var div = document.createElement('div');
    div.className = 'rb-ing';
    div.innerHTML =
      '<input class="rb-qty" type="text" placeholder="Qty" aria-label="Quantity">' +
      '<input class="rb-item" type="text" placeholder="Ingredient" aria-label="Ingredient">' +
      '<button type="button" class="rb-x" aria-label="Remove">&#xd7;</button>';
    list.appendChild(div);
    div.querySelector('.rb-x').addEventListener('click', function () { div.remove(); });
  }

  function addStep() {
    sid++;
    var wrap = document.getElementById('rb-steps');
    var num = wrap.children.length + 1;
    var div = document.createElement('div');
    div.className = 'rb-step';
    div.innerHTML =
      '<div class="rb-step-hdr">' +
        '<span class="rb-step-n">Step ' + num + '</span>' +
        '<input class="rb-sname" type="text" placeholder="Step name (e.g. Brown the meat)">' +
        '<button type="button" class="rb-btn-remove">Remove</button>' +
      '</div>' +
      '<textarea class="rb-sdesc" rows="3" placeholder="Describe what to do in this step..."></textarea>';
    wrap.appendChild(div);
    div.querySelector('.rb-btn-remove').addEventListener('click', function () {
      div.remove();
      var steps = document.querySelectorAll('.rb-step');
      steps.forEach(function (el, i) {
        var n = el.querySelector('.rb-step-n');
        if (n) n.textContent = 'Step ' + (i + 1);
      });
    });
  }

  function addNote() {
    var list = document.getElementById('rb-notes');
    var div = document.createElement('div');
    div.className = 'rb-note';
    div.innerHTML =
      '<input class="rb-ntext" type="text" placeholder="Tip or note...">' +
      '<button type="button" class="rb-x" aria-label="Remove">&#xd7;</button>';
    list.appendChild(div);
    div.querySelector('.rb-x').addEventListener('click', function () { div.remove(); });
  }

  document.getElementById('rb-category').addEventListener('change', function () {
    document.getElementById('rb-newcat-wrap').style.display = this.value === 'other' ? '' : 'none';
  });

  document.getElementById('rb-add-group').addEventListener('click', function () { addGroup(''); });
  document.getElementById('rb-add-step').addEventListener('click', addStep);
  document.getElementById('rb-add-note').addEventListener('click', addNote);

  document.getElementById('rb-generate').addEventListener('click', function () {
    var title    = document.getElementById('rb-title').value.trim();
    var subtitle = document.getElementById('rb-subtitle').value.trim();
    var catSel   = document.getElementById('rb-category').value;
    var catNew   = document.getElementById('rb-newcat').value.trim();
    var category = catSel === 'other' ? slug(catNew || 'uncategorized') : catSel;
    var yld      = document.getElementById('rb-yield').value.trim();
    var prep     = document.getElementById('rb-prep').value.trim();
    var cook     = document.getElementById('rb-cook').value.trim();
    var texture  = document.getElementById('rb-texture').value.trim();

    if (!title)    { alert('Recipe title is required.'); return; }
    if (!category) { alert('Please select a category.'); return; }
    if (!yld)      { alert('Yield is required.'); return; }

    var lines = [];
    lines.push('# ' + title);
    if (subtitle) lines.push('*(' + subtitle + ')*');
    lines.push('');

    lines.push('!!! info "Recipe Details"');
    lines.push('    *   **Yield:** ' + yld);
    if (prep)    lines.push('    *   **Prep Time:** ' + prep);
    if (cook)    lines.push('    *   **Cook Time:** ' + cook);
    if (texture) lines.push('    *   **Texture target:** ' + texture);
    lines.push('');

    lines.push('## Ingredients');
    lines.push('');
    var groups = document.querySelectorAll('.rb-group');
    if (!groups.length) {
      lines.push('- [ ] **Qty** Ingredient');
      lines.push('');
    } else {
      groups.forEach(function (g) {
        var gname = g.querySelector('.rb-gname').value.trim() || 'Primary';
        lines.push('### ' + gname);
        g.querySelectorAll('.rb-ing').forEach(function (ing) {
          var qty  = ing.querySelector('.rb-qty').value.trim();
          var item = ing.querySelector('.rb-item').value.trim();
          if (item) lines.push(qty ? '- [ ] **' + qty + '** ' + item : '- [ ] ' + item);
        });
        lines.push('');
      });
    }

    lines.push('## Method');
    lines.push('');
    var steps = document.querySelectorAll('.rb-step');
    if (!steps.length) {
      lines.push('### 1. Step Name');
      lines.push('Step description.');
      lines.push('');
    } else {
      steps.forEach(function (step, i) {
        var sname = step.querySelector('.rb-sname').value.trim() || ('Step ' + (i + 1));
        var sdesc = step.querySelector('.rb-sdesc').value.trim();
        lines.push('### ' + (i + 1) + '. ' + sname);
        if (sdesc) lines.push(sdesc);
        lines.push('');
      });
    }

    var noteVals = Array.from(document.querySelectorAll('.rb-ntext'))
      .map(function (n) { return n.value.trim(); }).filter(Boolean);
    if (noteVals.length) {
      lines.push('!!! tip "Chef\'s Notes"');
      noteVals.forEach(function (n) { lines.push('    *   ' + n); });
      lines.push('');
    }

    lines.push('---');
    lines.push('*Tags: #' + category + '*');

    var md = lines.join('\n');
    document.getElementById('rb-code').textContent = md;
    document.getElementById('rb-filepath').textContent =
      'docs/recipes/' + category + '/' + slug(title) + '.md';
    var out = document.getElementById('rb-output');
    out.style.display = '';
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  document.getElementById('rb-copy').addEventListener('click', function () {
    var text = document.getElementById('rb-code').textContent;
    var btn  = this;
    function copied() {
      btn.textContent = 'Copied!';
      setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(copied);
    } else {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.style.cssText = 'position:fixed;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); copied(); } catch (e) {}
      document.body.removeChild(ta);
    }
  });

  addGroup('Primary');
  addStep();
})();
</script>
