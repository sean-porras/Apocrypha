#################
#   APOCRYPHA   #
#    V.1.1.0    #
#################
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
    multi_in: default False. Dictates whether or not multiple runs of Apoc will be run on a single file
        containing commands for each separate result. ### CURRENTLY UNIMPLEMENTED ###
    output: default 'print'. Dictates what form the output of Apoc will be given as. Currently
        only supports printing the output. Future support for .txt, .json, and .apoc formats.
    """
    allow_cmdln: bool = True
    multi_in: bool = False
    output: str = "print"  # in ['print', '.txt', '.json', '.apoc']


def config_subsys(cf: dict) -> dict:
    """
    The subsystem in charge of taking in and modifying a dictionary according to user
    input. Constantly runs in the subsystem until the user enters the command to quit/exit.
    :param cf: Dictionary; This dictionary with config options is modified and returned
    :return: Dictionary; Modified cf dictionary post-user processing.
    """
    stay = True
    default = {'allow_cmdln': True, 'multi_in': False, 'output': 'print'}
    print("Config Handler Subsystem. Type 'help' for commands.")
    while stay:
        inp = input("> ").lower()
        if inp == "help":
            print("The Config Handler Subsystem allows you to modify and save config settings within\n"
                  "the program itself to then return and use upon an automatic restart of the program.\n")
            print("Commands:\n"
                  "help: prints out this list\n"
                  "default: Returns all values to their defaults\n"
                  "allow_cmdln: Allows you to edit the 'allow_cmdln' config option\n"
                  "multi_in: Allows you to edit the 'multi_in' config option\n"
                  "output: Allows you to edit the 'output' config option\n"
                  "exit/quit: Exits the Config Handler Subsystem\n")
        elif inp in ["exit", "quit"]:
            stay = False
        elif inp == "default":
            cf = default
            stay = False
        elif inp == "allow_cmdln":
            print("allow_cmdln is currently: "+str(cf['allow_cmdln']))
            print("Valid options: True, False")
            opt = input(">>> ")
            if opt in ["True", "False"]:
                cf['allow_cmdln'] = bool(opt)
            else:
                print("Invalid Input.")
        elif inp == "multi_in":
            print("multi_in is currently: "+str(cf['multi_in']))
            print("Valid options: True, False")
            opt = input(">>> ")
            if opt in ["True", "False"]:
                cf['multi_in'] = bool(opt)
            else:
                print("Invalid Input.")
        elif inp == "output":
            print("output is currently: "+cf['output'])
            print("Valid options: print, .txt, .json, .apoc")
            opt = input(">>> ")
            if opt in ["print", ".txt", ".json", ".apoc"]:
                cf['output'] = opt
            else:
                print("Invalid Input.")
    return cf


def config_handler(fileloc: str = '', cfSUBSYS: bool = None) -> Config:
    """
    Looks for an existing config file to read from and set up, otherwise creates a config
    with default values and returns the resulting configuration from the file.
    :param fileloc: Str; Valid Path of file named "config.json"
    :param cfSUBSYS: bool; None by default, if not None, allows the user to change config options
    :returns: Config object
    """
    cd = {'allow_cmdln': True, 'multi_in': False, 'output': 'print'}
    cc = json.dumps(cd, sort_keys=True, indent=4)
    if Path('config.json').exists() or (fileloc == '' and Path('config.json').exists()):
        with open('config.json') as file:
            cc = json.load(file)
        try:
            if cfSUBSYS is not None:
                cc = config_subsys(cc)
                with open('config.json', 'w') as file:
                    file.write(json.dumps(cc, sort_keys=True, indent=4))
            return Config(cc['allow_cmdln'], cc['multi_in'], cc['output'])
        except KeyError:
            print("Error [I.C1]: Invalid config file, you can retry and specify a different JSON file.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    config_fileloc = input("cA_filepath: ")
                    if cfSUBSYS is not None:
                        return config_handler(config_fileloc, True)
                    return config_handler(config_fileloc)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    elif Path(fileloc).exists() and fileloc != '' and fileloc[-5:] == ".json":
        with open(fileloc) as file:
            cc = json.load(file)
        try:
            if cfSUBSYS is not None:
                cc = config_subsys(cc)
                with open('config.json', 'w') as file:
                    file.write(json.dumps(cc, sort_keys=True, indent=4))
            return Config(cc['allow_cmdln'], cc['multi_in'], cc['output'])
        except KeyError:
            print("Error [I.C2]: Invalid config file, you can retry and specify a different file location.")
            try:
                if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                    config_fileloc = input("cA_filepath: ")
                    if cfSUBSYS is not None:
                        return config_handler(config_fileloc, True)
                    return config_handler(config_fileloc)
                else:
                    os._exit(0)
            except IndexError:
                os._exit(0)
    else:
        with open('config.json', 'w') as file:
            file.write(cc)
        cc = json.loads(cc)
        if cfSUBSYS is not None:
            cc = config_subsys(cc)
            with open('config.json', 'w') as file:
                file.write(json.dumps(cc, sort_keys=True, indent=4))
        return Config(bool(cc['allow_cmdln']), bool(cc['multi_in']), cc['output'])


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
        print("WARNING: If you use a non-Apocrypha text file, it may not be as secure.")
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
        message = input("Message: ")
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
        for ch in message:
            try:
                if ch not in [".", "$", "^"]:
                    if ch in strfile:
                        chars = [m.start() for m in re.finditer(ch, strfile)]
                        charused = random.choice(chars)
                        basecharused = charused
                    elif ch not in strfile:
                        try:
                            basecharused = random.choice(range(len(strfile)))*-1  # Get position of random ch * -1
                            messagefinal.append(basecharused)  # Append
                            charused = ord(strfile[-1*basecharused])*ord(ch)  # Multiply ord together for 2nd append
                        except:
                            print("Error [II.E2]: Couldn't encrypt message."
                                  "Exception thrown encrypting character not found in key.")
                            try:
                                if input("Retry with a new key (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                    Aencode2(config, None)
                                else:
                                    os._exit(0)
                            except IndexError:
                                os._exit(0)
                else:
                    if ch == "." and ch in strfile:
                        charused = random.choice([m.start() for m in re.finditer("\.", strfile)])
                        basecharused = charused
                    else:
                        try:
                            basecharused = random.choice(range(len(strfile))) * -1
                            messagefinal.append(basecharused)
                            charused = ord(strfile[-1 * basecharused]) * ord(ch)
                        except:
                            print("Error [II.E4]: Couldn't encrypt message."
                                  "Couldn't encrypt '$' or '^' character.")
                            try:
                                if input("Retry with a new key (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                                    Aencode2(config, None)
                                else:
                                    os._exit(0)
                            except IndexError:
                                os._exit(0)
            except:
                try:
                    basecharused = random.choice(range(len(strfile))) * -1
                    messagefinal.append(basecharused)
                    charused = ord(strfile[-1 * basecharused]) * ord(ch)
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
            strfile = strfile[:abs(basecharused)] + strfile[abs(basecharused) + 1:]
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
                try:
                    print("Error [III.F2]: NoneType passed for fileloc.")
                    if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                        Adecode2(config, input("dA_key = ") + ".msg")
                    else:
                        os._exit(0)
                except IndexError:
                    os._exit(0)
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
                            if locationbuild < 0:
                                try:
                                    basech = locationbuild*-1
                                    nxtbld = ''
                                    try:
                                        while encryptedmessage[0] != ' ':
                                            nxtbld = "".join(nxtbld + encryptedmessage[0])
                                            encryptedmessage = encryptedmessage[1:]
                                    except IndexError:
                                        nxt = int(nxtbld)
                                        ch = chr(int(nxt / ord(strfile[basech])))
                                        finalmessage.append(ch)
                                        strfile = strfile[:abs(locationbuild)] + strfile[abs(locationbuild) + 1:]
                                        finalkeyhash = h.sha256(strfile.encode('utf-8')).hexdigest()
                                        finalkeyhash = ''.join(list(filter(lambda che: che not in "'", finalkeyhash)))
                                        locationbuild = ""
                                        finalmessage = "".join(finalmessage)
                                        print("Decrypted Message:\n")
                                        print(finalmessage)
                                        print("\nKey Hash Match: Unknown, missing message hash.")
                                        print("\nCurrent Final Key Hash: " + finalkeyhash)
                                        print("Start Initial Key Hash: " + keyhash)
                                        input("\nPress enter to close the program.")
                                        os._exit(0)
                                    nxt = int(nxtbld)
                                    ch = chr(int(nxt/ord(strfile[basech])))
                                    finalmessage.append(ch)
                                    encryptedmessage = encryptedmessage[1:]
                                except:
                                    print("Error [III.9B]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:abs(locationbuild)] + strfile[abs(locationbuild) + 1:]
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
                            if locationbuild < 0:
                                try:
                                    basech = locationbuild * -1
                                    nxtbld = ''
                                    try:
                                        while encryptedmessage[0] != ' ' and len(encryptedmessage) != 0:
                                            nxtbld = "".join(nxtbld + encryptedmessage[0])
                                            encryptedmessage = encryptedmessage[1:]
                                    except IndexError:
                                        nxt = int(nxtbld)
                                        ch = chr(int(nxt / ord(strfile[basech])))
                                        finalmessage.append(ch)
                                        strfile = strfile[:abs(locationbuild)] + strfile[abs(locationbuild) + 1:]
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
                                    nxt = int(nxtbld)
                                    ch = chr(int(nxt / ord(strfile[basech])))
                                    finalmessage.append(ch)
                                    encryptedmessage = encryptedmessage[1:]
                                except:
                                    print("Error [III.9A]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:abs(locationbuild)] + strfile[abs(locationbuild) + 1:]
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
                            locationbuild = int(locationbuild)
                            if locationbuild < 0:
                                try:
                                    basech = abs(locationbuild)
                                    nxtbld = ''
                                    try:
                                        while encryptedmessage[0] != ' ' and len(encryptedmessage) != 0:
                                            nxtbld = "".join(nxtbld + encryptedmessage[0])
                                            encryptedmessage = encryptedmessage[1:]
                                    except IndexError:
                                        nxt = int(nxtbld)
                                        ch = chr(int(nxt / ord(strfile[basech])))
                                        finalmessage.append(ch)
                                        strfile = strfile[:abs(int(locationbuild))]+strfile[abs(int(locationbuild))+1:]
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
                                    nxt = int(nxtbld)
                                    ch = chr(int(nxt / ord(strfile[basech])))
                                    finalmessage.append(ch)
                                    encryptedmessage = encryptedmessage[1:]
                                except:
                                    print("Error [III.9D]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[int(locationbuild)])
                            strfile = strfile[:abs(int(locationbuild))]+strfile[abs(int(locationbuild))+1:]
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
                            locationbuild = int(locationbuild)
                            if locationbuild < 0:
                                try:
                                    basech = abs(locationbuild)
                                    nxtbld = ''
                                    try:
                                        while encryptedmessage[0] != ' ' and len(encryptedmessage) != 0:
                                            nxtbld = "".join(nxtbld + encryptedmessage[0])
                                            encryptedmessage = encryptedmessage[1:]
                                    except IndexError:
                                        nxt = int(nxtbld)
                                        ch = chr(int(nxt / ord(strfile[basech])))
                                        finalmessage.append(ch)
                                        strfile = strfile[:abs(int(locationbuild))]+strfile[abs(int(locationbuild))+1:]
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
                                    nxt = int(nxtbld)
                                    ch = chr(int(nxt / ord(strfile[basech])))
                                    finalmessage.append(ch)
                                    encryptedmessage = encryptedmessage[1:]
                                except:
                                    print("Error [III.9C]: Could not resolve character not found in key")
                            else:
                                finalmessage.append(strfile[locationbuild])
                            strfile = strfile[:abs(int(locationbuild))]+strfile[abs(int(locationbuild))+1:]
                            locationbuild = ""
                    except:
                        print("Error [III.D2]: Unable to decrypt message. "
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
    print("A_version: 1.1.0")
    EncOrDec = input("A_func<E;D;C>: ").lower()
    try:
        if EncOrDec[0] == 'e':
            config = config_handler()
            k = Aencode1(config)
            Aencode2(config, k)
        elif EncOrDec[0] == 'd':
            config = config_handler()
            Adecode2(config, Adecode1(config))
        elif EncOrDec[0] == 'c':
            print("NOTE: Only a 'config.json' file in the same directory as Apocrypha.py will be accepted currently")
            config_handler("config.json", True)
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
    except IndexError:
        print("Error [I.M2]: Invalid input.")
        try:
            if input("Retry (default: No)? [Y]es/[N]o: ").lower().strip()[0] == "y":
                main()
            else:
                os._exit(0)
        except IndexError:
            os._exit(0)


if __name__ == "__main__":
    main()
