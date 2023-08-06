import sys
import typing


def convert_from_particle_system():
    ''' Add a new curves object based on the current state of the particle system

    '''

    pass


def convert_to_particle_system():
    ''' Add a new or update an existing hair particle system on the surface object

    '''

    pass


def delete():
    ''' Remove selected control points or curves

    '''

    pass


def sculptmode_toggle():
    ''' Enter/Exit sculpt mode for curves

    '''

    pass


def select_all(action: typing.Union[str, int] = 'TOGGLE'):
    ''' (De)select all control points

    :param action: Action, Selection action to execute * TOGGLE Toggle -- Toggle selection for all elements. * SELECT Select -- Select all elements. * DESELECT Deselect -- Deselect all elements. * INVERT Invert -- Invert selection of all elements.
    :type action: typing.Union[str, int]
    '''

    pass


def select_end(end_points: bool = True, amount: int = 1):
    ''' Select end points of curves

    :param end_points: End Points, Select points at the end of the curve as opposed to the beginning
    :type end_points: bool
    :param amount: Amount, Number of points to select
    :type amount: int
    '''

    pass


def select_less():
    ''' Shrink the selection by one point

    '''

    pass


def select_linked():
    ''' Select all points in curves with any point selection

    '''

    pass


def select_more():
    ''' Grow the selection by one point

    '''

    pass


def select_random(seed: int = 0, probability: float = 0.5):
    ''' Randomizes existing selection or create new random selection

    :param seed: Seed, Source of randomness
    :type seed: int
    :param probability: Probability, Chance of every point or curve being included in the selection
    :type probability: float
    '''

    pass


def set_selection_domain(domain: typing.Union[str, int] = 'POINT'):
    ''' Change the mode used for selection masking in curves sculpt mode

    :param domain: Domain
    :type domain: typing.Union[str, int]
    '''

    pass


def snap_curves_to_surface(attach_mode: typing.Union[str, int] = 'NEAREST'):
    ''' Move curves so that the first point is exactly on the surface mesh

    :param attach_mode: Attach Mode, How to find the point on the surface to attach to * NEAREST Nearest -- Find the closest point on the surface for the root point of every curve and move the root there. * DEFORM Deform -- Re-attach curves to a deformed surface using the existing attachment information. This only works when the topology of the surface mesh has not changed.
    :type attach_mode: typing.Union[str, int]
    '''

    pass


def surface_set():
    ''' Use the active object as surface for selected curves objects and set it as the parent

    '''

    pass
