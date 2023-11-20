#!/usr/bin/env python3
import os
import sys
import re
import argparse
import yaml
import cashaddress
from typing import Union
import time
from sms import send_sms

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(file_path))

from btc_address_dump import mnemonic_util
from btc_address_dump import wif_util
from btc_address_dump import p2pkh_util
from btc_address_dump import p2wpkh_util
from btc_address_dump import p2sh_p2wpkh_util
from btc_address_dump import p2tr_util
from btc_address_dump import common_util

from itertools import permutations
#import winsound
#from pymempool import MempoolAPI


def get_base58_prefix(coins_info, chain: str, typ: str) -> Union[bytes, None]:
    if coins_info[chain]["base58_prefix"][typ] is None:
        return None
    else:
        return coins_info[chain]["base58_prefix"][typ].to_bytes(1, byteorder='big')


def get_bech32_hrp(coins_info, chain: str) -> Union[str, None]:
    return coins_info[chain]["bech32_hrp"]


def get_derivation_path(coins_info, chain: str, typ: str) -> Union[str, None]:
    try:
        derivation_path = coins_info[chain]["hd_path"][typ]
    except KeyError:
        derivation_path = None
    return derivation_path


def main_entry(input):
    mnemonic = ''
    private_key = b''
    public_key_compressed = b''
    public_key_hash160 = b''
    addr_p2wpkh = ''


    file = open(os.path.join(os.path.abspath(file_path), "coins.yaml"), 'r', encoding="utf-8")
    file_data = file.read()
    file.close()

    coins_info = yaml.load(file_data, Loader=yaml.FullLoader)

    chain = 'btc'
    derivation = 'bip84'
    inputs = input

    # See https://en.bitcoin.it/wiki/List_of_address_prefixes
    #pubkey_version_bytes = get_base58_prefix(coins_info, chain, 'pubkey')  # 0x00 for btc mainnet, 0x6f for testnet
    #script_version_bytes = get_base58_prefix(coins_info, chain, 'script')  # 0x05 for btc mainnet, 0xc4 for testnet
    #wif_version_bytes = get_base58_prefix(coins_info, chain, 'wif')  # 0x80 for btc mainnet, 0xef for testnet
    human_readable_part = get_bech32_hrp(coins_info, chain)  # "bc" for btc mainnet, and "tb" for testnet

    if re.search("^([a-zA-Z]+\\s){11}([a-zA-Z]+).*$", inputs):
        # 12 mnemonic words
        # For example: olympic wine chicken argue unaware bundle tunnel grid spider slot spell need
        # sys.stderr.write("you input mnemonic\n")
        mnemonic = inputs
        derivation_path = derivation if derivation.startswith("m/") else get_derivation_path(coins_info, chain, derivation)

        private_key = mnemonic_util.mnemonic_to_private_key(mnemonic, derivation_path)

        public_key_compressed = common_util.prikey_to_pubkey(private_key, compressed=True)

        # For bech32 address
        addr_p2wpkh = p2wpkh_util.pubkey_to_segwit_v0_addr(human_readable_part, public_key_compressed)

    else:
        sys.stderr.write("invalid input: {0}\n".format(inputs))
        sys.exit(1)

    if addr_p2wpkh:

        if addr_p2wpkh == 'bc1qr8d58qxzrp9ztyazhqw2u0e9dpnpl2gkwg9t8e':

            print("mnemonic = {}".format(mnemonic))

            if addr_p2wpkh:
                if public_key_hash160:
                    print("bech32 address (only valid if input is hash160 of COMPRESSED public key) = {}".format(addr_p2wpkh))
                else:
                    print("bech32 address (p2wpkh) = {}".format(addr_p2wpkh))

            return True


        elif public_key_hash160 == 'bc1qr8d58qxzrp9ztyazhqw2u0e9dpnpl2gkwg9t8e':

            print("mnemonic = {}".format(mnemonic))
  
            if addr_p2wpkh:
                if public_key_hash160:
                    print("bech32 address (only valid if input is hash160 of COMPRESSED public key) = {}".format(addr_p2wpkh))
                else:
                    print("bech32 address (p2wpkh) = {}".format(addr_p2wpkh))
            return True


    return False


if __name__ == '__main__':

    words = ["Law", "Hundred", "Found", "Transfer", "Life", "Blouse", "Wine", "Sting", "Congress", "Aerobic", "Simple", "Hazard"]
    all_permutations = permutations(words)
    keys = []
    for permutation in all_permutations:
        start_time = time.time()
        main_entry(" ".join(permutation))
        end_time = time.time()
        print("time: ", end_time-start_time)
        if main_entry(" ".join(permutation)):
            print('\a')
            #winsound.Beep(440, 50)
            print("\n\n\n---------------------!!!!! HHHHIIIITTTT !!!!!---------------------\n\n\n")

            print(permutation)
            keys.append(permutation)
            message = f"PERMUTATION GEFUNDEN!!!\nPermutation: {permutation}\nJuhuu wir sind reich baby!"
            #send_sms(message)

            break


    print(keys)
    print("Done all permutations")

