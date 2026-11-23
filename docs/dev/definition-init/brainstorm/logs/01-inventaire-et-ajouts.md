# Source de l’inventaire et saisie des ajouts

- **Ouvert le** 2026-11-19
- **Dernière mise à jour** 2026-11-19
- **État** résolu
- **Travail concerné** [Inventaire d’ingrédients de potions](../brainstorm.md)

## Point de départ

L’expression « mon inventaire » pouvait désigner les données d’un joueur dans Minecraft ou un inventaire suivi à part. Le dossier fourni contient des packs d’exemples. Les recettes de brassage ont des champs `reagent`, notamment `minecraft:ghast_tear`.

## Évolution de la réflexion

- La personne a précisé que l’inventaire est un fichier JSON local. Elle a choisi un objet par ingrédient avec le champ `nombre`.
- Deux modes de saisie ont été discutés. La saisie guidée demande des réponses dans le terminal. Les arguments regroupent plusieurs paires sur une ligne. La personne a retenu les arguments et donné en exemple `potions -a blaze_powder 3 ghast_tear 6`. L’exemple affiché quand `potions -a` est lancé seul a été retenu dans la reformulation.
- La première formulation proposait de rejeter tout le lot en cas d’erreur. La personne a précisé que seules les paires invalides doivent être rejetées. Les ingrédients valides accompagnés d’une quantité entière strictement positive sont ajoutés à l’inventaire. L’avertissement, le message prévu pour un nom inconnu et l’affichage de l’aide s’appliquent aux commandes qui contiennent une erreur.

## Questions transmises

La spécification déterminera le chemin du fichier, le comportement à la première utilisation, les variantes de noms acceptées et la présentation de la sortie.
