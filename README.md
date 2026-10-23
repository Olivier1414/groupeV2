# Atelier de documents

Application Python de bureau pour créer des attestations, convocations, reçus et bulletins en PDF ou Word.

## Installer
Depuis ce dossier, ouvrez un terminal puis exécutez :
```bat
python -m pip install -r requirements.txt
python app.py
```

## Utiliser
- **Créer un document** : sélectionnez une catégorie, remplissez les champs, choisissez PDF et/ou Word, puis cliquez sur Créer.
- **Importer une liste** : sélectionnez un CSV ou Excel (`.xlsx`) et générez un document pour chaque ligne.
- **Éditer les textes** : sélectionnez un modèle, modifiez le texte et enregistrez-le.
- **Journal** : consultez les fichiers produits dans le dossier `output`.

## Format du fichier Excel/CSV
En-têtes conseillés : `type, civilite, nom, prenom, date, motif, montant, note, email`.
La colonne `type` est facultative si vous choisissez un type de document par défaut.

Un jeu de données CSV est fourni dans `data/exemple.csv`. Pour créer aussi un fichier Excel, exécutez :
```bat
python creer_exemple.py
```

## Vérification
```bat
python test_generation.py
```
Utilisez des données fictives pour les essais. Les documents sont des modèles de démonstration et doivent être vérifiés avant usage officiel.
"# groupeV2" 
