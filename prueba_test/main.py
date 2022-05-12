def suma(x, y):
    return x + y


def escribir(fpath, data_in):
    with open(fpath, "w") as file_in:
        file_in.write(data_in)

class calculadora:
    def sumar(x, y):
        return suma(x, y)