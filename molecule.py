from ensembles import MonatomicCanonicalEnsemble

class Gas:
    def __init__(self, type: str, input_data: dict):
        self.variables_dict = {
            'N': input_data['N'],
            'V': input_data['V'],
            'T': input_data['T'],
            'm': input_data['u']/input_data['N']
        }
        self.units_dict = {
            'P': 'atm',
            'P_bar': 'bar',
            'E': 'kJ/mol',
            'H': 'kJ/mol',
            'S': 'J/mol.K',
            'G': 'kJ/mol',
            'A': 'kJ/mol',
            'Cv': 'J/mol.K',
            'Cp': 'J/mol.K'
        }
    
class MonatomicGas(Gas):
    def __init__(self, type: str, input_data: dict, ensemble: str):
        super().__init__(type, input_data)
        self.ensemble = MonatomicCanonicalEnsemble(variables=self.variables_dict, partition=ensemble)
        self.properties = self.ensemble.get_properties()

    def print_properties(self):
        print(f"Properties of Monatomic Ideal Gas with properties \n \
                u = {self.variables_dict['m']*1000*6.022e23: .4} g/mol \n \
                V = {self.variables_dict['V']*1000: .4} L \n \
                T = {self.variables_dict['T']: .4} K \n \
                ______________________ \
                ")
        
        keys = ['P', 'P_bar', 'E', 'H', 'S', 'G', 'A', 'Cv', 'Cp']
        for key in keys:
            print(f"{key} = {self.properties[key]: .4} {self.units_dict[key]}")
        return "____________________________"