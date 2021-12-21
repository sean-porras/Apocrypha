#################
#   APOCRYPHA   #
#    V.1.8.5    #
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
        return Config(cc['allow_cmdln'], cc['casemod'], cc['force_case'], cc['lower_msg'], cc['multi_in'], cc['output'],
                      cc['force_msg_case'])
    elif Path(fileloc).exists() and fileloc != '' and fileloc[-11:] == "config.json":
        with open(fileloc) as file:
            cc = json.load(file)
        return Config(cc['allow_cmdln'], cc['casemod'], cc['force_case'], cc['lower_msg'], cc['multi_in'], cc['output'],
                      cc['force_msg_case'])
    else:
        with open('config.json', 'w') as file:
            file.write(cc)
        cc = json.loads(cc)
        return Config(bool(cc['allow_cmdln']), bool(cc['casemod']), bool(cc['force_case']), bool(cc['lower_msg']),
                      bool(cc['multi_in']), cc['output'], bool(cc['force_msg_case']))


def expanding_hash(invar: str, length: int = 5000) -> str:  # Currently Unimplemented
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
            print("Error: Invalid Input, using python64 generation method")
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
            print("Error: Link did not have a status code of 200, using python64 generation method")
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
                print("Error: Link did not have a status code of 200, using python64 generation method")
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
                print("Error: Link did not have a status code of 200, using python64 generation method")
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
        eAkey = input("Key Message: ") + ".msg"
        return eAkey
    else:
        print("Error: Incorrect input, generating python64 location")
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
            print("Error in opening the key link in a web browser, please open manually. Link: " + key)
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
            print("Error: File must be a .txt, .json, or .apoc file\nNOTE: Only .txt is supported currently.")
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
                origstrfile = expanding_hash(key[:-4])
        else:
            file = open(fileloc)
            origstrfile = file.read()
            file.close()
        if len(origstrfile) < len(message):
            print("Error: Key file is not large enough to encrypt for your message.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    Aencode2(config, None)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
        strfile = origstrfile.replace("\n", "")
        t0 = time.time()
        for ch in message:
            try:
                if ch != ".":
                    chars = [m.start() for m in re.finditer(ch, strfile)]
                    if len(chars) == 0 and ch.upper() != ch.lower():
                        if ch.isupper() and config.casemod:
                            charused = random.choice([m.start() for m in re.finditer(ch.lower(), strfile)])
                            print("Warning: Character case has been modified.")
                        elif ch.islower() and config.casemod:
                            charused = random.choice([m.start() for m in re.finditer(ch.upper(), strfile)])
                            print("Warning: Character case has been modified.")
                        else:
                            print("Error: Couldn't encrypt message. Character not found in key in upper or lower.")
                            input("Press enter to continue and retry with a new key.")
                            Aencode2(config, None)
                    else:
                        charused = random.choice(chars)
                    # charused = random.choice([m.start() for m in re.finditer(ch, strfile)])  # Replace w/above
                else:
                    charused = random.choice([m.start() for m in re.finditer("\.", strfile)])  # Replace w/chars in
            except:
                print("Error: Couldn't encrypt message. Character not found in key.")
                input("Press enter to continue and retry with a new key.")
                Aencode2(config, None)
            messagefinal.append(charused)
            strfile = strfile[:charused] + strfile[charused + 1:]
        keyhash = h.sha256(strfile.encode('utf-8')).hexdigest()
        t1 = time.time()
        print("\nTime: ", t1 - t0)
        messagefinal = [messagefinal, keyhash]
        print("\nEncrypted Message:\n")
        print(messagefinal)
        input("\nPress enter when done: ")
        os._exit(0)
    else:
        print("Error: Incorrect filepath.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                Aencode2(config, None)
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


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
  13. Create different versions of this program with certain restrictions [[WIP]]
    a. Public Dist: Require a hash that matches after decryption to display message [ ]
    b. Private Dist: Only show final hash of the key and given, if not matching, display hashes, not the message [ ]
    c. Admin Dist: Current version, no restrictions, updated for parity features [X]
  14. Create failsafe if ch is not found, end program, prompt for retry with a new key [X]
  15. Create administrative documentation and changelog for posterity [WIP]
  16. Implement a function which simply uses any key to securely use with current method [X]
  17. Implement whole base program command line functionality [ ]
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
                print("Error: File must be a .txt, .apoc, or .json file\nNOTE: Only .txt files are supported as of now")
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
                    origstrfile = expanding_hash(fileloc[:-4])
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
                            locationbuild = int(locationbuild)
                            finalmessage.append(strfile[locationbuild])
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
                            locationbuild = int(locationbuild)
                            finalmessage.append(strfile[locationbuild])
                            strfile = strfile[:locationbuild] + strfile[locationbuild + 1:]
                            locationbuild = ""
                    except:
                        print("Error: Unable to decrypt message.\n"
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
                            locationbuild = int(locationbuild)
                            finalmessage.append(strfile[locationbuild])
                            strfile = strfile[:locationbuild] + strfile[locationbuild + 1:]
                            finalkeyhash = h.sha256(strfile.encode('utf-8')).hexdigest()
                            finalkeyhash = ''.join(list(filter(lambda ch: ch not in "'", finalkeyhash)))
                            locationbuild = ""
                            finalmessage = "".join(finalmessage)
                            print("Decrypted Message:\n")
                            print(finalmessage)
                            if finalkeyhash == msgkeyhash:
                                pass
                            elif finalkeyhash != msgkeyhash:
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
                            locationbuild = int(locationbuild)
                            finalmessage.append(strfile[locationbuild])
                            strfile = strfile[:locationbuild] + strfile[locationbuild + 1:]
                            locationbuild = ""
                    except:
                        print("Error: Unable to decrypt message."
                              "Probable Cause: Incorrect/Too Small of a key file.")
                        try:
                            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                Adecode2(config, Adecode1(config))
                            else:
                                os._exit(0)
                        except IndexError:
                            os._exit(0)
        else:
            print("Error: Incorrect file type.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    Adecode2(config, Adecode1(config))
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    except:
        print("Error: Unexpected error. Likely NoneType given for file location")
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
                    print("Error: Failed to open key link, please open manually. Link: " + baseurl + locreq)
                fileloc = input("dA_filepath = ")
                return fileloc
            else:
                print("Error: Link did not have a status code of 200.")
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
                    print("Error: Failed to open key link, please open manually. Link: " + baseurl + locreq)
                fileloc = input("dA_filepath = ")
                return fileloc
            else:
                print("Error: Link did not have a status code of 200.")
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
                print("Error: Failed to open key link, please open manually. Link: " + locreq)
            fileloc = input("dA_filepath = ")
            return fileloc
        else:
            print("Error: Link did not have a status code of 200.")
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
        print("Error: Invalid Option.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                Adecode1(config)
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


def main():
    print("A_version: 1.8.5")
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
        print("Error: Invalid input.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                main()
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


if __name__ == "__main__":
    main()
