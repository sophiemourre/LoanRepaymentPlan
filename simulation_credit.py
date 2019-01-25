import numpy as np


class Credit():
    
    def __init__(self, apport_inclus, travaux_inclus, cent_dix_pourcent, prix_appartement=154000, apport=20000, travaux=20000):
        self.prix_appartement = prix_appartement
        self.apport = apport
        self.travaux = travaux 

        total = self.prix_appartement

        if apport_inclus:
            total -= apport
        if travaux_inclus:
            total += travaux
        if cent_dix_pourcent:
            total += 13200 # Need exact amount - frais de notaire 

        self.capital_restant = total

        self._cout_total_assurance = 0
        self._cout_total_credit = 0
        self.echeance_mensuelle = 0

    def assurance_mensuelle(self, info_assurance = 0, assurance_degressive = False):
        """
            @in info_assurance: si l'assurance est degressive, l'info assurance est necessairement un pourcentage. Sinon, une mensualite.
        """
        if assurance_degressive:
            total_assurance = annual2mensual_rate(info_assurance) * self.capital_restant
        else:
            total_assurance = info_assurance

        return total_assurance

    def annual2mensual_rate(self, annual_rate):
        return annual_rate / 12

    def calcul_echeance_mensuelle(self, montant_initial, taux_annuel, duree_credit):
        """
            @in taux_annuel: bien fournir le taux d'interet ANNUEL
            @in duree_credit: la duree du credit en annees
        """
        taux_mensuel = annual2mensual_rate(taux_annuel)
        self.echeance_mensuelle = montant_initial * taux_mensuel / (1. - (1. + taux_mensuel)**(-duree_credit * 12))

    def decoupage_echeance_hors_assurance(self, taux_annuel, duree_credit):
        """
            @in taux_annuel: bien fournir le taux d'interet ANNUEL
            @in frequence_echeances: si jamais l'echeance est annuelle, alors frequence_echeances vaudra 12
            @in duree_credit: la duree du credit en annees
        """
        interay_mensuel = self.capital_restant * annual2mensual_rate(taux_annuel)
    
        if self.capital_restant >= self.echeance_mensuelle:
            mensualitay = self.echeance_mensuelle
        else:
            mensualitay = self.capital_restant + interay_mensuel
        amortissement = mensualitay - interay_mensuel
        self.capital_restant -= amortissement
        self._cout_total_credit += interay_mensuel

        return mensualitay, amortissement, interay_mensuel


    def calcul_multiples_echeances(self, taux_annuel, frequence_echeances, info_assurance, assurance_degressive, duree_credit):
        assurance = 0
        montant = 0
        amortissement = 0
        interets = 0

        for i in range(0, frequence_echeances):
            assurance += assurance_mensuelle(self.capital_restant, info_assurance, assurance_degressive)
            mensualitay_temp, amortissement_mensuel, interay_mensuel = decoupage_echeance_hors_assurance(taux_annuel, duree_credit)
            montant += mensualitay_temp
            amortissement += amortissement_mensuel
            interets += interay_mensuel

        self._cout_total_assurance += assurance


        return montant, amortissement, interets, assurance
    
    @property
    def cout_total_assurance(self):
        return self._cout_total_assurance

    @cout_total_assurance.setter
    def cout_total_assurance(self, cout_assurance):
        self._cout_total_assurance = cout_assurance

    @cout_total_assurance.getter
    def cout_total_assurance(self):
        return self._cout_total_assurance
    
    @property
    def cout_total_credit(self):
        return self._cout_total_credit

    @cout_total_credit.setter
    def cout_total_credit(self, cout_credit):
        self._cout_total_credit = cout_credit

    @cout_total_credit.getter
    def cout_total_credit(self):
        return self._cout_total_credit
    

def pretty_print(i, capital_restant, montant, amortissement, interets, assurance):
    if i == 1:
        print("ECHEANCE\t | CAPITAL_RESTANT_DU \t | MONTANT    \t | AMORTISSEMENT \t | INTERETS \t "\
              "| ASSURANCE \t | MONTANT_AVEC_ASSURANCE")
 
    print(f"{i:8d}\t |  {capital_restant:18.2f} \t | {montant:10.2f} \t | {amortissement:13.2f} \t "\
          f"| {interets:8.2f} \t | {assurance:9.2f} \t | {(montant + assurance):25.2f}")

    

class Simulation:
    taux_annuel_range = [0.012, 0.019]
    credit = None 
    loan_structure = {}

    def moulinette(self, apport_inclus, travaux_inclus, cent_dix_pourcent):
        taux_testes = np.arange(start=self.taux_annuel_range[0], stop=self.taux_annuel_range[1], step=0.0005)

        for taux_annuel in taux_testes:
            self.calcul_credit(self, taux_annuel, duree_credit, frequence_echeances, info_assurance, assurance_degressive, duree_credit):

    def init_credit(fonction):
        def initialisation(taux_annuel):
            duree_credit = 25
            assurance = 50*2
            frequence_echeances = 1
            assurance_degressive = True
            info_assurance = 0.0035
            tableau_amortissement = False 
            i = 0
            
            if frequence_echeances == 0:
                raise ZeroDivisionError("Attention, il faut au moins une échéance sur la durée du crédit.")
            if frequence_echeances > 12:
                raise NotImplementedError("NOT IMPLEMENTED")
            if frequence_echeances < 0:
                raise ValueError("Bien tenté mais non")
        

            fonction(taux_annuel, duree_credit, frequence_echeances, info_assurance, assurance_degressive, duree_credit)
           
            return initialisation 

    @init_credit
    def calcul_credit(self, taux_annuel, duree_credit, frequence_echeances, info_assurance, assurance_degressive, duree_credit):
        calcul_echeance_mensuelle(montant_credit(), taux_annuel, duree_credit)
        print(f"Taux d'intérêt testé : {taux_annuel*100:.2f}%")
        
        for i in range(1, duree_credit * int(12/frequence_echeances) +1):
            montant, amortissement, interets, assurance  = calcul_multiples_echeances(taux_annuel, frequence_echeances, info_assurance, assurance_degressive, duree_credit)
        
            if tableau_amortissement:
                pretty_print(i, self.credit.capital_restant, montant, amortissement, interets, assurance)
        
        print(f"Cout total de l'assurance : {self.credit.cout_total_assurance:.2f}, cout total du credit : {self._cout_total_credit:.2f}, montant de l'echeance : {self.credit.echeance_mensuelle:.2f}\n")

    def test_1(self):
        print(" ========================= Test 1 : sans travaux, ni apport, ni 110%") 
        self.moulinette(apport_inclus = False, travaux_inclus=False, cent_dix_pourcent = False)
    
    def test_2(self):
        print("========================= Test 2 : avec travaux, sans apport, avec 110%") 
        self.moulinette(apport_inclus = False, travaux_inclus=True, cent_dix_pourcent = True)
        self.moulinette()
    
    def test_3(self):
        print("========================= Test 3 : avec travaux, avec apport, avec 110%") 
        self.moulinette(apport_inclus = True, travaux_inclus=True, cent_dix_pourcent = False)
        self.moulinette()

if __name__ == "__main__":



    simulation = Simulation()
    simulation.test_1()
    simulation.test_2()
    simulation.test_3() 
