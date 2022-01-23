# Error Codes

### Up to date with
![version](https://img.shields.io/badge/Admin_Version-1.9.1-blue.svg)
![stableversion](https://img.shields.io/badge/Stable_Version-1.0.1-brightgreen.svg)

Error codes are up-to-date with the latest Admin Distribution, errors found in the Stable Distribution are consistent
but may not include all errors listed, as some errors are caused by features not currently in the Stable Distribution.

---

# I.##: Main

### I.M1
>"Error [I.M1]: Invalid input."

Originates in the `main` function when the first character of whatever entered is not included in the following list:
`e`, `d`, `c`.

A likely cause for a seemingly correct input throwing this error could be an accidental space being the first character
for the input. It's recommended to just hit backspace and restart you're input if you think you may have accidentally
done something like this.

### I.M2
>"Error [I.M2]: Invalid input."

Originates in the `main` function when the first character of whatever entered is not included in the following list:
`e`, `d`, `c`.

[I.M2] specifically indicates that the user simply just hit enter, having entered nothing as an input except that.

### I.C1
>"Error [I.C1]: Invalid config file, you can retry and specify a different JSON file."

Originates in the `config_handler` function when the loaded JSON file is missing a necessary key to be accepted as a
valid config file for the program. I.C1 signifies a default filepath for the config file.

It's highly recommended to just use the default config file and edit it as necessary, but default values should suffice
for most widespread usage. You can delete the config file and rerun the program which will automatically generate a new
valid config file in its place. You can regain default settings this way for your config file.

### I.C2
>"Error [I.C2]: Invalid config file, you can retry and specify a different file location."

Originates in the `config_handler` function when the loaded JSON file is missing a necessary key to be accepted as a
valid config file for the program. I.C2 signifies a custom filepath for the config file.

It's highly recommended to just use the default config file and edit it as necessary, but default values should suffice
for most widespread usage. You can delete the config file and rerun the program which will automatically generate a new
valid config file in its place. You can regain default settings this way for your config file.

---

# II.##: Encryption

### II.N1
>"Error [II.N1]: Invalid Input, using python64 generation method"

Originates in the `Aencode1` function when for some reason the custom python generation fails.

This is likely due to a not-nice number being entered after `python` where it is not a power of 2.

### II.L1
>"Error [II.L1]: Link did not have a status code of 200, using python64 generation method"

Originates in the `Aencode1` function when the link generated doesn't return a status code of 200.

This is likely due to internet connectivity issues or for some reason the Library of Babel site is down.
This could also be caused by an incorrect usage of the `customfull` option as the build wasn't done correctly.
You need to enter the whole website link with this option.

### II.L2
>"Error [II.L2]: Link did not have a status code of 200, using python64 generation method"

Originates in the `Aencode1` function when the link generated doesn't return a status code of 200.

This is likely due to internet connectivity issues or for some reason the Library of Babel site is down.
This could also be caused by an incorrect usage of the `customparam` option as the build wasn't done correctly.
You need to enter everything from the link after the `?`, you can include the `?` if you wish, it will still work.
II.L2 signifies a `?` was used in the parameter input.

### II.L3
>"Error [II.L3]: Link did not have a status code of 200, using python64 generation method"

Originates in the `Aencode1` function when the link generated doesn't return a status code of 200.

This is likely due to internet connectivity issues or for some reason the Library of Babel site is down.
This could also be caused by an incorrect usage of the `customparam` option as the build wasn't done correctly.
You need to enter everything from the link after the `?`, you can include the `?` if you wish, it will still work.
II.L3 signifies a `?` was NOT used in the parameter input.

### II.N2
>"Error [II.N2]: Invalid input, generating python64 location"

Originates in the `Aencode1` function when no valid input is given to the `eA_gen.type` prompt.

This is likely caused by a typo, or simply not knowing what correct inputs are accepted. All correct inputs are listed
and separated by semicolons. Curley braces denote anything inside as something up to user discretion such as `{INT}`.

### II.W1
>"Error [II.W1]: unable to open the key link in a web browser, please open manually. Link: {LINK HERE}"

Originates in the `Aencode2` function when the link is unable to be opened by the program for whatever reason.

This is likely caused by errors with the default system browser. Closing any instances of a browser may help.

### II.F1
>"Error [II.F1]: File must be a .txt, .json, or .apoc file\nNOTE: Only .txt is supported currently."

Originates in the `Aencode2` function when the passed file is not an accepted type using the `file` encryption option.

### II.K1
>"Error [II.K1]: Invalid key. Likely blank key entered."

Originates in the `Aencode2` function when the key fails to be hashed and developed as a viable base for encryption.

This is likely due to the key entered being blank or there is a character that cannot be hashed by blake2b.

### II.E1
>"Error [II.E1]: Key file is not large enough to encrypt for your message."

Originates in the `Aencode2` function when the key file is smaller than the message itself.

The absence of this error doesn't guarantee your key as being long enough to encrypt. It is also dependent
on the content of that file. You can't encrypt the message "hello" with a txt file that only includes "check".

### II.E2
>"Error [II.E2]: Couldn't encrypt message. Character not found in key in upper or lower."

Originates in the `Aencode2` function when the program fails to encrypt a character that has a lower- or uppercase
counterpart. Casemod can be used to prevent this. A feature is planned to make this error a lot less common.

This, given casemod is False, denotes that the character attempting to be encrypted was not found in the key.

### II.E3
>"Error [II.E3]: Couldn't encrypt message. Character not found in key."

Originates in the `Aencode2` function when the program fails to encrypt a character that doesn't have a lower- or
uppercase counterpart. A feature is planned to make this error a lot less common.

This denotes that the character attempting to be encrypted was not found in the key.

### II.P1
>"Error [II.P1]: Incorrect filepath."

Originates in the `Aencode2` function when the filepath given doesn't exist.

Make sure to doublecheck your filepath and make sure it is an absolute filepath.

---

# III.##: Decryption

### III.F1
>"Error [III.F1]: File must be a .txt, .apoc, or .json file NOTE: Only .txt files are supported as of now"

Originates in the `Adecode2` function when the passed file is not an accepted file type.
It is impossible a file has been encrypted using another file type without modifying the program.

### III.K1
>"Error [III.K1]: Invalid key. Likely blank key entered."

Originates in the `Adecode2` function when the key fails to be hashed and developed as a viable base for encryption.

This is likely due to the key entered being blank or there is a character that cannot be hashed by blake2b.

### III.F2
>"Error [III.F2]: NoneType passed for fileloc."

Originates in the `Adecode2` function when `None` is given for the variable `fileloc` which dictates the file path of
the decryption key.

### III.D1
>"Error [III.D1]: Unable to decrypt message. Probable Cause: Incorrect/Too Small of a key file."

Originates in the `Adecode2` function when the program fails to decrypt the message due an indexing error.
III.D1 denotes that a final key hash was NOT provided with the encrypted message.

This, as the error message suggests, is likely due to the key being incorrect.

### III.D2
>"Error [III.D2]: Unable to decrypt message. Probable Cause: Incorrect/Too Small of a key file."

Originates in the `Adecode2` function when the program fails to decrypt the message due an indexing error.
III.D2 denotes that a final key hash was provided with the encrypted message.

This, as the error message suggests, is likely due to the key being incorrect.

### III.F2
>"Error [III.F2]: Incorrect file type."

Originates in the `Adecode2` function when the file provided doesn't have a valid ending.
Effectively the first check of III.F1, please refer to that.

### III.U1
>"Error [III.U1]: Unexpected error. Likely NoneType given for file location"

Originates in the `Adecode2` function when an unhandled exception occurs within the function as a whole.

Most likely caused by a NoneType being passed into `Adecode2` for some reason.

### III.W1
>"Error [III.W1]: Failed to open key link, please open manually. Link: {LINK HERE}"

Originates in the `Adecode1` function when the link is unable to be opened by the program for whatever reason.
III.W1 denotes this error occurred within the `linkparam` option, the link had a 200 status code, and a `?` was used.

This is likely caused by errors with the default system browser. Closing any instances of a browser may help.

### III.L1
>"Error [III.L1]: Link did not have a status code of 200."

Originates in the `Adecode1` function when the link generated doesn't return a status code of 200.

This is likely due to internet connectivity issues or for some reason the Library of Babel site is down.
This could also be caused by an incorrect usage of the `linkparam` option as the build wasn't done correctly.
You need to enter everything from the link after the `?`, you can include the `?` if you wish, it will still work.
III.L1 signifies a `?` was used in the parameter input.

### III.W2
>"Error [III.W2]: Failed to open key link, please open manually. Link: {LINK HERE}"

Originates in the `Adecode1` function when the link is unable to be opened by the program for whatever reason.
III.W2 denotes this error occurred within the `linkparam` option, the link had a 200 status code,
and a `?` was NOT used.

This is likely caused by errors with the default system browser. Closing any instances of a browser may help.

### III.L2
>"Error [III.L2]: Link did not have a status code of 200."

Originates in the `Adecode1` function when the link generated doesn't return a status code of 200.

This is likely due to internet connectivity issues or for some reason the Library of Babel site is down.
This could also be caused by an incorrect usage of the `linkparam` option as the build wasn't done correctly.
You need to enter everything from the link after the `?`, you can include the `?` if you wish, it will still work.
III.L2 signifies a `?` was NOT used in the parameter input.

### III.W3
>"Error [III.W3]: Failed to open key link, please open manually. Link: {LINK HERE}"

Originates in the `Adecode1` function when the link is unable to be opened by the program for whatever reason.
III.W2 denotes this error occurred within the `linkfull` option and the link had a 200 status code.

This is likely caused by errors with the default system browser. Closing any instances of a browser may help.

### III.L3
>"Error [III.L3]: Link did not have a status code of 200."

Originates in the `Adecode1` function when the link generated doesn't return a status code of 200.

This is likely due to internet connectivity issues or for some reason the Library of Babel site is down.
This could also be caused by an incorrect usage of the `linkfull` option as the link wasn't copied or pasted correctly.

### III.N1
>"Error [III.N1]: Invalid Option."

Originates in the `Adecode1` function when an invalid input is given for the prompt for the key type.

There are 4 valid input options: `linkfull`, `linkparam`, `file`, or `msg`.

A likely cause for a seemingly correct input throwing this error could be an accidental space being the first character
for the input. It's recommended to just hit backspace and restart you're input if you think you may have accidentally
done something like this.

### III.9A
>"Error [III.9A]: Could not resolve character not found in key"

Originates in the `Adecode2` function when a character encrypted that wasn't found in the key cannot be decrypted.
This signifies that a character failed to decrypt with the current method of characters not found in the key.

[III.9A] indicates that a key hash was NOT found with the encrypted message, and it was NOT the last character to be
decrypted.

### III.9B
>"Error [III.9B]: Could not resolve character not found in key"

Originates in the `Adecode2` function when a character encrypted that wasn't found in the key cannot be decrypted.
This signifies that a character failed to decrypt with the current method of characters not found in the key.

[III.9B] indicates that a key hash was NOT found with the encrypted message, and it was the last character to be decrypted

### III.9C
>"Error [III.9C]: Could not resolve character not found in key"

Originates in the `Adecode2` function when a character encrypted that wasn't found in the key cannot be decrypted.
This signifies that a character failed to decrypt with the current method of characters not found in the key.

[III.9C] indicates that a key hash was found with the encrypted message, and it was NOT the last character to be decrypted

### III.9D
>"Error [III.9D]: Could not resolve character not found in key"

Originates in the `Adecode2` function when a character encrypted that wasn't found in the key cannot be decrypted.
This signifies that a character failed to decrypt with the current method of characters not found in the key.

[III.9D] indicates that a key hash was found with the encrypted message, and it was the last character to be decrypted