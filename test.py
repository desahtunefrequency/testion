import random
import colorama

colorama.init()

colors = [colorama.Fore.RED, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.BLUE, colorama.Fore.MAGENTA, colorama.Fore.CYAN, colorama.Fore.WHITE]

print(random.choice(colors) + "Hello, world!" + colorama.Style.RESET_ALL)
