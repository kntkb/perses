"""
Settings objects for the different protocols using gufe objects.

This module implements the objects that will be needed to run relative binding free
energy calculations using perses.
"""

from gufe.settings.models import ProtocolSettings
from openff.units import unit
from perses.protocols.utils import _serialize_pydantic

# Default settings for the lambda functions
x = 'lambda'
DEFAULT_ALCHEMICAL_FUNCTIONS = {
    'lambda_sterics_core': x,
    'lambda_electrostatics_core': x,
    'lambda_sterics_insert': f"select(step({x} - 0.5), 1.0, 2.0 * {x})",
    'lambda_sterics_delete': f"select(step({x} - 0.5), 2.0 * ({x} - 0.5), 0.0)",
    'lambda_electrostatics_insert': f"select(step({x} - 0.5), 2.0 * ({x} - 0.5), 0.0)",
    'lambda_electrostatics_delete': f"select(step({x} - 0.5), 1.0, 2.0 * {x})",
    'lambda_bonds': x,
    'lambda_angles': x,
    'lambda_torsions': x
}

class NonEqCyclingSettings(ProtocolSettings):
    """
    Settings for the relative free energy setup protocol.

    Attributes
    ----------
    ligand_input : str
        The path to the ligand input file.
    ligand_index : int
        The index of the ligand in the ligand input file.
    solvent_padding : float
        The amount of padding to add to the ligand in nanometers.
    forcefield : ForceFieldSettings
        The force field settings to use.
    alchemical : AlchemicalSettings
        The alchemical settings to use.
    """
    class Config:
        arbitrary_types_allowed = True

    # Lambda settings
    lambda_functions = DEFAULT_ALCHEMICAL_FUNCTIONS
    # lambda_windows = 11
    # alchemical settings
    softcore_LJ_v2 = True
    interpolate_old_and_new_14s = False
    phase = 'vacuum'

    forcefield_files = [
        "amber/ff14SB.xml",
        "amber/tip3p_standard.xml",
        "amber/tip3p_HFE_multivalent.xml",
        "amber/phosaa10.xml",
    ]
    small_molecule_forcefield = 'openff-2.0.0'

    timestep = 4.0 * unit.femtoseconds
    neq_splitting = "V R H O R V"
    eq_steps = 1000
    neq_steps = 100

    platform = 'CUDA'
    save_frequency = 100
    phase = 'vacuum'

    def _gufe_tokenize(self):
        return _serialize_pydantic(self)