from common import CHAIN_IDS
from exceptions import InvalidUsage
import re

def validate_chain_id(chain_id):
    if chain_id is None or chain_id not in CHAIN_IDS:
        raise InvalidUsage(f"Invalid chain_id {chain_id}")
    
def validate_evm_address(evm_address):
    case_insensitive = re.compile("^(0x)?[0-9a-f]{40}$", re.IGNORECASE)
    all_caps = re.compile("^(0x)?[0-9A-F]{40}$")
    lower_case = re.compile("^(0x)?[0-9a-f]{40}$")
    if not case_insensitive.match(evm_address) or (not all_caps.match(evm_address) and lower_case.match(evm_address)):
        raise InvalidUsage(f"Invalid EVM address {evm_address}")

def validate_number_string(number):
    if not number or len(number) <= 0:
        raise InvalidUsage(f"Invalid number string {number}")
    
    for i in range(0, len(number)):
        if number[i] < '0' or number[i] > '9':
            raise InvalidUsage(f"Invalid char {number[i]} in string {number}")
