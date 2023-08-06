from typing import Any, Callable, Dict, List, Optional
from time import time

import numpy as np
from ase import Atoms
from .fastatomstruct import *
from tidynamics import msd


def chunks(indices: List[int], n: int):
    """Yield successive chunks from list of atoms."""
    for i in range(0, len(indices), n):
        yield indices[i : i + n]


def ipar(
    func: Callable, atoms: List[Atoms], *args: List[Any], **kwargs: Dict[Any, Any]
):
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        print("\nImage parallelization report\n" + "----------------------------")

    if rank == 0:
        res_full, t0_f = [], time()

    for i, c in enumerate(chunks(list(range(len(atoms))), comm.size)):
        while len(c) < comm.size:
            c.append(None)

        if rank == 0:
            per = (len(c) - np.count_nonzero([ci is None for ci in c])) / len(c)
            t0 = time()
        if c[rank] is not None:
            a = atoms[c[rank]]
            res = func(a, *args, **kwargs)
        else:
            res = None

        res = comm.gather(res, root=0)
        if rank == 0:
            t = time() - t0
            print(f"Chunk {i + 1}: {per * 100:03.2f}% | {t:.2f} s")
            res_full.extend(res)

    if rank == 0:
        for i in range(len(res_full) - 1, -1, -1):
            if res_full[i] is None:
                del res_full[i]
        print("----------------------------")
        print(f"Total: {(time() - t0_f):.2f} s\n")
    else:
        res_full = None

    return res_full


def static_structure_factor(
    atoms: List[Atoms],
    q: np.ndarray,
    r_max: float,
    n_bins: int,
    filter: Optional[Filter] = None,
) -> np.ndarray:
    """Static structure factor, as calculated from the RDF.

    For isotropic systems, the static structure factor can be calculated using

    .. math::

        S(q) = q + 4 \pi \\rho \int_0^\infty r (g(r) - 1) \\frac{\sin{qr}}{q} dr,

    with :math:`q` the absolute value of the reciprocal vector and :math:`g(r)`
    the radial distribution function.

    Arguments:
        atoms (ase.Atoms or List[ase.Atoms]): Atoms object(s) from ASE
        q (np.ndarray): Array with values of :math:`q`
        r_max (float): Cutoff radius for calculating the radial distribution function
        n_bins (int): Number of bins for calculating the radial distribution function
        filter (fastatomstruct.Filter): Filter applied to the atoms

    Returns:
        np.ndarray of floats with values of :math:`S(q)`

    Examples
    --------

    The exemplary file "Sb540.traj" `can be found here <https://zivgitlab.uni-muenster.de/ag-salinga/fastatomstruct/-/raw/master/regressiontesting/Structures/Sb540.traj>`_.

    >>> import fastatomstruct as fs
    >>> import numpy as np
    >>> from ase import io
    >>> atoms = io.read("Sb540.traj")
    >>> q = np.linspace(0.1, 10, 100)
    >>> fs.static_structure_factor(atoms, q, 10, 100)
    array([ 2.38192150e+00,  1.52370665e+00,  6.46487735e-01,  1.56760937e-01,
            1.20323650e-01,  2.76121498e-01,  2.99045859e-01,  8.31513912e-02,
           -1.90316248e-01, -2.47717736e-01, -2.64701388e-03,  3.32212401e-01,
            4.12935073e-01,  8.23095798e-02, -4.33279251e-01, -6.37901553e-01,
           -1.34285685e-01,  1.02734748e+00,  2.30245828e+00,  2.97459962e+00,
            2.63495154e+00,  1.47795768e+00,  1.95200237e-01, -4.64900582e-01,
           -1.67915414e-01,  8.23636781e-01,  1.86264373e+00,  2.35654147e+00,
            2.12370925e+00,  1.44199006e+00,  7.96081378e-01,  5.32944085e-01,
            6.68269224e-01,  9.48456321e-01,  1.08128433e+00,  9.46956728e-01,
            6.48174186e-01,  3.96442496e-01,  3.47315244e-01,  5.10293291e-01,
            7.78951127e-01,  1.03029307e+00,  1.20441057e+00,  1.31266361e+00,
            1.39040807e+00,  1.44917566e+00,  1.46855988e+00,  1.42365507e+00,
            1.31353477e+00,  1.16335792e+00,  1.00360668e+00,  8.51865026e-01,
            7.15775063e-01,  6.10344434e-01,  5.65892631e-01,  6.11851235e-01,
            7.47484590e-01,  9.27629136e-01,  1.08202234e+00,  1.15793322e+00,
            1.15344778e+00,  1.11384177e+00,  1.09289068e+00,  1.10994910e+00,
            1.13732027e+00,  1.12748028e+00,  1.05705663e+00,  9.51231920e-01,
            8.68843102e-01,  8.60366739e-01,  9.31803892e-01,  1.04118569e+00,
            1.12787974e+00,  1.15066369e+00,  1.10732762e+00,  1.02633983e+00,
            9.43038802e-01,  8.80934999e-01,  8.48915518e-01,  8.48906335e-01,
            8.81116102e-01,  9.40582699e-01,  1.01098283e+00,  1.06655300e+00,
            1.08547102e+00,  1.06556309e+00,  1.02825219e+00,  1.00491362e+00,
            1.01457151e+00,  1.05006526e+00,  1.08377161e+00,  1.08843837e+00,
            1.05674417e+00,  1.00482220e+00,  9.58470246e-01,  9.34461644e-01,
            9.31941120e-01,  9.38971544e-01,  9.46172717e-01,  9.54459745e-01])
    """
    if isinstance(atoms, list):
        rdf = []
        for a in atoms:
            r, rdf_i = radial_distribution_function(a, r_max, n_bins, filter)
            rdf.append(rdf_i)
        rdf = np.mean(rdf, axis=0)
        rho = len(atoms[0]) / atoms[0].get_volume()
    else:
        r, rdf = radial_distribution_function(atoms, r_max, n_bins)
        rho = len(atoms) / atoms.get_volume()

    integral = np.zeros(len(q))
    for i, qi in enumerate(q):
        integrand = r[1:] * np.sin(qi * r[1:]) * (rdf[1:] - 1)
        integral[i] = np.trapz(integrand, r[1:])
    return 1 + 4 * np.pi * rho / q * integral


def __convert_pos(atoms) -> List[np.ndarray]:
    pos = []
    for i in range(len(atoms[0])):
        pos_temp = np.empty((len(atoms), 3))
        for j, a in enumerate(atoms):
            pos_temp[j, :] = a.positions[i, :]
        pos.append(pos_temp)
    return pos


def mean_squared_displacement(atoms: List[Atoms]) -> np.ndarray:
    return squared_displacement(atoms).mean(axis=0)


def squared_displacement(atoms: List[Atoms]) -> np.ndarray:
    pos = __convert_pos(atoms)
    m = [msd(p) for p in pos]
    return np.array(m)
