// Helper Functions
let doReveal = true;

const generate_random_number = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

const shuffle_string = (text1, text2) => {
  const shuffled = [];
  let i = 0;
  let j = 0;
  const len1 = text1.length;
  const len2 = text2.length;
  const upper_bound = Math.ceil(len2 / len1);

  while (i < text1.length && j < text2.length) {
    let num_characters = generate_random_number(0, upper_bound);
    shuffled.push(text1[i]);
    shuffled.push(text2.slice(j, j + num_characters));
    i++;
    j += num_characters;
  }

  while (i < len1) {
    shuffled.push(text1[i]);
    i++;
  }

  while (j < len2) {
    shuffled.push(text2[j]);
    j++;
  }

  return shuffled.join('');
}

const process_multibytes = (multibyte) => {
  let foo = multibyte.replaceAll('%', '');
  return parseInt(foo, 16).toString(2).padStart(8, '0');
}

// Main Function [Conceal]
const conceal = (cover_message, secret_message) => {
  const codepoints = [];
  for (const s of secret_message) {
    let encoded = encodeURI(s);
    if (encoded.match(/^%+/)) {
      encoded = process_multibytes(encoded);
    } else {
      encoded = encoded.charCodeAt(0).toString(2).padStart(8, '0');
    }
    codepoints.push(encoded);
  }
  const binary_string = codepoints.join('');
  const zwc_string = binary_string.replaceAll('0', '\u200b').replaceAll('1', '\u200c');
  return shuffle_string(cover_message, zwc_string);
}

const reveal = (stego_message) => {
  let decoder = new TextDecoder();
  const zwc_string = stego_message.replaceAll(/[^\u200b-\u200c]/g, '');
  const binary_string = zwc_string.replaceAll('\u200b', '0').replaceAll('\u200c', '1');
  
  const block8_binaries = binary_string.match(/.{8}/g);
  
  const block8_integers = block8_binaries.map(block8 => parseInt(block8, 2));
  const revealed_message = decoder.decode(new Uint8Array(block8_integers));
  return revealed_message;
}

const coverMessage = document.getElementById("cover-message");
const secretMessage = document.getElementById("secret-message");
const coverButton = document.getElementById("cover-button");

const hiddenMessage = document.getElementById("hidden-message");
const uncoverButton = document.getElementById("uncover-button");
const revealedMessage = document.getElementById("revealed-message");

const btsTextArea = document.getElementById("bts");
const revealButton = document.getElementById("reveal-button");
const copyButton = document.getElementById("copy-button");

const clearButton = document.getElementById("clear-button");

coverButton.addEventListener('click', () => {
  const cover = coverMessage.value === undefined ? "" : coverMessage.value;
  const secret = secretMessage.value === undefined ? "" : secretMessage.value;
  const stegoMessage = conceal(cover, secret);
  btsTextArea.value = stegoMessage;
});

uncoverButton.addEventListener('click', () => {
  const hidden = hiddenMessage.value === undefined ? "" : hiddenMessage.value;
  revealedMessage.value = reveal(hidden);
});

const doCopying = () => {
  btsTextArea.select();
  btsTextArea.setSelectionRange(0, 99999);
  navigator.clipboard.writeText(btsTextArea.value);

  const tooltip = document.getElementById('copyToolTip');
  tooltip.innerHTML = "Copied: " + btsTextArea.value;
}

clearButton.addEventListener('click', () => {
  coverMessage.value = '';
  secretMessage.value = '';
  hiddenMessage.value = '';
  revealedMessage.value = '';
  btsTextArea.value = '';
});

revealButton.addEventListener('click', () => {
  if (doReveal) {
    btsTextArea.value = btsTextArea.value.replaceAll('\u200b', '<200b>').replaceAll('\u200c', '<200c>');
  } else {
    btsTextArea.value = btsTextArea.value.replaceAll('<200b>', '\u200b').replaceAll('<200c>', '\u200c');
  }
  doReveal = !doReveal;
});
