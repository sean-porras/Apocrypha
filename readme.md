# Apocrypha
###### 1. from ecclesiastical Latin "Apocrypha (scripta)" meaning "hidden (writings)".
###### 2. the plane of Oblivion belonging to Hermaeus Mora, the Daedric Prince of Fate, Knowledge and Memory

----
----


## Description

![version](https://img.shields.io/badge/Admin_Version-1.9.2-blue.svg)
![stableversion](https://img.shields.io/badge/Stable_Version-1.1.0-brightgreen.svg)
![documentation](https://img.shields.io/badge/documentation-passing-brightgreen.svg)

The Apocrypha cipher takes a message and a key given by the user
and proceeds to encrypt the message with the key by iteratively
changing the key as it encrypts.

>NOTE: For the best reading experience and to correctly view this document as intended,
>please view in an IntelliJ IDE or other Markdown viewer which displays similarly. There
>should be no random `#`s at the beginning of lines as appears on GitHub.

----
----


## Requirements

- Python 3.9+ (Haven't tested versions before 3.9)
- `blake3` Python Library (`pip install blake3`)

----
----

## Documentation

### Class Objects

####`Config`

The `Config` class object is used to create an easy library of attributes.
These dictate the functions of the Apocrypha program.

---
---

>######TO BE IMPLEMENTED: `allow_cmdln`: default `True`. Dictates whether or not command line can be used given all arguments rather than needing to go through the program step by step.

---

>######CURRENTLY UNIMPLEMENTED: `multi_in`: default `False`. Dictates whether or not multiple runs of Apoc will be run on a single file containing commands for each separate result.

---

`output`: default `'print'`. Dictates what form the output of Apoc will be given as. Apoc currently
only supports printing the output. Future support for .txt, .json, and .apoc formats is planned.

----
----

### Functions

####`Aencode1(config: Config) -> str or None`

_Generates and returns a key to be used for encryption in Aencode2._

>Parameter _config:_ Config object which allows for config options to be utilized.
> 
>Returns: str (valid link) or None (indicative of txt, json, or apoc file)

The first step in the Apocrypha encryption process. Works to determine the key that'll be used,
and create one if necessary. Takes user input to create either a link using the secrets module as
the user has specified, the Library of Babel's built-in random function, or given specific parameters
of the key to be used so it can be constructed and fetched. The file option is available which
returns None and proceeds to the second part of encryption via the Aencode2 function. Otherwise the
custom key option is available which returns the key entered by the user with a post-fixed ".msg" signifier
to be identified by the Aencode2 function.

---

####`Aencode2(config: Config, key: str or None) -> None`

_Given a key of either a valid link or a NoneType, processes to encrypt and print the output._

>Parameter `config`: `Config` object which allows for config options to be utilized
> 
>Parameter `key`: `str` is indicative of a valid link, `None` is indicative of a file being used
> 
>Returns: `None`; Works to print out the result of encryption via printing to the console.

The second and final step in the Apocrypha encryption process. Gets the file location of the downloaded
valid file to read and prepare to use as a key for the encryption. If the key format that gets passed
is a link, it'll attempt to open it via the default system web browser, so it can be downloaded. It then
moves on to get the user to input the filepath or the custom key for the program to utilize.

The program then prompts for the message the user wants to encrypt after validating the key.
It then encrypts the message using the Apocrypha method: Find and compile a list of all indexes of characters matching
the current character being encrypted of the message in the key. It then selects a random one of those characters
and deletes it from the key file, which then changes the file to then repeat the process until the message is complete.
It finally gets the hash of the final result of the key after encryption as a unique identifier of that encryption.

This method allows for the same key and the same message to have multiple encrypted versions while all decrypting to the
same original message given the same initial key and message.

NOTE: For characters not found in the key, as of {AD} 1.9.0, it will take a position of an unused character (a character
in the key but not found in the message), and use its position as the base, then invert the ord and multiply by -1 as an
indicator of it being a 'custom' character. This version of 'custom' character encryption will be changed to be more
secure and reliable, as the current iteration doesn't always reliably work, many examples can be found in comments in
{AD} which detail how it was made, what it was supposed to decrypt to, and what it actually decrypted to.

---

####`Adecode1(config: Config) -> str`

_Helper function which starts the decryption process and prompts the user to return the path of a valid file path
(.txt required in Adecode2)._

>Parameter `config`: `Config` object which allows for config options to be utilized.
> 
>Returns: `str`; File path to be processed by Adecode2

The first step in the Apocrypha decryption process. Given the user input of either a full link, link parameters,
a file, or a custom key, gets the user to either open the link, constructs then opens the link, or simply input the
filepath or key respectively. Finally gets the user to enter the location of the file either obtained, or previously
had. Passes the str of the filepath or key to Adecode2 for processing and use for decryption.

---

####`Adecode2(config: Config, fileloc: str) -> None`

_Given a valid file location, prompts for an encrypted message to decrypt and print the results._

>Parameter `config`: `Config` object which allows for config options to be utilized.
> 
>Parameter `fileloc`: valid Path where the file is a .txt file
> 
>Returns: `None`; Final function using the Adecode1 helper function, prints to console.

The second and final step in the Apocrypha decryption process. Takes the filepath or key and validates it or creates it,
respectively, then opens it and prepares it for the decryption process. Proceeds to prompt the user for the input of the
encrypted message. It then formats the input to be able to process each character to find and then delete from the key
in the same way the encryption process created it.

---

####`config_handler(fileloc: str = '') -> Config`
_Looks for an existing config file to read from and set up, otherwise creates a config with default values and returns
the resulting configuration from the file._

>Parameter `fileloc`: `str`; Valid Path of file named "config.json"
> 
>Returns: `Config` object

Function that is used for returning a `Config` object for the Apoc program to use if a "config.json" file exists,
otherwise creates a "config.json" file in the parent directory with the default values as defined above.

---

####`config_subsys(cf: dict) -> dict`
_The subsystem in charge of taking in and modifying a dictionary according to user input. Constantly runs in the
subsystem until the user enters the command to quit/exit._

>Parameter `cf`: `dict`; Dictionary; This dictionary with config options is modified and returned
> 
>Returns: `dict`; Modified cf dictionary post-user processing.

The function that puts the user into a system where they can modify the options of the config file as they please.
Called only by the `config_handler` function via entering `c` into the `A_func` prompt in `main`.

---

####`expanding_hash(invar: str, length: int = 5000) -> str`

_Iteratively increases a given string into a hash containing characters specified below in the return docstring._

>Parameter `invar`: String to be expanded into a hash used for Apocrypha method encryption as the key.
>
>Parameter `length`: NonNegInteger; Defaults to 5000
>
>Returns `k`; Final key, string, contains upper and lowercase letters, numbers, periods, numbers, spaces, and commas.

Expanding hash utilizes several hashing functions within it to create a unique and custom hash with a variable length.
The function first goes over one iteration of the custom hashing function which then passes that hash to itself in a loop
to complete the rest of the expansion of the hash.

It first creates a large number via taking the floored square root of the numbers present in the blake2b hash of the `invar`.
That number is then used to grab the middle 2 numbers to use as the shifted position of the `,` in the final construction
of the next segment of the expanded hash.

It then creates the first iteration of the hash which is the base64 encryption of the blake3 hash with
`+`, `/`, and `=` replaced with `.`, ` `, and `,` respectively. By default, due to how base64 encryption works, the `=`
and thus the `,` is always at the end, which is where the middle two numbers randomly generated are used. It determines
where the `,` is moved in the segments that were generated such that the `,` isn't a signifier for where each iteration
starts and ends.

Finally, it creates a list to pass onto the loop portion of the function which will continue this process until the
length parameter is met for the final key. The list passed onto the loop is the result of the first iteration but sliced
into 4 equal length segments to then by hashed individually to repeat the process and expand the final key.

---

####`main() -> None`

_The main function of the Apocrypha program which carries out the 3 primary functions of Apocrypha:
Encrypt, Decrypt, Config._

>Returns: `None`; Main function of the program which calls other functions to carry out the functionality of Apocrypha.

Prints the current version of the Apocrypha program and prompts the user for input. Valid inputs include: E, D, and C.
Any string with these letters as the first character will be considered a valid input and execute the corresponding function.

----
----