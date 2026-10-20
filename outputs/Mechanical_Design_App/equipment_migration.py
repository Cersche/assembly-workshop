"""Compatibility for retired saved equipment ids, isolated from normal geometry."""
import copy
from equipment_examples import EXAMPLE_ID, example_item


def migrate(value):
    """Return a converted draft and whether conversion occurred. Preserve assembly verbatim."""
    draft = copy.deepcopy(value)
    changed = False
    racks = draft.get('racks', [])
    if not isinstance(racks, list):
        return draft, False
    for rack in racks:
        if not isinstance(rack, dict):
            continue
        placements = rack.get('placements', [])
        if not isinstance(placements, list):
            continue
        for placement in placements:
            if not isinstance(placement, dict):
                continue
            if placement.get('equipment') != 'pi4':
                continue
            changed = True
            placement['equipment'] = EXAMPLE_ID
            placement['geometry'] = 'equipment-library'
            span = placement.get('span', 1)
            if isinstance(span, int) and 1 <= span <= 5 and isinstance(placement.get('tray', {}), dict):
                placement.setdefault('tray', {}).setdefault('u', span)
            # The former preview used the top U as its base; generic equipment uses the bottom U.
            # Keep the old world-space port positions, including partial saved overrides and cable ids.
            if isinstance(span, int) and span > 1:
                if not isinstance(rack.get('cabling', {}), dict):
                    continue  # The ordinary schema validator reports malformed data.
                ports = rack.setdefault('cabling', {}).setdefault('ports', [])
                if not isinstance(ports, list) or any(not isinstance(p, dict) for p in ports):
                    continue
                existing = {p['port']: p for p in ports if p.get('allocation') == placement.get('id')}
                for base in example_item()['spec']['planning_ports']:
                    edit = existing.get(base['id'])
                    if edit is None:
                        edit = {'allocation': placement['id'], 'port': base['id']}
                        ports.append(edit)
                    edit['z'] = edit.get('z', base['z']) + (span - 1) * 44.45
                for edit in ports:
                    if edit.get('allocation') == placement.get('id') and edit.get('custom') and 'z' in edit:
                        edit['z'] += (span - 1) * 44.45
    return draft, changed
