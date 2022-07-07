import enum


class Status(enum.Enum):
    """
    Enumerator that represents the different status values defined on the INE API.
    """
    D = "Definitive"
    P = "Provisional"
    E = "Estimated"
    UNKNOWN = "Unknown"
