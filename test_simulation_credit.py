from simulation_credit import Credit

def test_montant_credit():
    Credit.apport_inclus = True
    Credit.travaux_inclus = True
    Credit.cent_dix_pourcent = True
    Credit.prix_apppartement = 154000

    assert (Credit.montant_credit() == Credit.prix_appartement)
