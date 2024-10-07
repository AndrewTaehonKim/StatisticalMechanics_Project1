import sympy as sp
from sympy import factorial, log, pi

from math import floor, log10

# define constants
K = 1.38064852e-23 # Boltzmann constant [J/K]
h = 6.62607015e-34 # Planck constant [J.s]

class Ensemble:
    def __init__(self, variables: dict, partition):
        self.variables = variables
        self.partition = partition
        self.properties_list = ['P', 'E', 'H', 'S', 'G', 'A', 'Cv', 'Cp']
        
        
class MonatomicCanonicalEnsemble(Ensemble):
    def __init__(self, variables, partition):
        # define variables N, V, T, m
        super().__init__(variables, partition)
        assert 'N' in self.variables.keys(), "T must be defined for the Canonical Ensemble"
        assert 'V' in self.variables.keys(), "V must be defined for the Canonical Ensemble"
        assert 'T' in self.variables.keys(), "T must be defined for the Canonical Ensemble"
        assert 'm' in self.variables.keys(), "m must be defined for the Canonical Ensemble"
        
        ### define sympy equations
        N = sp.symbols('N')
        V = sp.symbols('V')
        T = sp.symbols('T')
        m = sp.symbols('m')
        
        ### store properties in a dictionary
        self.P = N*K*T/V
        self.E = 1.5*N*K*T
        self.H = 2.5*N*K*T
        self.A = -K*T*(-1*log(factorial(N)) +
                        1.5*N*log(2*pi*m*K/h**2) +
                        1.5*N*log(T) +
                        N*log(V))
        self.S = (self.E-self.A)/T
        self.G = self.H - T*self.S
        # self.S = K*(-1*log(factorial(N)) +
        #             1.5*N*log(2*pi*m*K/h**2) +
        #             1.5*N*log(T) +
        #             N*log(V) -
        #             N)
        # self.A = self.E - T*self.S
        
        self.Cv = 1.5*N*K
        self.Cp = 2.5*N*K
        property_expr_list = [self.P, self.E, self.H, self.S, self.G, self.A, self.Cv, self.Cp]
        self.property_expr_dict = {key: equation for key, equation in zip(self.properties_list, property_expr_list)}
        
    def get_properties(self):
        properties_dict = {}
        for property in self.property_expr_dict.keys():
            properties_dict[property] = self.property_expr_dict[property].subs(self.variables).evalf()
        
        # unit conversion
        # pressure Pa -> atm & bar
        properties_dict['P_bar'] = properties_dict['P'] / 1e5
        properties_dict['P'] /= 101325
        # all energies J/mol -> kJ/mol
        properties_dict['E'] /= 1000
        properties_dict['H'] /= 1000
        properties_dict['G'] /= 1000   
        properties_dict['A'] /= 1000
        
        # rounding
        for key in properties_dict.keys():
            properties_dict[key] = round(properties_dict[key], -int(floor(log10(abs(properties_dict[key])))) + 3)
        return properties_dict