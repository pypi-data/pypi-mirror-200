#!/usr/bin/env python
""" Util classes """
__author__ = "Alec Thomson"

import logging as logger
from dataclasses import dataclass
from typing import Tuple, Optional, Union
import numpy as np
from astropy.io import fits
from radio_beam import Beam, Beams
from astropy import units as u
from racs_tools import au2

@dataclass
class ImageData():
    """ Dataclass for 2D image data """
    filename: str
    image: np.ndarray
    ndim: int
    header: fits.Header
    old_beam: Beam
    nx: int
    ny: int
    dx: u.Quantity
    dy: u.Quantity

    # Ensure image is 2D
    def __post__init__(self):
        assert self.image.ndim == 2, "Image must be 2D"

    def getbeam(self, new_beam: Beam, cutoff: Union[float, None] = None) -> Tuple[Beam, float]:
        logger.info(f"Current beam is {self.old_beam!r}")

        if cutoff is not None and self.old_beam.major.to(u.arcsec) > cutoff * u.arcsec:
            conbm = Beam(
                major=np.nan * u.deg,
                minor=np.nan * u.deg,
                pa=np.nan * u.deg,
            )
            fac = np.nan
            return conbm, fac

        if new_beam == self.old_beam:
            conbm = Beam(
                major=0 * u.deg,
                minor=0 * u.deg,
                pa=0 * u.deg,
            )
            fac = 1.0
            logger.warning(
                f"New beam {new_beam!r} and old beam {self.old_beam!r} are the same. Won't attempt convolution."
            )
            return conbm, fac
        try:
            conbm = new_beam.deconvolve(self.old_beam)
        except Exception as err:
            logger.warning(f"Could not deconvolve. New: {new_beam!r}, Old: {self.old_beam!r}")
            raise err
        fac, amp, outbmaj, outbmin, outbpa = au2.gauss_factor(
            beamConv=[
                conbm.major.to(u.arcsec).value,
                conbm.minor.to(u.arcsec).value,
                conbm.pa.to(u.deg).value,
            ],
            beamOrig=[
                self.old_beam.major.to(u.arcsec).value,
                self.old_beam.minor.to(u.arcsec).value,
                self.old_beam.pa.to(u.deg).value,
            ],
            dx1=self.dx.to(u.arcsec).value,
            dy1=self.dy.to(u.arcsec).value,
        )
        return conbm, fac