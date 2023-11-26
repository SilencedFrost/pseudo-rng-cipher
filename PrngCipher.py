import random as rng
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
import re


alphabet = list('CÛüÅ¾I,xhJÀ\ÇHùf|ØÆi®×ö+tdSq[íúO¨é·8-7g }y²Ä«æÞ)TèÝLÎ%ë1KäÓBv¥õÚ]lwÙý(ÈzN~½4ıQ¬»sÏêôÉ{Â36°ÕáeMÁÜ<Öjó¯¿ÔokÊUFnR§=ËÌ>.?Ã:Òåº¹¸ãçZuî5E"XD¢!þ$@G`òcÍ¡#µ³ªû£Y*‗r¼Abm±â_ÿßap;©&/¦ìï^´WÑ÷Vàƒøð09ñP¶2Ð' + "'")


# Define shifting process
def process(lettermap, shiftmap):
    for x in range(len(lettermap)):
        solving = lettermap[x]
        if solving in alphabet:
            number = int(alphabet.index(solving))
            number = number + int(shiftmap[x])
            while number < 0:
                number = len(alphabet) + number
            while number >= len(alphabet):
                number = number - len(alphabet)
            lettermap[x] = alphabet[number]


# Define shiftmap generation process
def shiftgen(leng):
    sft = str(rng.randint(leng / 10, leng - 1))
    rng.seed(sft[:8])
    sft = re.findall("..", sft + str(rng.randint(leng / 10, leng - 1)))
    return sft


# Define GUI
class Grid(FloatLayout):
    code = ObjectProperty(None)

    # Define encode module
    def translate(self):
        global seed
        # User input for 'text'
        text = list(self.code.text)
        if 308 > len(text) > 7 and text[-1] != '¤':
            # Calculate and set 'seed' for prng
            seed = rng.randint(pow(10, 7), pow(10, 8) - 1)
            rng.seed(seed)
            # Shifting process
            process(text, shiftgen(pow(10, len(text))))
            # Encode seed
            seed = re.findall("..", str(seed))
            for x in range(4):
                seed[x] = alphabet[int(seed[x])]
            # Insert 'seed' into 'text' value
            for x in range(4):
                text.insert(x * 2, seed[x])
            # Output to GUI, adding '¤' mark
            self.code.text = ''.join(text) + '¤'
            # Else if text is between 12 and 6 char and not marked '¤'
        elif 8 > len(text) > 0 and text[-1] != '¤':
            # Calculate and set 'seed' for prng
            seed = rng.randint(pow(10, 3), pow(10, 4) - 1)
            rng.seed(seed)
            # Calculate character length
            length = pow(pow(10, len(text)), 2)
            # Shifting process
            process(text, re.findall("..", str(rng.randint(length, length * 10 - 1))))
            # Encode seed
            seed = re.findall("..", str(seed))
            for x in range(2):
                seed[x] = alphabet[int(seed[x])]
            # Output to GUI adding '¤' mark
            self.code.text = ''.join(seed) + ''.join(text) + '¤'
        # If text is atleast 12 chars and marked '¤'
        elif len(text) > 12 and text[-1] == '¤':
            # Delete '¤' mark
            text.pop(-1)
            # Get raw seed and convert to numeric seed
            seed = text[:7]
            seed = seed[::2]
            for x in range(4):
                seed[x] = str(alphabet.index(seed[x]))
                text.pop(x)
                if len(seed[x]) < 2:
                    seed[x] = '0' + seed[x]
            seed = int(''.join(seed))
            rng.seed(seed)
            # Generate shiftmap and revert shift
            shift = shiftgen(pow(10, len(text)))
            for x in range(len(text)):
                shift[x] = int(shift[x]) * -1
            # Shifting process
            process(text, shift)
            # Output to GUI
            self.code.text = ''.join(text)
        # Else if text is between 12 and 6 char and marked '¤'
        elif 11 > len(text) > 3 and text[-1] == '¤':
            # Delete '¤' mark
            text.pop(-1)
            # Get raw seed and convert to numeric seed
            seed = text[:2]
            for x in range(2):
                seed[x] = str(alphabet.index(seed[x]))
                text.pop(0)
                if len(seed[x]) < 2:
                    seed[x] = '0' + seed[x]
            seed = int(''.join(seed))
            rng.seed(seed)
            # Generate shiftmap
            length = pow(pow(10, len(text)), 2)
            shift = re.findall("..", str(rng.randint(length, length * 10 - 1)))
            for x in range(len(text)):
                shift[x] = int(shift[x]) * -1
            # Shifting process
            process(text, shift)
            # Output to GUI
            self.code.text = ''.join(text)


class CipherApp(App):
    def build(self):
        return Grid()


if __name__ == '__main__':
    CipherApp().run()
