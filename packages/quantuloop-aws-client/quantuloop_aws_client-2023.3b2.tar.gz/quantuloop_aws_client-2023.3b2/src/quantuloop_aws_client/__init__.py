"""Client for Quantuloop Quantum Simulator Suite for HPC on AWS"""

from __future__ import annotations
# Copyright 2023 Quantuloop
from ctypes import *
from io import BytesIO
from os import PathLike, path
from time import time
from typing import Literal
from random import Random
import getpass
import json
import zipfile
from ket import quantum_exec_timeout
from ket.base import set_quantum_execution_target
from ket.clib.libket import JSON
import requests
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

PRIVATE_KEY = ""
URL = ""
VERIFY = True
TIMEOUT = 0

AVAILABLE_SIMULATORS = []
SIMULATOR = ''
RNG = Random()
DUMP_TYPE = 'shots'
SHOTS = '1024'
GPU_COUNT = '1'
PRECISION = '1'

__all__ = ['available_simulators', 'set_server', 'set_simulator']


def available_simulators() -> list[str]:
    """Get a list of the available quantum simulators."""

    global AVAILABLE_SIMULATORS
    AVAILABLE_SIMULATORS = requests.get(
        URL+'/simulators', timeout=30, verify=VERIFY).json()

    return AVAILABLE_SIMULATORS


def set_server(*,
               url: str,
               private_key: PathLike,
               passphrase: bool | bytes | None = None,
               verify: bool = True,
               timeout: int | None = None):
    """Set the server URL and private key for quantum execution

    Args:
        url: Server URL, for example, https://example.com or http://127.0.0.1:8080.
        private_key: Path for the OpenSSH RSA private key.
        passphrase: Password to decrypt the private key. Set to ``True`` to prompt for the password, or pass the password in plain text in bytes. Set to ``None`` if the key is not encrypted.
        verify: Set to ``False`` to not verify the SSL certificate that may be invalid if using the Application Load Balancer domain with HTTPS.
        timeout: Set a timeout in seconds for the quantum execution requests.
    """
    global PRIVATE_KEY
    with open(path.expandvars(path.expanduser(private_key)), 'rb') as file:
        if passphrase:
            if isinstance(passphrase, bool):
                passphrase = bytes(getpass.getpass(
                    f'passphrase for {private_key}:'), 'utf-8')
        else:
            passphrase = None

        PRIVATE_KEY = serialization.load_ssh_private_key(
            file.read(), password=passphrase, backend=default_backend()
        )

    global URL
    URL = str(url)

    global VERIFY
    VERIFY = bool(verify)

    if timeout:
        timeout = int(timeout)
        global TIMEOUT
        TIMEOUT = timeout
        quantum_exec_timeout(timeout)

    available_simulators()


def set_simulator(simulator: str | None = None, *,
                  seed: any | None = None,
                  dump_type: str | None = None,
                  shots: int | None = None,
                  gpu_count: int | None = None,
                  precision: Literal[1, 2] | None = None):
    """Set the simulation server as the quantum execution target.

    You must run :func:`quantuloop_aws_client.set_server` before calling this function.

    Quantuloop QueST is not affected by the "precision" and "gpu_count" parameters 
    as it is only available for single GPU and single precision execution.        

    .. warning::

        Your internet connection can strongly influence the total execution time when
        setting the "dump_type" parameter to "vector" or "probability".

    Args:
        simulator: See :func:`quantuloop_aws_client.available_simulators` for the available simulators.
        seed: Initialize the simulator RNG.
        dump_type: must be "vector", "probability", or "shots", default "vector".
        shots: select the number of shots if ``dump_type`` is "shots".
        gpu_count: maximum number of GPUs; if set to 0, simulation will use all available GPUs.
        precision: floating point precision used in the simulation; positive values are: 1 for single precision (float) and 2 for double precision
    """

    if simulator is not None:
        simulator = simulator.lower()
        if simulator not in AVAILABLE_SIMULATORS:
            raise ValueError(
                f"parameter 'simulator' must be in {AVAILABLE_SIMULATORS}"
            )
        global SIMULATOR
        SIMULATOR = simulator

    if seed is not None:
        global RNG
        RNG = Random(seed)

    if dump_type:
        if dump_type not in ["vector", "probability", "shots"]:
            raise ValueError(
                'parameter "dump_type" must be "vector", "probability", or "shots"')
        global DUMP_TYPE
        DUMP_TYPE = dump_type

    if shots:
        if shots < 1:
            raise ValueError('parameter "shots" must be greater than one')
        global SHOTS
        SHOTS = str(shots)

    if gpu_count is not None:
        global GPU_COUNT
        GPU_COUNT = str(int(gpu_count))

    if precision is not None:
        if precision not in [1, 2]:
            raise ValueError('parameter "dump_type" must be int(1) or int(2)')
        global PRECISION
        PRECISION = str(int(precision))

    set_quantum_execution_target(_send_quantum_code)


def _send_quantum_code(process):
    process.serialize_quantum_code(JSON)
    process.serialize_metrics(JSON)

    code_data, code_size, _ = process.get_serialized_quantum_code()
    metrics_data, metrics_size, _ = process.get_serialized_metrics()

    iat = int(time())
    exp = iat+(60*8 if TIMEOUT == 0 else TIMEOUT)

    payload = {
        'simulator': SIMULATOR,
        'seed': str(RNG.getrandbits(64)),
        'dump_type': DUMP_TYPE,
        'shots': SHOTS,
        'gpu_count': GPU_COUNT,
        'precision': PRECISION,
        'timeout': TIMEOUT,
        'iat': iat,
        'exp': exp,
    }

    token = jwt.encode(payload, PRIVATE_KEY, algorithm='PS256',)

    request_files = BytesIO()
    with zipfile.ZipFile(request_files, 'w',
                         compression=zipfile.ZIP_BZIP2,
                         compresslevel=9) as zip_file:
        zip_file.writestr('token.jwt', token)
        zip_file.writestr('quantum_code.json',
                          bytearray(code_data[:code_size.value]))
        zip_file.writestr('quantum_metrics.json',
                          bytearray(metrics_data[:metrics_size.value]))

    zipped_result = requests.get(
        URL+'/run',
        files={
            'request.zip': ('request.zip', request_files.getvalue(), 'application/zip')
        },
        timeout=None if TIMEOUT == 0 else TIMEOUT,
        verify=VERIFY
    ).content

    try:
        with zipfile.ZipFile(BytesIO(zipped_result), 'r') as zip_file:
            result = zip_file.read('result.json')

        result_size = len(result)

        process.set_serialized_result(
            (c_uint8*result_size)(*result),
            result_size,
            JSON
        )
    except zipfile.BadZipFile:
        raise RuntimeError(json.loads(zipped_result))
