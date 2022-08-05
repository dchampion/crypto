"""
The collection of elliptic curves from the Standards for Efficient Cryptography Group's (SECG)
Recommended Elliptic Curve Domain Parameters (see https://www.secg.org/sec2-v2.pdf for further
details).
"""

class Curve():
    def __init__(self, p, a, b, Gx, Gy, n, h):
        # field parameter p -> prime modulus in the curve equation y^2 = x^3 + ax + b (mod p)
        self.p = p
        # coefficient a in curve equation
        self.a = a
        # coefficient b in curve equation
        self.b = b
        # Base/generator point G x-coordinate
        self.Gx = Gx
        # Base/generator point G y-coordinate
        self.Gy = Gy
        # Order n of base/generator point G -> such that nG = i, where i is the identity element
        self.n = n
        # cofactor h -> where h is the order of the curve (written as #E(Fp)) divided by n
        self.h = h

    def G(self):
        # Base/generator point (G)
        return [self.Gx, self.Gy]

    def __str__(self):
        return f"{type(self).__name__} curve parameters:\n\
 p:  {self.p}\n\
 a:  {self.a}\n\
 b:  {self.b}\n\
 Gx: {self.Gx}\n\
 Gy: {self.Gy}\n\
 n:  {self.n}\n\
 h:  {self.h}"
    
class Secp192k1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.2.1
    def __init__(self):
        super().__init__(
            2**192 - 2**32 - 2**12 - 2**8 - 2**7 - 2**6 - 2**3 - 1, 0, 3,
            5377521262291226325198505011805525673063229037935769709693,
            3805108391982600717572440947423858335415441070543209377693,
            6277101735386680763835789423061264271957123915200845512077,
            1
        )      

class Secp192r1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.2.2
    def __init__(self):
        super().__init__(
            2**192 - 2**64 - 1,
            6277101735386680763835789423207666416083908700390324961276,
            2455155546008943817740293915197451784769108058161191238065,
            602046282375688656758213480587526111916698976636884684818,
            174050332293622031404857552280219410364023488927386650641,
            6277101735386680763835789423176059013767194773182842284081,
            1
        )      

class Secp224k1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.3.1
    def __init__(self):
        super().__init__(
            2**224 - 2**32 - 2**12 - 2**11 - 2**9 - 2**7 - 2**4 - 2 - 1, 0, 5,
            16983810465656793445178183341822322175883642221536626637512293983324,
            13272896753306862154536785447615077600479862871316829862783613755813,
            26959946667150639794667015087019640346510327083120074548994958668279,
            1
        )      

class Secp224r1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.3.2
    def __init__(self):
        super().__init__(
            2**224 - 2**96 + 1,
            26959946667150639794667015087019630673557916260026308143510066298878,
            18958286285566608000408668544493926415504680968679321075787234672564,
            19277929113566293071110308034699488026831934219452440156649784352033,
            19926808758034470970197974370888749184205991990603949537637343198772,
            26959946667150639794667015087019625940457807714424391721682722368061,
            1
        )      

class Secp256k1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.4.1
    def __init__(self):
        super().__init__(
            2**256 - 2**32 - 977, 0, 7,
            55066263022277343669578718895168534326250603453777594175500187360389116729240,
            32670510020758816978083085130507043184471273380659243275938904335757337482424,
            115792089237316195423570985008687907852837564279074904382605163141518161494337,
            1
        )      

class Secp256r1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.4.2
    def __init__(self):
        super().__init__(
            2**224 * (2**32 - 1) + 2**192 + 2**96 - 1,
            115792089210356248762697446949407573530086143415290314195533631308867097853948,
            41058363725152142129326129780047268409114441015993725554835256314039467401291,
            48439561293906451759052585252797914202762949526041747995844080717082404635286,
            36134250956749795798585127919587881956611106672985015071877198253568414405109,
            115792089210356248762697446949407573529996955224135760342422259061068512044369,
            1
        )

class Secp384r1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.5.1
    def __init__(self):
        super().__init__(
            2**384 - 2**128 - 2**96 + 2**32 - 1,
            39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112316,
            27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575,
            26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087,
            8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871,
            39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643,
            1
        )

class Secp521r1(Curve):
    # https://www.secg.org/sec2-v2.pdf#subsubsection.2.6.1
    def __init__(self):
        super().__init__(
            2**521 - 1,
            6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057148,
            1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984,
            2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846,
            3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784,
            6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449,
            1
        )