# COMP6841-Steganography
Steganography is the practice of concealing a piece of information within a carrier medium. The security of steganography relies on a secret, meaning the carrier should be inconspicuous such that the hidden information remains undetected in the medium it is being transmitted.
In modern times, steganography can be used for lawful purposes such as watermarking and also unlawaful purposes such as hiding malicious scripts, executables and command & control traffic attacks. 

<br>

## Text Steganography
Te‌xt ‌St‌e‍‍ga‍n‌‌o‌graphy‍‍ ‍in‍‍v‍‌o‌l‍ve‍‍s‌ ‍h‌‍i‌d‌in‌‍g‍‍ th‌‌e‌ m‍‍es‍‍sa‍ge‌ ‍wi‌t‍‍hin a ‍‍c‍‍o‌ve‌‌r t‌e‍x‍‍t‌. ‌C‌o‍‍m‍p‍‍ar‍‌e‌d‍‌ ‍to‍‌ ‌o‌‌th‌‌e‍‍r‍‌ ‌fo‌‍r‍‍ms‍ ‍o‍‌f ‌c‍‌ov‍e‌‍r‍s‍ s‌‌u‌‍c‍h‍ ‌‌a‌s‍ a‍‍ud‍io, ‍‍i‌mag‌‍e‍‍ ‍‌a‌‍nd‌‌ ‌vid‍e‍‍o‌‌,‌ ‍‍t‍e‍‍x‍t‍ h‌‍a‍s‍ t‍‍he‌‍ le‍‌a‍‌st ‌red‍u‍‌nd‍a‌‌ncy‍,‌‌ b‌‌u‍t‌ ‌th‌e‍‌r‍‌e‍ ‍‌a‍re st‍i‍l‍l‍‍ ‌‌e‍‍xi‌‌s‍‍ti‌‌n‍g‌ ‌‌te‌ch‍niq‌ue‌‌s th‍‌a‍‌t‍‌ ‌c‍‌a‌n‌‍ b‍‌e‌‍ ‍‌u‍sed‍.‍‍‌‍‍‍‍‍‍‌‌‌‍‌‍‍‍‌‌‍‌‍‍‍‍‌‌‍‍‌‍‌‍‍‌‍‍‍‍‍‍‌‌‌‍‍‌‌‍‌‌‍‍‌‍‌‍‌‌‍‍‍‌‌‍‌‌‌‍‍‌‍‍‌‌‍‍‌‍‌‍‌‌‌‍‌‍‍‍‍‌‍‍‍‍‍‍‌‍‌‌‌‌‍‍‌‍‍‌‌‌‌‍‌‍‌‌‌‌‍ For this, I chose to utilise the zero width characters in Unicode to hide the secret. In Unicode, there are certain codepoints which are non-printable, meaning we can hide them within our cover message, and it will be covert enough to not suspect for an existence of a secret message.
To test it out, check out the GUI I made [here](https://cac1031.github.io/COMP6841-Steganography/), which allows us to hide a secret message within a cover.

P.S. Do you think the paragraph above contains a hidden message :0 (use the GUI to find out!)

<br>

## Image Steganography
The most commonly employed technique for image steganography is LSB substitution. This involves substituting the least significant bit(s) of the pixel values of the cover image with the data we intend to hide. To enhance LSB, we can use Discrete Cosine Transform (DCT), an algorithm used in JPG compression. To briefly explain the steps, the image is broken down into blocks of 8x8 and the DCT algorithm will be applied to each pixel of an image. Through a process of quantization (compression), the secret data can be embedded into the quantised coefficients. Then, we undo the quantisation process and perform the inverse DCT, resulting in an image embedded with our secret information.

To use the dct steganography tool I have made, this repo has to be cloned.
Then, navigate to the `dct-image` directory. The program will run on the command line.

To embed an image, we run the command:
```
./controller.py <path-of-image-we-want-to-use-as-cover> -e <path-of-file-containing-secret>
```
If the paths of both the cover message and secret file is valid, the program will have created a new stego image!

To reveal the data hidden in an image, we run the command:
```
./controller.py <path-of-image-we-want-to-extract-data-from> -r
```
If the image path is valid, the program will produce a .dat file that contains our secret!
Note that if the .dat file is a png/jpg, we can simply rename the file, for example `extracted1.dat` to `extracted1.png` so we can view the secret image!

There are folders containing sample cover images and sample secret files to utilise!

<br>

### Video Runthrough:



