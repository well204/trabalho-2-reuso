import time
from threading import Semaphore

MAX_CONCURRENT_OCR = 3
RETRY_TIMES = 3
CIRCUIT_THRESHOLD = 3
CIRCUIT_TIMEOUT = 30

bulkhead_semaphore = Semaphore(MAX_CONCURRENT_OCR)
circuit_failures = 0
circuit_opened_at = None

def is_circuit_open():
    global circuit_opened_at
    if circuit_opened_at is None:
        return False

    if time.time() - circuit_opened_at > CIRCUIT_TIMEOUT:
        return False
    
    return True

def register_failure():
    global circuit_failures, circuit_opened_at
    circuit_failures += 1
    if circuit_failures >= CIRCUIT_THRESHOLD:
        circuit_opened_at = time.time()

def register_success():
    global circuit_failures, circuit_opened_at
    circuit_failures = 0
    circuit_opened_at = None