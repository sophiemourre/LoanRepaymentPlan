prix_appartement = 154000
frais_de_notaire = 13200 # TODO:Check amount - find exact one
travaux = 0
cout_total_assurance = 0
duree = 25
echeance_mensuelle_credit = 0
cout_credit_global = 0
capital_restant = 0
taux_annuel_range = [1.2, 1.9]
travaux_inclus = False
apport_inclus = False
cent_dix_pourcent = False

def montant_credit():
    global capital_restant

    total = prix_appartement

    if apport_inclus:
        total += apport
    if travaux_inclus:
        total += travaux
    if cent_dix_pourcent:
        total += frais_de_notaire

    capital_restant = total
    
    return total 

def assurance_mensuelle(capital_restant, info_assurance = 0, assurance_degressive = False):
    """
        @in info_assurance: si l'assurance est degressive, l'info assurance est necessairement un pourcentage. Sinon, une mensualite.
    """
    if assurance_degressive:
        total_assurance = info_assurance * capital_restant
    else:
        total_assurance = info_assurance

    return total_assurance

def annual2mensual_rate(annual_rate):
    return annual_rate / 12

def echeance_mensuelle(montant_initial, taux_annuel, duree_credit):
    """
        @in taux_annuel: bien fournir le taux d'interet ANNUEL
        @in duree_credit: la duree du credit en annees
    """
    taux_mensuel = annual2mensual_rate(taux_annuel)
    echeance_mensuelle_credit = montant_initial * taux_mensuel / (1. - (1. + taux_mensuel)**(-duree_credit * 12))
    
    return echeance_mensuelle_credit

def decoupage_echeance_hors_assurance(capital_restant, taux_annuel, duree_credit):
    """
        @in taux_annuel: bien fournir le taux d'interet ANNUEL
        @in frequence_echeances: si jamais l'echeance est annuelle, alors frequence_echeances vaudra 12
        @in duree_credit: la duree du credit en annees
    """
    global cout_credit_global    

    interay_mensuel = capital_restant * annual2mensual_rate(taux_annuel)
    mensualitay = echeance_mensuelle(capital_restant, taux_annuel, duree_credit)
    amortissement = mensualitay - interay_mensuel
    capital_restant -= amortissement
    cout_credit_global += interay_mensuel

    return capital_restant, mensualitay, amortissement, interay_mensuel


def calcul_multiples_echeances(capital_restant, taux_annuel, frequence_echeances, info_assurance, assurance_degressive, duree_credit):
    assurance = 0
    montant = 0
    amortissement = 0
    interets = 0

    global cout_total_assurance

    for i in range(0, frequence_echeances):
        assurance += assurance_mensuelle(capital_restant, info_assurance, assurance_degressive)
        capital_restant, mensualitay_temp, amortissement_mensuel, interay_mensuel = decoupage_echeance_hors_assurance(capital_restant, taux_annuel, duree_credit)
        montant += mensualitay_temp
        amortissement += amortissement_mensuel
        interets += interay_mensuel

    cout_total_assurance += assurance

    return capital_restant, montant, amortissement, interets, assurance, cout_total_assurance

def pretty_print(i, capital_restant, montant, amortissement, interets, assurance):
    if i == 1:
        print("ECHEANCE\t | CAPITAL_RESTANT_DU \t | MONTANT    \t | AMORTISSEMENT \t | INTERETS \t "\
              "| ASSURANCE \t | MONTANT_AVEC_ASSURANCE")
 
    print(f"{i:8d}\t |  {capital_restant:18.2f} \t | {montant:10.2f} \t | {amortissement:13.2f} \t "\
          f"| {interets:8.2f} \t | {assurance:9.2f} \t | {(montant + assurance):25.2f}")


if __name__ == "__main__":

    assurance = 0
    montant = 0
    amortissement = 0
    interets = 0

    duree_credit = 25
    assurance = 50*2
    taux_annuel = 1.5/100
    frequence_echeances = 12
    assurance_degressive = True 
    echeance_mensuelle_credit = echeance_mensuelle(montant_credit(), taux_annuel, duree_credit)
    info_assurance = 0.36/100
    i = 0 

    while capital_restant > echeance_mensuelle_credit:
        i += 1
        capital_restant, montant, amortissement, interets, assurance, cout_total_assurance = calcul_multiples_echeances(capital_restant, taux_annuel, frequence_echeances, info_assurance, assurance_degressive, duree_credit)
        
        pretty_print(i, capital_restant, montant, amortissement, interets, assurance)
    
    # TODO: Rajouter la derniere echeance quelque part   
 
    print(f"Cout total de l'assurance : {cout_total_assurance:.2f}, cout total du credit : {cout_credit_global:.2f}")
