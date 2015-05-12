import axolotl_curve25519 as _curve
import os

from .eckeypair import ECKeyPair
from axolotl.invalidkeyexception import InvalidKeyException

class Curve:

    DJB_TYPE = 5
    # always DJB curve25519 keys

    @staticmethod
    def generatePrivateKey():
        rand = os.urandom(32)
        return _curve.generatePrivateKey(rand)

    @staticmethod
    def generatePublicKey(privateKey):
        return _curve.generatePublicKey(privateKey)

    @staticmethod
    def generateKeyPair():
        from axolotl.ecc import djbec
        privateKey = Curve.generatePrivateKey()
        publicKey = Curve.generatePublicKey(privateKey)
        return ECKeyPair(djbec.DjbECPublicKey(publicKey), djbec.DjbECPrivateKey(privateKey))

    @staticmethod
    def decodePoint(_bytes, offset=0):
        from axolotl.ecc import djbec
        type = _bytes[0] # byte appears to be automatically converted to an integer??

        if type == Curve.DJB_TYPE:
            type = _bytes[offset] & 0xFF
            if type != Curve.DJB_TYPE:
                raise InvalidKeyException("Unknown key type: %s " % type )
            keyBytes = _bytes[offset+1:][:32]
            return djbec.DjbECPublicKey(bytes(keyBytes))
        else:
            raise InvalidKeyException("Unknown key type: %s" % type )

    @staticmethod
    def decodePrivatePoint(_bytes):
        from axolotl.ecc import djbec
        return djbec.DjbECPrivateKey(bytes(_bytes))


    @staticmethod
    def calculateAgreement(publicKey, privateKey):
        """
        :type publicKey: ECPublicKey
        :type privateKey: ECPrivateKey
        """

        if publicKey.getType() != privateKey.getType():
            raise InvalidKeyException("Public and private keys must be of the same type!")

        if publicKey.getType() == Curve.DJB_TYPE:
            return _curve.calculateAgreement(privateKey.getPrivateKey(), publicKey.getPublicKey())
        else:
            raise InvalidKeyException("Unknown type: %s" % publicKey.getType())

    @staticmethod
    def verifySignature(ecPublicSigningKey, message, signature):
        """
        :type ecPublicSigningKey: ECPublicKey
        :type message: bytearray
        :type signature: bytearray
        """

        if ecPublicSigningKey.getType() ==Curve.DJB_TYPE:
            result = _curve.verifySignature(ecPublicSigningKey.getPublicKey(), message, signature)
            return result == 0
        else:
            raise InvalidKeyException("Unknown type: %s" % ecPublicSigningKey.getType())

    @staticmethod
    def calculateSignature(privateSigningKey ,message):
        """
        :type privateSigningKey: ECPrivateKey
        :type  message: bytearray
        """
        if privateSigningKey.getType() == Curve.DJB_TYPE:
            rand = os.urandom(64)
            res = _curve.calculateSignature(rand, privateSigningKey.getPrivateKey(), message)
            return res
        else:
            raise InvalidKeyException("Unknown type: %s" % privateSigningKey.getType())
