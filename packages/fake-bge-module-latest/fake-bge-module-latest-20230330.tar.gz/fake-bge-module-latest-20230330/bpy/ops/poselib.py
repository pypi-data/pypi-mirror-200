import sys
import typing


def apply_pose_asset(blend_factor: float = 1.0, flipped: bool = False):
    ''' Apply the given Pose Action to the rig

    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it
    :type blend_factor: float
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: bool
    '''

    pass


def blend_pose_asset(blend_factor: float = 0.0,
                     flipped: bool = False,
                     release_confirm: bool = False):
    ''' Blend the given Pose Action to the rig

    :param blend_factor: Blend Factor, Amount that the pose is applied on top of the existing poses. A negative value will subtract the pose instead of adding it
    :type blend_factor: float
    :param flipped: Apply Flipped, When enabled, applies the pose flipped over the X-axis
    :type flipped: bool
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button
    :type release_confirm: bool
    '''

    pass
