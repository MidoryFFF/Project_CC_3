from msilib.schema import Error
import sys

# – Путь к исходному файлу с текстом программы.
# – Путь к двоичному файлу-результату.
# – Режим тестирования.

argsSet = {"P": "-", "F": "-", "M": "-"}

acamulator = 0
RAMmemory = [0] * 64

def CommandStringPars():
    args = sys.argv
    for key in argsSet:
        if "-" + key in args:
            try:
                argsSet[key] = args.pop(args.index("-" + key) + 1)
            except:
                print("Error: not all args filled")