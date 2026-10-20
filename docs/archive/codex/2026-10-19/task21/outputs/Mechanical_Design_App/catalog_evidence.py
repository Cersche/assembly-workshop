"""Offline inspection of catalog evidence. Never promotes metadata into fit approval."""
import math

COMMON = ('manufacturer','part_number','units','material','finish','retrieved',
          'availability','redistribution_status')
SCREW = ('length','length_convention','threaded_length','head_style','drive',
         'head_diameter','head_height','shank_diameter','dimensional_tolerances')
INSERT = ('installation_method','length','outside_diameter','hole_profile',
          'hole_diameter','usable_depth','min_wall','dimensional_tolerances')

def validate_profile(part):
    """Optional source-described axial segments; deliberately not a geometry adapter."""
    profile=part.get('installation_hole_segments')
    if profile is None:return
    if part.get('kind')!='heatset' or part.get('hole_profile')!='segmented':
        raise ValueError('Axial segments require a heatset with hole_profile segmented.')
    if not isinstance(profile,list) or not profile:
        raise ValueError('installation_hole_segments must be a nonempty list.')
    end=0.0
    for segment in profile:
        keys={'z0','z1','diameter0','diameter1','source'}
        if not isinstance(segment,dict) or set(segment)!=keys:
            raise ValueError('Each segment needs z0,z1,diameter0,diameter1,source only.')
        values=[segment[k] for k in ('z0','z1','diameter0','diameter1')]
        if any(type(x) not in (float,int) or not math.isfinite(x) for x in values):
            raise ValueError('Segment dimensions must be finite mm numbers.')
        z0,z1,d0,d1=values
        if z0<0 or z1<=z0 or d0<=0 or d1<=0 or abs(z0-end)>1e-9:
            raise ValueError('Segments must be contiguous from z=0 with positive lengths/diameters.')
        if not isinstance(segment['source'],str) or not segment['source'].strip():
            raise ValueError('Each segment requires source evidence.')
        end=z1

def inspect(part):
    required=COMMON+(SCREW if part['kind']=='screw' else INSERT)
    missing=[k for k in required if part.get(k) in (None,'')]
    declared=part.get('unknown_fields',[])
    evidence=part.get('manufacturer_installation_evidence',{})
    return dict(id=part['id'],revision=part['revision'],verification=part['verification'],
                missing_fields=missing,declared_unknowns=declared,
                source=part['source'],source_document=part.get('source_document'),
                installation_evidence=evidence,
                installation_resolution=part.get('installation_evidence_resolution'),
                installation_conflicts=[evidence['hole_tolerance_conflict']] if evidence.get('hole_tolerance_conflict') and part.get('installation_evidence_resolution',{}).get('status')!='resolved_project_basis' else [],
                geometry_scope='Existing Pi4 M3 adapter only; catalog coverage does not extend geometry support',
                physical_approval=False)
