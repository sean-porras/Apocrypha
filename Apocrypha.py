#################
#   APOCRYPHA   #
#    V.1.9.0    #
#################
"""
-=#=- Administrative Distribution Internal Documentation [ADID] -=#=-
    Apocrypha:
        I. from ecclesiastical Latin "Apocrypha (scripta)" meaning "hidden (writings)".
        II. the plane of Oblivion belonging to Hermaeus Mora, the Daedric Prince of Fate, Knowledge and Memory
"""
import os
import re
import sys
import time
import json
import random
import requests
import webbrowser
import secrets as s
import hashlib as h
from pathlib import Path
from math import floor, sqrt
from string import ascii_letters
from blake3 import blake3 as bl3
from dataclasses import dataclass
from base64 import b64encode as b64e


@dataclass
class Config:
    """
    The Config class object is used to create an easy library of attributes.
    These dictate the functions of the Apocrypha program.

    allow_cmdln: default True. Dictates whether or not command line can be used given all arguments
        rather than needing to go through the program step by step. ### CURRENTLY UNIMPLEMENTED ###
    casemod: default False. Dictates whether or not Apoc will be able to change the case of the letter
        it's trying to encrypt if the letter in its current case isn't able to be found.
    force_case: default True. Dictates whether or not Apoc will force all characters to be either
        all uppercase or all lowercase as determined by :lower_msg:, otherwise keeps original case
        and allows for mixed case messages. If you're planning on using a custom key using expanded
        hashing or custom .txt file, it's recommend to set this as False as those methods allows for mixed case.
    lower_msg: default True. Dictates whether or not Apoc will force all characters to be either
        all uppercase or all lowercase if :force_case: is True. Given :force_case: is True, and if lower_msg
        is True, the message will be forced to all lowercase, otherwise forces to uppercase.
    multi_in: default False. Dictates whether or not multiple runs of Apoc will be run on a single file
        containing commands for each separate result. ### CURRENTLY UNIMPLEMENTED ###
    output: default 'print'. Dictates what form the output of Apoc will be given as. Currently
        only supports printing the output. Future support for .txt, .json, and .apoc formats.
    force_msg_case: default False. Dictates whether or not Apoc will force all characters to be either all
        uppercase or all lowercase when using the `msg` encryption option. Must be used in conjunction with
        `force_case` to take effect.
    """
    allow_cmdln: bool = True
    casemod: bool = False
    force_case: bool = True
    lower_msg: bool = True
    multi_in: bool = False
    output: str = "print"  # in ['print', '.txt', '.json', '.apoc']
    force_msg_case: bool = False


def config_handler(fileloc: str = '') -> Config:
    """
    Looks for an existing config file to read from and set up, otherwise creates a config
    with default values and returns the resulting configuration from the file.
    :param fileloc: Str; Valid Path of file named "config.json"
    :returns: Config object
    """
    cc = json.dumps({'allow_cmdln': True, 'casemod': False, 'force_case': True, 'lower_msg': True, 'multi_in': False,
                     'output': 'print', 'force_msg_case': False},
                    sort_keys=True, indent=4)
    if Path('config.json').exists() or (fileloc == '' and Path('config.json').exists()):
        with open('config.json') as file:
            cc = json.load(file)
        try:
            return Config(cc['allow_cmdln'], cc['casemod'], cc['force_case'], cc['lower_msg'], cc['multi_in'],
                          cc['output'], cc['force_msg_case'])
        except KeyError:
            print("Error [I.C1]: Invalid config file, you can retry and specify a different JSON file.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    config_fileloc = input("cA_filepath: ")
                    return config_handler(config_fileloc)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    elif Path(fileloc).exists() and fileloc != '' and fileloc[-5:] == ".json":
        with open(fileloc) as file:
            cc = json.load(file)
        try:
            return Config(cc['allow_cmdln'], cc['casemod'], cc['force_case'], cc['lower_msg'], cc['multi_in'],
                          cc['output'], cc['force_msg_case'])
        except KeyError:
            print("Error [I.C2]: Invalid config file, you can retry and specify a different file location.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    config_fileloc = input("cA_filepath: ")
                    return config_handler(config_fileloc)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    else:
        with open('config.json', 'w') as file:
            file.write(cc)
        cc = json.loads(cc)
        return Config(bool(cc['allow_cmdln']), bool(cc['casemod']), bool(cc['force_case']), bool(cc['lower_msg']),
                      bool(cc['multi_in']), cc['output'], bool(cc['force_msg_case']))


def expanding_hash(invar: str, length: int = 5000) -> str:
    """
    Iteratively increases a given string into a hash containing characters specified below in the return docstring.
    :param invar: String to be expanded into a hash used for Apocrypha method encryption as the key.
    :param length: NonNegInteger; Defaults to 5000
    :return: k; Final key, string, contains upper and lowercase letters, numbers, periods, numbers, spaces, and commas.
    """
    # Extends invar a ton to make a key similar to the txt file from Apocrypha
    # Use this as a way to move around the {= --> ,} in a regularly irregular way in the final expanded key
    orignum1 = floor(sqrt(int(h.blake2b(invar[len(invar) // 2].encode('utf-8')).hexdigest().translate(
        {ord(c): None for c in ascii_letters}))))  # Cursed pseudo-random large number generated via hashing
    num1 = int(str(orignum1)[len(str(orignum1)) // 2:len(str(orignum1)) // 2 + 2])  # Take the middle 2 numbers
    k1 = b64e(bl3(invar.encode('utf-8')).digest()).decode('utf-8').replace(
        '+', '.').replace('/', ' ').replace('=', ',')  # Generates the first iteration
    if num1 // 2 > len(k1) - 1:  # Checks to see if middle 2 nums from cursed num is within the scope, otherwise mods it
        num1 = num1 // 3
    elif num1 > len(k1) - 1:
        num1 = num1 // 2
    k1 = k1[:num1] + k1[len(k1) - 1] + k1[num1:len(k1) - 1]  # Moves the ',' around by the num gen'd above for each iter
    itemlist1 = []
    for i in range(0, len(k1), len(k1) // 4):
        itemlist1.append(k1[i:i + len(k1) // 4])  # Divides each iteration into 4 segments
    itemorig = itemlist = item = itemlist1  # Sets up the stage for future iterations of final length :length:
    k = ''
    while len(k) < length:
        for i in range(0, len(itemorig)):
            orignum = floor(sqrt(int(h.blake2b(item[i][len(item[i]) // 2].encode('utf-8')).hexdigest().translate(
                {ord(c): None for c in ascii_letters}))))
            num = int(str(orignum)[len(str(orignum)) // 2:len(str(orignum)) // 2 + 2])
            knew = b64e(bl3(item[i].encode('utf-8')).digest()).decode('utf-8').replace(
                '+', '.').replace('/', ' ').replace('=', ',')
            if num // 2 > len(knew) - 1:
                num = num // 3
            elif num > len(knew) - 1:
                num = num // 2
            knew = knew[:num] + knew[len(knew) - 1] + knew[num:len(knew) - 1]
            for num in range(0, len(itemlist)):
                k += ''.join(itemlist[num])
            itemlist = []
            for j in range(0, len(knew), len(knew) // 4):
                itemlist.append(knew[j:j + len(knew) // 4])
        item = itemlist
    return k  # Returns the final key 'k' after a sufficient number of iterations to create the key with length :length:


def Aencode1(config: Config) -> str or None:
    """
    Generates and returns a key to be used for encryption in Aencode2.
    :param config: Config obj; Config object which allows for config options to be utilized.
    :return: str (valid link or custom key) or None (indicative of txt, json, or apoc file)
    """
    gentype = input("eA_gen.type[<python{INT};apocrypha;custom{full;param};file;msg>]: ")
    gentype = gentype.lower().strip()
    if gentype[:6] == "python":
        try:
            pynum = int(gentype[6:].strip())
            eAhex = s.token_hex(pynum // 2)
        except:
            print("Error [II.N1]: Invalid Input, using python64 generation method")
            eAhex = s.token_hex(32)
        eAloc = eAhex + "-w" + str(random.randint(1, 4)) + "-s" + str(random.randint(1, 5)) + "-v" + str(
            random.randint(1, 32)) + ":" + str(random.randint(1, 410))
        eAlink = "https://libraryofbabel.info/book.cgi?" + eAloc
        print(eAlink)
        return eAlink
    elif gentype == "apocrypha":
        key = requests.get('https://libraryofbabel.info/random.cgi')
        print(key.url)
        eAlink = key.url
        return eAlink
    elif gentype == "customfull":
        keyreq = input("eA_k.full = ")
        requests_keyreq = requests.get(keyreq)
        if requests_keyreq.status_code == 200:
            print("Success")
            return keyreq
        else:
            print("Error [II.L1]: Link did not have a status code of 200, using python64 generation method")
            eAhex = s.token_hex(32)
            eAloc = eAhex + "-w" + str(random.randint(1, 4)) + "-s" + str(random.randint(1, 5)) + "-v" + str(
                random.randint(1, 32)) + ":" + str(random.randint(1, 410))
            eAlink = "https://libraryofbabel.info/book.cgi?" + eAloc
            print(eAlink)
            return eAlink
    elif gentype == "customparam":
        keyparam = input("eA_k.param = ")
        if keyparam[0] == "?":
            keyrequrl = "https://libraryofbabel.info/book.cgi" + keyparam
            requests_keyreq = requests.get(keyrequrl)
            if requests_keyreq.status_code == 200:
                print("Success")
                return keyrequrl
            else:
                print("Error [II.L2]: Link did not have a status code of 200, using python64 generation method")
                eAhex = s.token_hex(32)
                eAloc = eAhex + "-w" + str(random.randint(1, 4)) + "-s" + str(random.randint(1, 5)) + "-v" + str(
                    random.randint(1, 32)) + ":" + str(random.randint(1, 410))
                eAlink = "https://libraryofbabel.info/book.cgi?" + eAloc
                print(eAlink)
                return eAlink
        else:
            keyrequrl = "https://libraryofbabel.info/book.cgi?" + keyparam
            requests_keyreq = requests.get(keyrequrl)
            if requests_keyreq.status_code == 200:
                print("Success")
                return keyrequrl
            else:
                print("Error [II.L3]: Link did not have a status code of 200, using python64 generation method")
                eAhex = s.token_hex(32)
                eAloc = eAhex + "-w" + str(random.randint(1, 4)) + "-s" + str(random.randint(1, 5)) + "-v" + str(
                    random.randint(1, 32)) + ":" + str(random.randint(1, 410))
                eAlink = "https://libraryofbabel.info/book.cgi?" + eAloc
                print(eAlink)
                return eAlink
    elif gentype == "file":
        print("WARNING: If you use a non-Apocrypha text file, it will not be as secure.")
        return None
    elif gentype == "msg":
        eAkey = input("eA_key = ") + ".msg"
        return eAkey
    else:
        print("Error [II.N2]: Invalid input, generating python64 location")
        eAhex = s.token_hex(32)
        eAloc = eAhex + "-w" + str(random.randint(1, 4)) + "-s" + str(random.randint(1, 5)) + "-v" + str(
            random.randint(1, 32)) + ":" + str(random.randint(1, 410))
        eAlink = "https://libraryofbabel.info/book.cgi?" + eAloc
        print(eAlink)
        return eAlink


def Aencode2(config: Config, key: str or None) -> None:
    """
    Given a key of either a valid link, custom key, or a NoneType, processes to encrypt and print the output.
    :param config: Config obj; Config object which allows for config options to be utilized
    :param key: str or None; str is indicative of a valid link or custom key, None is indicative of a file being used
    """
    if key is not None and key[-4:] not in [".txt", ".msg"] and key[-5:] not in [".json", ".apoc"]:
        print("The link to the key will now open, when you have downloaded the file, press enter")
        try:
            webbrowser.open(key)
        except:
            print("Error [II.W1]: unable to open the key link in a web browser, please open manually. Link: " + key)
        fileloc = input("eA_filepath = ")
    elif key is not None:
        if key[-4:] in [".txt", ".msg"] or key[-5:] in [".json", ".apoc"]:
            fileloc = key
        else:
            fileloc = ''
    else:
        fileloc = input("eA_filepath = ")
        key = fileloc
    if (Path(fileloc).exists() and fileloc != '') or key[-4:] == ".msg":
        if fileloc[-4:] in [".txt", ".msg"] or fileloc[-5:] in [".json", ".apoc"]:
            pass
        else:
            print("Error [II.F1]: File must be a .txt, .json, or .apoc file\nNOTE: Only .txt is supported currently.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    Aencode2(config, None)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
        print("NOTE: You can only use the following with Apocrypha files: letters, space, comma, and period")
        message = input("Message: ")
        if key[-4:] != ".msg" and config.lower_msg and config.force_case or \
                (key[-4:] == ".msg" and config.force_msg_case and config.lower_msg and config.force_case):
            message = message.lower()
        elif key[-4:] != ".msg" and not config.lower_msg and config.force_case or \
                (key[-4:] == ".msg" and config.force_msg_case and not config.lower_msg and config.force_case):
            message = message.upper()
        messagefinal = []
        if key is not None:
            if key[-4:] != ".msg" and fileloc != '':
                file = open(fileloc)
                origstrfile = file.read()
                file.close()
            else:
                try:
                    origstrfile = expanding_hash(key[:-4])
                except IndexError:
                    try:
                        print("Error [II.K1]: Invalid key. Likely blank key entered.")
                        if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                            Aencode2(config, input("eA_key = ")+".msg")
                        else:
                            os._exit(0)
                    except IndexError:
                        os._exit(0)
        else:
            file = open(fileloc)
            origstrfile = file.read()
            file.close()
        if len(origstrfile) < len(message):
            print("Error [II.E1]: Key file is not large enough to encrypt for your message.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    Aencode2(config, None)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
        strfile = origstrfile.replace("\n", "")
        t0 = time.time()
        unusedchars = list(set([ch for ch in strfile]).difference([ch for ch in message]))
        for ch in message:
            try:
                if ch != ".":  # It appears ^ is another escape character that's weird. To research and fix later.
                    chars = [m.start() for m in re.finditer(ch, strfile)]
                    if len(chars) == 0 and ch.upper() != ch.lower():
                        if ch.isupper() and config.casemod:
                            charused = random.choice([m.start() for m in re.finditer(ch.lower(), strfile)])
                            print("Warning: Character case has been modified.")
                        elif ch.islower() and config.casemod:
                            charused = random.choice([m.start() for m in re.finditer(ch.upper(), strfile)])
                            print("Warning: Character case has been modified.")
                        else:
                            # Use any unused character, modify and signify, modded character
                            try:
                                rchar = random.choice(unusedchars)
                                charused = (random.choice([m.start() for m in re.finditer(rchar, strfile)])+(1/ord(ch)))*-1
                            except:
                                print("Error [II.E2]: Couldn't encrypt message."
                                      "Unused character not found in key.")
                                try:
                                    if input("Retry with a new key (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                        Aencode2(config, None)
                                    else:
                                        os._exit(0)
                                except IndexError:
                                    os._exit(0)
                    else:
                        charused = random.choice(chars)
                else:
                    charused = random.choice([m.start() for m in re.finditer("\.", strfile)])
            except:
                # Use any unused character, modify and signify, modded character
                try:
                    rchar = random.choice(unusedchars)
                    charused = (random.choice([m.start() for m in re.finditer(rchar, strfile)])+(1/ord(ch)))*-1
                except:
                    print("Error [II.E3]: Couldn't encrypt message. Character not found in key.")
                    try:
                        if input("Retry with a new key (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                            Aencode2(config, None)
                        else:
                            os._exit(0)
                    except IndexError:
                        os._exit(0)
            messagefinal.append(charused)
            strfile = strfile[:floor(abs(charused))] + strfile[floor(abs(charused)) + 1:]
        keyhash = h.sha256(strfile.encode('utf-8')).hexdigest()
        t1 = time.time()
        print("\nTime: ", t1 - t0)
        messagefinal = [messagefinal, keyhash]
        print("\nEncrypted Message:\n")
        print(messagefinal)
        input("\nPress enter when done: ")
        os._exit(0)
    else:
        print("Error [II.P1]: Incorrect filepath.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                Aencode2(config, None)
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


# IDEA FOR FIXING ORD AND UNUSED CH ISSUE IN COMMENT
"""
Assign position number to be negative to not add that character to the final message,
Instead take the NEXT value which will be ord(that ch) + ord(real ch)
[-5749, 131] could be an unused 'B' at position 5749 with ord 66 for an actual 'A' with ord 65.
This is a LOT more secure as well. Could also multiply which would be [-5749, 4290]
NOTE: Execute the process of building the next number when a negative is found, perform operations as necessary.
This will prevent the base process from having to be modified to account for negatives and these cases.
Future iterations of encrypting characters not found in the key could perhaps implement primes in calculations?

Current implementation is good for pushing as 1.9.0, as well to save this iteration for posterity.
"""

# WEIRD CASES TO RESEARCH AND FIX
"""
IDEA:
Reorder so the unhandled/unused characters are used first so only one [m.start()] list comp. is executed.
Increases efficiency, and very well could fix some of the oddities below. UPDATE: Above comment works best in theory,
still best to attempt to only use one instance of list comprehension per character to increase efficiency.
msg: test
[[-1559.0285714285715], 'f63397f09f50998804abff7b26715a7df2a602fca8b7e192ae6471d424e190a5'] -> [@] gives ["]
    1/ord('@') = 0.015625
[[-3457.0285714285715], '9b50860fb659a2bb171e195f10c67630441e06cdc72fa930067dee8492741518'] -> [#] gives ["]
    1/ord('#') = 0.02857142857142857
    Variable assigned to this float keeps all figures.
    Figures different here begin 5 from the end, "42857" is just "5" in the enc. message
[[0], 'dd800d8b15ca503a1963d9c76a6bd9b5186ec7fe83f85a5adaa138fec140bde6'] -> [^] gives [S]
[[-1122.0238095238096], 'd28fbb2c137765fa87e847eac57fa0589b00ec54cd01140d0a3d298e145dfd42'] -> [*] gives [)]
[[-3036.008130081301, -101.008], '11cc112141554b44318f4f43a0c07e82bc3a07efb18803b03e55de31ad3ac041'] -> [{}] gives [A}]
[[-3036.008130081301], '11cc112141554b44318f4f43a0c07e82bc3a07efb18803b03e55de31ad3ac041'] gives [z] and key hash fail
[[-1051.0108695652175], 'ba580b622c5fd98ef399b0e32ec224e01607dbc5a379fd477a37d328f102b7b8'] -> [ \ ] gives { [ }
[[1816], '8686f969db0d40475d07cbf1c6c5ef1e1ae97741169bd965aee40f85ab878e00'] -> [|] gives [0]
[[-2442.029411764706], '9aacfdd5cb07b32a805888b00dd72d926c2557eb16c1cffa80ded71f7ae32f7e'] -> ["] gives [!]
[[-2213.016666666667], 'bdd2f417bdccef26feab04164837e5bee5a7034ec2acab02a02d8af543fb3b7a'] -> [<] gives [;]
[[-1997.0212765957447], '27c43ed5cd6cb400025f32785896b976852c2a8b3c00ac2f6e43a0615e856848'] -> [/] gives [.]
[[-3997.0158730158732], 'e7f13ab15c775b2f1ac46b407d0fc1a4b141613537fc768b0ac4830e18cfbeb3'] -> [?] gives [>]
[[-383.0104166666667], '0395be518faa12bf59925923c47ed5c6b4199ca296d71ce2bc0410151de144e3'] -> [`] gives [_]
[[-3223.0222222222224], '395a8746a45d8e70e67cfbf4f787fbd62d8250f4c0ea7f4143cafde7ce174d21'] -> [-] gives [,]
[[-226.01639344262296], '6b6d02eaeee80486a0f4f9df389610fd48093624c464f28fa4a9cf2cdfd131ef'] -> [=] gives [<]
[[-1835.0232558139535], '0785adec9c7beebc395024fcf08ba99c43d7f403b9e4b38c328297766af5d191'] -> [+] gives [*]
[[-1844.0040322580646], 'c103b4d0017fb240553bec027bb9177f65760721f875a9630c516336c77c4196'] -> [ø] gives [÷]
[[-3716.001041666667], 'b83a3fb415a794783072c939cdc92437aef84c93fdb2081075a2819f023da84a'] -> [π] gives [ο]
[[-4987.004484304933], 'c7d86da806ade48dbdc2fe4487f871b68cb9b28f500f992b8605aa0ae2caed2d'] -> [ß] gives [Þ]
[[-83.00011486331266], '5402c11cc94ba730c53577643de539605d003dbd69ba9d1f36333a72078667a6'] -> [∂] gives [∁]
[[-4974.0058139534885], '34d04b51f58a4db1a2dfd03604df09e9fb05f2d83d8aaf82415c56eb29d8035c'] -> [¬] gives [«]
[[-1133.004347826087], '92a7547045ca397fbe5dd89fd0545e4a721a1eece6413ee5ffbc3bb11702fd13'] -> [æ] gives [å]
[[-1732.0010672358592], 'dd245756505a6d0389f906d39a5ed74a8337f7a918e8f3e1b30ac7a81cd4a8ad'] -> [Ω] gives [Ψ]
[[-4474.000113947129], '55d069318025a9a77ae4c28af569025bdefcc81c5035eb8d144b3451ad7009a8'] -> [≈] gives [≇]
[[-3159.0001143249115], '18adaa973a290f3edd1fc5430954343a1a13040d9f6bd7d95b58f53a7658ab0a'] -> [∫] gives [∪]
[[-2612.0001135718344], '6cfd09b486b31a4b6e638dc7a7b2721db923de3b860a5da4f3b4b67f182e4d33'] -> [≥] gives [≤]
[[-3727.004048582996], 'cfd4555124af4e44b158886ca921f259a153c7ecbd198b5bf0de5ac41d535ab5'] -> [÷] gives [ö]
[[-769.0029585798817], 'e94f97a618c5184a290eb35d4dc9a1e56bbefaf371e080b68cc7e88e383615c3'] -> [Œ] gives [ő]
[[-2941.0051813471505], 'a8f06a60f6132cfd2f0d155b90d8f1cef5eb01263715188cdbb675fa784d527b'] -> [Á] gives [À]
[[-4496.005347593583], 'c57dc2cd4496e9c2d221a1652dcaaf5cb3485a309c1a2e2ba585965dbfbcb213'] -> [»] gives [º]
[[-521.005076142132], 'c7866361d599812c598737b47dbbba9cc0365fd46231c7b585cbffdbf95d0333'] -> [Å] gives [Ä]
[[-4752.0048780487805], '33a31df027de406a0cd28ddce25de77b85bf7d9e48cd03c2775965e0730d2429'] -> [Í] gives [Ì]
[[-413.0047393364929], '7ec5a555ba23e7d970a1b4f933decc505c200fa1bfe6c0843ce18af69d6f0f09'] -> [Ó] gives [Ò]
[[-238.00471698113208], '7ed2a7c7143b840f3b6c9af640b2577fb8823093119cf6b0e0e33ce2268f06fa'] -> [Ô] gives [Ó]
[[-4641.004761904762], 'b7efa41558055777fbab2bc8d7b15a439f7633484a4da2373769b2fac9a4ccbc'] -> [Ò] gives [Ñ]
[[-255.0032786885246], '92cc194bfd5692795529c081e3ee2cff39ce1889d6a7dd767b359840f9f7c49f'] -> [ı] gives [İ]
"""

'''Concept List:
  1. Get the user to DL the .txt file of the book [X]
  2. Have the user input the file location of the .txt file under a drive [X]
  3. Check to see if the file location is correct, if not, close the program [X]
  4. Create a list from the message via iter each ch and choose a random index of given ch, then remove. [X]
  5. Create hashes of the final key to validate encryption [X]
  6. Rework the decryption method to function again [X]
  7. If a hash does not exist with the message, work around to decode anyways [X]
  8. Ensure the file going to be opened is a .txt file [X]
  9. Prevent build if file length is shorter than the message to be encrypted [X]
  10. Clean up python gentype with any length of token [X]
  11. Add recursion functionality to retry failed/errored out parts of the program [X]
  12. Clean up the code base [while True: WIP]
  13. Create different versions of this program with certain restrictions [[Trashed, Admin vs Stable]]
    a. Public Dist: Require a hash that matches after decryption to display message [T]
    b. Private Dist: Only show final hash of the key and given, if not matching, display hashes, not the message [T]
    c. Admin Dist: Latest developer version, no restrictions, updated first for new features [X]
    d. Stable Dist: Current proven version with bug testing and absent of major errors [X]
  14. Create failsafe if ch is not found, end program, prompt for retry with a new key [X]
  15. Create administrative documentation and changelog for posterity [while True: WIP]
  16. Implement a function which simply uses any key to securely use with current method [X]
  17. Implement changing of unused characters in key for any character accepted as valid [WIP]
  18. Implement whole base program command line functionality [ ]
  ??. Implement custom config path persistence securely [ ]
  99. Create a new version which simply uses any key to securely use with no fail state. (Similar to AES) [ ]
'''


def Adecode2(config: Config, fileloc: str) -> None:
    """
    Given a valid file location or custom key, prompts for an encrypted message to decrypt and print the results.
    :param config: Config obj; Config object which allows for config options to be utilized.
    :param fileloc: Str; valid Path where the file is a .txt file or a custom key passed through with appended '.msg'
    :return: None; Final function using the Adecode1 helper function, prints to console.
    """
    try:
        if fileloc[-5:] in [".apoc", ".json"] or fileloc[-4:] in [".txt", ".msg"]:
            if fileloc[-4:] not in [".txt", ".msg", "apoc", "json"]:
                print("Error [III.F1]: File must be a .txt, .apoc, or .json file"
                      "NOTE: Only .txt files are supported as of now")
                try:
                    if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                        Adecode2(config, Adecode1(config))
                    else:
                        os._exit(0)
                except IndexError:
                    os._exit(0)
            if fileloc is not None:
                if fileloc[-4:] != ".msg" and fileloc != '':
                    if Path(fileloc).exists():
                        file = open(fileloc)
                        origstrfile = file.read()
                        file.close()
                else:
                    try:
                        origstrfile = expanding_hash(fileloc[:-4])
                    except IndexError:
                        try:
                            print("Error [III.K1]: Invalid key. Likely blank key entered.")
                            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                Adecode2(config, input("dA_key = ") + ".msg")
                            else:
                                os._exit(0)
                        except IndexError:
                            os._exit(0)
            else:
                if Path(fileloc).exists():
                    file = open(fileloc)
                    origstrfile = file.read()
                    file.close()
            keyhash = h.sha256(origstrfile.encode('utf-8')).hexdigest()
            encryptedmessage = input("dA_eM: ")
            strfile = origstrfile.replace("\n", "")
            listofencmessage = encryptedmessage.strip('][').split(', ')
            if "'" in listofencmessage[-1] and len(listofencmessage[-1]) == 66 and "]" not in listofencmessage[-1]:
                listofencmessage[-2] = ''.join(list(filter(lambda ch: ch not in "]", listofencmessage[-2])))
                msgkeyhash = listofencmessage[-1]
                msgkeyhash.replace("'", "")
                msgkeyhash = "".join(list(filter(lambda ch: ch not in "'", msgkeyhash)))
                encryptedmessage = str(listofencmessage[:-1])
            else:
                msgkeyhash = None
            if msgkeyhash is None:
                encryptedmessage = "".join(list(filter(lambda ch: ch not in "[',]", encryptedmessage)))
                finalmessage = []
                locationbuild = ""
                while True:
                    try:
                        if len(encryptedmessage) == 0:
                            locationbuild = float(locationbuild)
                            if locationbuild < 0:
                                # baseloc = abs(int(str(locationbuild)[:str(locationbuild).find('.')]))
                                try:
                                    ch = chr(abs(floor((1 / float(str(locationbuild)[str(locationbuild).find('.'):])))))
                                    finalmessage.append(ch)
                                except:
                                    print("Error [III.9B]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:locationbuild] + strfile[locationbuild + 1:]
                            finalkeyhash = h.sha256(strfile.encode('utf-8')).hexdigest()
                            finalkeyhash = ''.join(list(filter(lambda ch: ch not in "'", finalkeyhash)))
                            locationbuild = ""
                            finalmessage = "".join(finalmessage)
                            print("Decrypted Message:\n")
                            print(finalmessage)
                            print("\nKey Hash Match: Unknown, missing message hash.")
                            print("\nCurrent Final Key Hash: " + finalkeyhash)
                            print("Start Initial Key Hash: " + keyhash)
                            input("\nPress enter to close the program.")
                            os._exit(0)
                        elif encryptedmessage[0] != ' ':
                            locationbuild = "".join(locationbuild + encryptedmessage[0])
                            encryptedmessage = encryptedmessage[1:]
                        elif encryptedmessage[0] == ' ':
                            encryptedmessage = encryptedmessage[1:]
                            locationbuild = float(locationbuild)
                            if locationbuild < 0:
                                # baseloc = abs(int(str(locationbuild)[:str(locationbuild).find('.')]))
                                try:
                                    ch = chr(abs(floor((1 / float(str(locationbuild)[str(locationbuild).find('.'):])))))
                                    finalmessage.append(ch)
                                except:
                                    print("Error [III.9A]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:floor(abs(locationbuild))] + strfile[floor(abs(locationbuild)) + 1:]
                            locationbuild = ""
                    except:
                        print("Error [III.D1]: Unable to decrypt message.\n"
                              "Probable Cause: Incorrect/Too Small of a key file.")
                        try:
                            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                Adecode2(config, Adecode1(config))
                            else:
                                os._exit(0)
                        except IndexError:
                            os._exit(0)
            elif msgkeyhash is not None:
                encryptedmessage = "".join(list(filter(lambda ch: ch not in "[',]", encryptedmessage)))
                finalmessage = []
                locationbuild = ""
                while True:
                    try:
                        if len(encryptedmessage) == 0:
                            locationbuild = float(locationbuild)
                            if locationbuild < 0:
                                # baseloc = abs(int(str(locationbuild)[:str(locationbuild).find('.')]))
                                try:
                                    ch = chr(abs(floor((1/float(str(locationbuild)[str(locationbuild).find('.'):])))))
                                    finalmessage.append(ch)
                                except:
                                    print("Error [III.9D]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:int(floor(abs(locationbuild)))]+strfile[int(floor(abs(locationbuild)))+1:]
                            finalkeyhash = h.sha256(strfile.encode('utf-8')).hexdigest()
                            finalkeyhash = ''.join(list(filter(lambda ch: ch not in "'", finalkeyhash)))
                            locationbuild = ""
                            finalmessage = "".join(finalmessage)
                            print("Decrypted Message:\n")
                            print(finalmessage)
                            if finalkeyhash != msgkeyhash:
                                print("\nWARNING: Key Hash Matching Fail. Message is likely incorrect.")
                            print("\nKey Hash Match: " + str(finalkeyhash == msgkeyhash))
                            print("\nMessage Final Key Hash: " + msgkeyhash)
                            print("Current Final Key Hash: " + finalkeyhash)
                            print("Start Initial Key Hash: " + keyhash)
                            input("\nPress enter to close the program.")
                            os._exit(0)
                        elif encryptedmessage[0] != ' ':
                            locationbuild = "".join(locationbuild + encryptedmessage[0])
                            encryptedmessage = encryptedmessage[1:]
                        elif encryptedmessage[0] == ' ':
                            encryptedmessage = encryptedmessage[1:]
                            locationbuild = float(locationbuild)
                            if locationbuild < 0:
                                baseloc = floor(locationbuild)*-1
                                try:
                                    ch = chr(abs(floor(1/(locationbuild+baseloc))))
                                    finalmessage.append(ch)
                                except:
                                    print("Error [III.9C]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:int(floor(abs(locationbuild)))]+strfile[int(floor(abs(locationbuild)))+1:]
                            locationbuild = ""
                    except:
                        print("Error [III.D2]: Unable to decrypt message."
                              "Probable Cause: Incorrect/Too Small of a key file.")
                        try:
                            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                Adecode2(config, Adecode1(config))
                            else:
                                os._exit(0)
                        except IndexError:
                            os._exit(0)
        else:
            print("Error [III.F2]: Incorrect file type.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    Adecode2(config, Adecode1(config))
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    except:
        print("Error [III.U1]: Unexpected error. Likely NoneType given for file location")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                Adecode1(config)
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


def Adecode1(config: Config) -> str:
    """
    Helper function which starts the decryption process and prompts the user to return the path
    of a valid file path (.txt required in Adecode2) or input a custom key.
    :param config: Config obj; Config object which allows for config options to be utilized.
    :return: Str; File path or key with appended '.msg' string to be processed by Adecode2
    """
    keyformat = input("dA_k.format[<link{full;param};file;msg>]: ")
    keyformat = keyformat.lower()
    if keyformat == "linkparam":
        locreq = input("dA_param = ")
        if locreq[0] == '?':
            baseurl = 'https://libraryofbabel.info/book.cgi'
            cache = requests.get(baseurl + locreq)
            print(baseurl + locreq)
            if cache.status_code == 200:
                print("Download the key file. It will open momentarily.")
                time.sleep(1)
                try:
                    webbrowser.open(baseurl + locreq)
                except:
                    print("Error [III.W1]: Failed to open key link, please open manually. Link: " + baseurl + locreq)
                fileloc = input("dA_filepath = ")
                return fileloc
            else:
                print("Error [III.L1]: Link did not have a status code of 200.")
                try:
                    if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                        Adecode1(config)
                    else:
                        os._exit(0)
                except IndexError:
                    os._exit(0)
        else:
            baseurl = 'https://libraryofbabel.info/book.cgi?'
            cache = requests.get(baseurl + locreq)
            print(baseurl + locreq)
            if cache.status_code == 200:
                print("Download the key file. It will open momentarily.")
                time.sleep(1)
                try:
                    webbrowser.open(baseurl + locreq)
                except:
                    print("Error [III.W2]: Failed to open key link, please open manually. Link: " + baseurl + locreq)
                fileloc = input("dA_filepath = ")
                return fileloc
            else:
                print("Error [III.L2]: Link did not have a status code of 200.")
                try:
                    if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                        Adecode1(config)
                    else:
                        os._exit(0)
                except IndexError:
                    os._exit(0)
    elif keyformat == "linkfull":
        locreq = input("dA_loc = ")
        cache = requests.get(locreq)
        print(locreq)
        if cache.status_code == 200:
            print("Download the key file. It will open momentarily.")
            time.sleep(1)
            try:
                webbrowser.open(locreq)
            except:
                print("Error [III.W3]: Failed to open key link, please open manually. Link: " + locreq)
            fileloc = input("dA_filepath = ")
            return fileloc
        else:
            print("Error [III.L3]: Link did not have a status code of 200.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    Adecode1(config)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    elif keyformat == "file":
        fileloc = input("dA_filepath = ")
        return fileloc
    elif keyformat == "msg":
        fileloc = input("dA_key = ") + ".msg"
        return fileloc
    else:
        print("Error [III.N1]: Invalid Option.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                Adecode1(config)
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


def main():
    print("A_version: 1.9.0")
    EncOrDec = input("A_func<E;D;C>: ").lower()
    if EncOrDec[0] == 'e':
        config = config_handler()
        k = Aencode1(config)
        Aencode2(config, k)
    elif EncOrDec[0] == 'd':
        config = config_handler()
        Adecode2(config, Adecode1(config))
    elif EncOrDec[0] == 'c':
        config_fileloc = input("cA_filepath: ")
        config_handler(config_fileloc)
        _ = os.system('cls' if os.sys.platform == 'win32' else 'clear')
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        print("Error [I.M1]: Invalid input.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                main()
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


if __name__ == "__main__":
    main()
