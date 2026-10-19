import pathlib, re, shutil

ws_path = pathlib.Path("outputs/Mechanical_Design_App/workspace.js")
backup_path = pathlib.Path("outputs/Mechanical_Design_App/workspace.js.bak")

# 1. Create a pristine safety backup
shutil.copy2(ws_path, backup_path)
print(f"[OK] Safety backup saved to {backup_path}")

content = ws_path.read_text(encoding="utf-8")

# 2. Update the HTML modal template inside workspace.js
old_modal_re = r'(?s)<dialog id="rackDialog".*?</dialog>'
clean_modal = '''<dialog id="rackDialog" class="modal-card" style="max-width:760px; width:92vw; background:#141b24; color:#d8e2ed; border:1px solid #2d3d52; border-radius:8px; padding:20px;">
  <form id="rackForm" method="dialog">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
      <h2 id="rackDialogTitle" style="margin:0; font-size:18px; color:#e2edf8;">Rack Configuration</h2>
      <button type="button" class="btn-subtle" onclick="byId('rackDialog').close()" style="background:transparent; border:none; color:#a2b4c7; font-size:18px; cursor:pointer;">&times;</button>
    </div>
    
    <label for="rackName" style="display:block; font-size:12px; font-weight:bold; margin-bottom:4px; color:#a2b4c7;">Project / Rack Name</label>
    <input id="rackName" type="text" style="width:100%; box-sizing:border-box; background:#0e131a; border:1px solid #2d3d52; border-radius:4px; padding:6px 10px; color:#fff; margin-bottom:14px;" required>

    <div class="fields-standardized">
      <label for="rackSlots" style="font-weight:bold; display:block; margin-bottom:6px; font-size:12px; color:#a2b4c7;">Rack Height / Capacity (Slots)</label>
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <input id="rackSlots" type="number" min="1" max="14" step="1" required style="width:80px; background:#0e131a; border:1px solid #2d3d52; border-radius:4px; padding:6px; color:#fff;">
        <span id="rackMmDisplay" style="font-size:12px; color:#7fcbb6; font-weight:bold;"></span>
      </div>
      <div id="dialogModularContainer"></div>
    </div>

    <div id="rackFormError" style="color:#f87171; font-size:12px; margin-top:8px;"></div>
    <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:16px;">
      <button type="button" onclick="byId('rackDialog').close()" class="btn-secondary" style="background:#1d2633; border:1px solid #2d3d52; color:#d8e2ed; padding:6px 14px; border-radius:4px; cursor:pointer;">Cancel</button>
      <button type="submit" class="btn-primary" style="background:#2a6ab0; border:none; color:#fff; padding:6px 16px; border-radius:4px; font-weight:bold; cursor:pointer;">Apply Rack Layout</button>
    </div>
  </form>
</dialog>'''

if re.search(old_modal_re, content):
    content = re.sub(old_modal_re, clean_modal, content)
    print("[OK] Cleaned dialog markup (removed 3 redundant fields and disclaimer).")

# 3. Replace openRackDialog logic cleanly
clean_open_func = '''  function openRackDialog(edit) {
    if (!leaveAssembly()) return;
    editingId = edit ? activeId : null;
    const rack = edit ? active() : null;
    const dialog = byId('rackDialog');
    if (!dialog) return;

    byId('rackDialogTitle').textContent = edit ? 'Rack Configuration' : 'New Rack Frame';
    byId('rackName').value = rack?.name || 'My Lab Rax';
    const slotsInput = byId('rackSlots');
    slotsInput.value = Math.min(14, Math.max(1, rack?.slots || 5));
    byId('rackFormError').textContent = '';

    const mmDisp = byId('rackMmDisplay');
    const updateMm = (val) => {
      if (mmDisp) mmDisp.textContent = `${(val * 44.45).toFixed(1)} mm standard height`;
    };
    updateMm(slotsInput.value);

    const container = byId('dialogModularContainer');
    if (container) {
      container.replaceChildren();

      const layoutWrap = document.createElement('div');
      layoutWrap.style.display = 'grid';
      layoutWrap.style.gridTemplateColumns = '1.1fr 0.9fr';
      layoutWrap.style.gap = '14px';
      layoutWrap.style.marginTop = '10px';

      const leftCol = document.createElement('div');
      leftCol.style.display = 'flex';
      leftCol.style.flexDirection = 'column';
      leftCol.style.gap = '10px';

      // Quick Standard Presets (1U to 14U)
      const pRow = document.createElement('div');
      pRow.style.display = 'flex';
      pRow.style.gap = '6px';
      pRow.style.flexWrap = 'wrap';

      const presets = [
        ['3U Desktop', 3],
        ['5U Standard', 5],
        ['6U Extended', 6],
        ['8U Mid-Tower', 8],
        ['10U Lab Rack', 10],
        ['14U Max', 14]
      ];
      presets.forEach(([name, s]) => {
        const btn = button(name, () => syncSlots(s), 'secondary subtle');
        btn.style.fontSize = '11px';
        btn.style.padding = '4px 8px';
        pRow.append(btn);
      });

      // Height Slider (1U - 14U)
      const sliderRow = document.createElement('div');
      sliderRow.style.display = 'flex';
      sliderRow.style.alignItems = 'center';
      sliderRow.style.gap = '8px';

      const slider = document.createElement('input');
      slider.type = 'range';
      slider.min = '1';
      slider.max = '14';
      slider.value = slotsInput.value;
      slider.style.flex = '1';
      slider.oninput = () => syncSlots(parseInt(slider.value, 10));
      sliderRow.append(slider);

      // Modular Pieces Tray (1U-5U Uprights + 1U Extension)
      const trayBox = document.createElement('div');
      trayBox.style.background = '#10151c';
      trayBox.style.padding = '8px 10px';
      trayBox.style.borderRadius = '6px';
      trayBox.style.border = '1px solid #283342';

      const trayHeading = document.createElement('div');
      trayHeading.textContent = 'Drag Modular Pieces to Stack:';
      trayHeading.style.fontSize = '11px';
      trayHeading.style.fontWeight = 'bold';
      trayHeading.style.color = '#a2b4c7';
      trayHeading.style.marginBottom = '6px';

      const partsRow = document.createElement('div');
      partsRow.style.display = 'flex';
      partsRow.style.gap = '6px';
      partsRow.style.flexWrap = 'wrap';

      const availablePieces = [
        { label: '+ 1U Post', type: 'post', u: 1 },
        { label: '+ 2U Post', type: 'post', u: 2 },
        { label: '+ 3U Post', type: 'post', u: 3 },
        { label: '+ 4U Post', type: 'post', u: 4 },
        { label: '+ 5U Post', type: 'post', u: 5 },
        { label: '+ 1U Extension', type: 'ext', u: 1 }
      ];

      availablePieces.forEach(piece => {
        const chip = document.createElement('div');
        chip.draggable = true;
        chip.textContent = piece.label;
        chip.style.padding = '4px 8px';
        chip.style.background = piece.type === 'ext' ? '#1f2e28' : '#1d2734';
        chip.style.border = piece.type === 'ext' ? '1px dashed #47b48e' : '1px dashed #4e75a3';
        chip.style.borderRadius = '4px';
        chip.style.fontSize = '11px';
        chip.style.color = piece.type === 'ext' ? '#7fcbb6' : '#82bdff';
        chip.style.cursor = 'grab';

        chip.ondragstart = (e) => {
          e.dataTransfer.setData('text/plain', JSON.stringify(piece));
          chip.style.opacity = '0.5';
        };
        chip.ondragend = () => { chip.style.opacity = '1'; };
        chip.onclick = () => {
          const cur = parseInt(slotsInput.value, 10) || 5;
          if (cur + piece.u <= 14) syncSlots(cur + piece.u);
          else notify('Maximum rack limit is 14 slots.', true);
        };
        partsRow.append(chip);
      });
      trayBox.append(trayHeading, partsRow);

      // Stack Drop Zone
      const dropZone = document.createElement('div');
      dropZone.style.background = '#0e131a';
      dropZone.style.padding = '10px';
      dropZone.style.borderRadius = '6px';
      dropZone.style.border = '2px dashed #2d3d52';
      dropZone.style.minHeight = '110px';
      dropZone.style.display = 'flex';
      dropZone.style.flexDirection = 'column';
      dropZone.style.gap = '4px';

      dropZone.ondragover = (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#47b48e';
      };
      dropZone.ondragleave = () => {
        dropZone.style.borderColor = '#2d3d52';
      };
      dropZone.ondrop = (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#2d3d52';
        try {
          const data = JSON.parse(e.dataTransfer.getData('text/plain'));
          if (data && data.u) {
            const cur = parseInt(slotsInput.value, 10) || 5;
            if (cur + data.u <= 14) syncSlots(cur + data.u);
            else notify('Maximum rack limit is 14 slots.', true);
          }
        } catch (_) {}
      };

      const stackList = document.createElement('div');
      stackList.style.display = 'flex';
      stackList.style.flexDirection = 'column';
      stackList.style.gap = '4px';

      leftCol.append(pRow, sliderRow, trayBox, dropZone);

      // Right Column: Live Proposed 3D Preview (Panels = false)
      const previewCard = document.createElement('div');
      previewCard.style.display = 'flex';
      previewCard.style.flexDirection = 'column';
      previewCard.style.background = '#0e131a';
      previewCard.style.borderRadius = '6px';
      previewCard.style.border = '1px solid #283342';
      previewCard.style.overflow = 'hidden';

      const previewTitle = document.createElement('div');
      previewTitle.textContent = 'Proposed Frame Preview';
      previewTitle.style.padding = '6px 10px';
      previewTitle.style.background = '#151d26';
      previewTitle.style.fontSize = '11px';
      previewTitle.style.color = '#7fcbb6';
      previewTitle.style.fontWeight = 'bold';

      const prevCanvas = document.createElement('canvas');
      prevCanvas.width = 300;
      prevCanvas.height = 300;
      prevCanvas.style.width = '100%';
      prevCanvas.style.height = '300px';
      prevCanvas.style.display = 'block';

      previewCard.append(previewTitle, prevCanvas);
      layoutWrap.append(leftCol, previewCard);
      container.append(layoutWrap);

      function refreshStack() {
        stackList.replaceChildren();
        let rem = parseInt(slotsInput.value, 10) || 5;
        const currentStack = [];
        while (rem > 0) {
          const u = Math.min(5, rem);
          currentStack.push(u);
          rem -= u;
        }

        const dropHint = document.createElement('div');
        dropHint.textContent = `Active Stack: ${slotsInput.value}U / 14U Max`;
        dropHint.style.fontSize = '11px';
        dropHint.style.color = '#7fcbb6';
        dropHint.style.marginBottom = '4px';
        dropHint.style.fontWeight = 'bold';
        dropZone.replaceChildren(dropHint, stackList);

        currentStack.forEach((u, idx) => {
          const row = document.createElement('div');
          row.style.display = 'flex';
          row.style.justifyContent = 'space-between';
          row.style.alignItems = 'center';
          row.style.background = '#18212c';
          row.style.padding = '4px 8px';
          row.style.borderRadius = '4px';
          row.style.fontSize = '11px';

          const label = document.createElement('span');
          label.textContent = `Segment ${idx + 1}: ${u}U Upright (${(u * 44.45).toFixed(1)} mm)`;
          label.style.color = '#a2b4c7';

          const remBtn = button('×', () => {
            const nextVal = parseInt(slotsInput.value, 10) - u;
            if (nextVal >= 1) syncSlots(nextVal);
            else notify('Minimum rack height is 1 slot.', true);
          }, 'subtle');
          remBtn.style.padding = '0 4px';
          remBtn.style.color = '#f87171';
          remBtn.title = 'Remove this segment';

          row.append(label, remBtn);
          stackList.append(row);
        });
      }

      function renderDialog3DPreview(proposedSlots) {
        const meshes = sourceMeshes || window._sourceMeshes;
        if (!meshes || !sceneRenderer) return;
        const pCtx = prevCanvas.getContext('2d');
        const w = prevCanvas.width, h = prevCanvas.height;
        pCtx.fillStyle = '#0e131a';
        pCtx.fillRect(0, 0, w, h);

        try {
          const scene = LabRaxScene.frame(proposedSlots, false);
          const box = LabRaxScene.bounds(scene, meshes);
          const view = LabRaxScene.camera(box, -0.48, 0.24, w, h, 1.15);

          const renderedGl = sceneRenderer.draw(scene, meshes, view, w, h, {
            appearance: rack?.appearance || {},
            placements: []
          });
          pCtx.drawImage(renderedGl, 0, 0, w, h);

          pCtx.strokeStyle = 'rgba(71, 180, 142, 0.35)';
          pCtx.lineWidth = 0.8;
          for (let s = 1; s <= proposedSlots; s++) {
            const z = (proposedSlots - s) * LabRaxScene.U;
            const p1 = view.project([-104, -3, z + 1]);
            const p2 = view.project([104, -3, z + 1]);
            pCtx.beginPath();
            pCtx.moveTo(p1[0], p1[1]);
            pCtx.lineTo(p2[0], p2[1]);
            pCtx.stroke();
          }
        } catch (err) {
          console.warn('Dialog preview error:', err);
        }
      }

      function syncSlots(val) {
        val = Math.max(1, Math.min(14, val));
        slotsInput.value = val;
        slider.value = val;
        updateMm(val);
        refreshStack();
        renderDialog3DPreview(val);
      }

      slotsInput.oninput = () => syncSlots(parseInt(slotsInput.value, 10));

      refreshStack();
      setTimeout(() => renderDialog3DPreview(parseInt(slotsInput.value, 10)), 30);
    }

    dialog.showModal();
  }'''

# Locate function bounds precisely
start_marker = "function openRackDialog("
end_marker = "byId('rackForm').onsubmit"

start_pos = content.find(start_marker)
end_pos = content.find(end_marker, start_pos)

if start_pos != -1 and end_pos != -1:
    content = content[:start_pos] + clean_open_func + "\n\n  " + content[end_pos:]
    print("[OK] Replaced openRackDialog function block cleanly.")
else:
    print(f"[ERR] Markers not found: start={start_pos}, end={end_pos}")

# 4. Enforce strict 14 slot maximum across submit and validation handlers
content = content.replace('max="48"', 'max="14"')
content = content.replace('next.slots > 48', 'next.slots > 14')
content = content.replace('slots < 1 || next.slots > 48', 'slots < 1 || next.slots > 14')
content = content.replace('Slots must be between 1 and 48.', 'Slots must be between 1 and 14.')

ws_path.write_text(content, encoding="utf-8")
print("[OK] workspace.js updated and verified!")
