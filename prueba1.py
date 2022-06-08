class Prueba1:

    parametro_1: str = None
    parametro_2: int = None
    parametro_3: float = None

    def metodo_parametros_opcionales(
            parametro_1: str = None,
            parametro_2: int = None,
            parametro_3: float = None
    ):

        if parametro_1 is None:
            if self.parametro_1 is None:
                parametro_1 = PARAMETERO_1_DEFAULT_VALUE
            else:
                parametro_1 = self.parametro_1
        else:
            if self.parametro_1 is None:
                self.parametro_1 = parametro_1
       # Repetir lo de arriba para el resto de parámetros
        if parametro_2 is None:
            parametro_2 = PARAMETERO_2_DEFAULT_VALUE
        if parametro_3 is None:
            parametro_3 = PARAMETERO_3_DEFAULT_VALUE
