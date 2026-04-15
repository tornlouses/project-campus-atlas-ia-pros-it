import plotly.express as px
import pandas as pd

données = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv')
#print("Colonnes disponibles :", données.columns.tolist())

figure = px.pie(données, values='qte', names='region', title='quantité vendue par région')
figure.write_html('ventes-par-region.html')
print('ventes-par-région.html généré avec succès !')

# Etape 8.a : Génération du graph ventes par produit
figure = px.pie(données, values='qte', names='produit', color_discrete_sequence=px.colors.qualitative.Pastel, title='quantité vendue par produit')
figure.update_traces(textposition='inside', textinfo='value+percent+label')
figure.write_html('ventes-par-produit.html')
print('Etape 8.a : ventes-par-produit.html généré avec succès !')

# Etape 8.b : Génération du graph chiffre d'affaires par produit
données["chiffre_affaires"] = données["prix"] * données["qte"]
figure = px.pie(données, values='chiffre_affaires', names='produit', color_discrete_sequence=px.colors.qualitative.Pastel, title='chiffre d\'affaires par produit')
figure.update_traces(textposition='inside', textinfo='value+percent+label')
figure.write_html('chiffre-affaires-par-produit.html')
print('Etape 8.b : chiffre-affaires-par-produit.html généré avec succès !')


# Etape 6.a : moyenne du chiffre d’affaires par produit
moyenne_ca_produit = données.groupby("produit")["chiffre_affaires"].mean()
#print(moyenne_ca_produit)

# Etape 6.a : moyenne du volume des ventes par produit
moyenne_vente_produit = données.groupby("produit")["qte"].mean()

# Etape 6.a : médiane du chiffre d’affaires par produit
mediane_ca_produit = données.groupby("produit")["chiffre_affaires"].median()
#print(mediane_ca_produit)

# Etape 6.a : médiane du volume des ventes par produit
mediane_vente_produit = données.groupby("produit")["qte"].median()

# Etape 6.a : Affichage propre
resultat_6_a = pd.DataFrame({
    "moyenne_ca_produit": moyenne_ca_produit,
    "moyenne_vente_produit": moyenne_vente_produit,
    "mediane_ca_produit": mediane_ca_produit,
    "mediane_vente_produit": mediane_vente_produit
})
print("Etape 6.a : ", resultat_6_a)

#Etape 6.b : écart type du volume des ventes par produit
ecart_type_ventes_produit = données.groupby("produit")["qte"].std()

# Etape 6.b : variance du volume des ventes par produit
variance_ventes_produit = données.groupby("produit")["qte"].var()

# Etape 6.b : Affichage propre
resultat_6_b = pd.DataFrame({
    "moyenne_vente_produit": moyenne_vente_produit,
    "mediane_vente_produit": mediane_vente_produit,
    "ecart_type_ventes_produit" : ecart_type_ventes_produit,
    "variance_ventes_produit" : variance_ventes_produit
})
print("Etape 6.b : ", resultat_6_b)


# Etape 7 : sans pandas
import urllib.request
import csv

# Récupération des données sur le drive avec urllib
reponse = urllib.request.urlopen("https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4KusfFzvOsr8WJRgozzsCxrELW4G4PopUkiDbvrrV2lg0S19-zeryp02MC9WYSVBuzGCUtn8ucZW/pub?output=csv")
lignes = []
for ligne in reponse.readlines():
    lignes.append(ligne.decode('utf-8'))

# Parser le CSV avec le module csv
données_csv = csv.DictReader(lignes)

quantite_par_produit = {}
for row in données_csv:
    if row['produit'] in quantite_par_produit :
        quantite_par_produit[row['produit']]['quantite'] += int(row['qte'])
    else:
        quantite_par_produit[row['produit']] = {'quantite':int(row['qte'])}

max = {}
min = {}
i = 0
for cle, valeur  in quantite_par_produit.items():
    if len(max) == 0:
        max = {'produit':cle,'quantite':valeur['quantite']}
    elif valeur['quantite'] > max['quantite']:
        max = {'produit':cle,'quantite':valeur['quantite']}
    if len(min) == 0:
        min = {'produit':cle,'quantite':valeur['quantite']}
    elif valeur['quantite'] < min['quantite']:
        min = {'produit':cle,'quantite':valeur['quantite']}

print("Etape 7 : Le produit le plus vendu est le produit "+max['produit']+" ("+str(max['quantite'])+"), tandis que le moins vendu est le produit "+min['produit']+" ("+str(min['quantite'])+")")
