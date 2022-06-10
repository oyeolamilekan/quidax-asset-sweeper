from decouple import config

from quidaxapi.quidax import Quidax

quidax = Quidax(config("CRYPTO_PROVIDER"))
