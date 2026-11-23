# Prompts de l’initiative

Les messages des chats Codex du projet sont reproduits dans l’ordre où ils ont été envoyés.

## Créer le script de gestion des ingrédients

````text
utilise le skill brainstorming: besoin d'un script qui a partir de ce directory "C:\Users\Coren\Documents\cegep\prog3\examens\etc\bedrock-samples-main", doit me retourner la liste d'ingredient dans mon inventaire avec la commande 'potions --show' (raccourci 'potions -s'), me permettre d'ajouter des ingredients dans mon inventaire avec la commande 'potions --add' (raccourci 'potions -a')
````

````text
Par mon inventaire, je veux parler d'un fichier json local qui se contruirait comme ceci&#x20;
```arduino
{
    "<nom-ingredient>": {
        "nombre": <nombre>;
    },
    "<nom-ingredient>": {
        "nombre": <nombre>;
    }
}
```

````

````text
Je préfère la saisie en argument. Quand je lance `potions -a` je voudrais que ca me demande comme ceci, "potions -a blaze_powder 3 ghast_tear 6
````

````text
la commande indique l’erreur et l’inventaire reste tel quel cependant, je veux qu'il y ai un warning si quelque chose ne va pas, par exemple si je me trompe et que je met `ghost_tear` au lieu de `ghast_tear`, le programme doit me dire `l'ingredient que vous avez cherche n'existe pas` et doit afficher un --help (ou -h),  le brainstorming doit se trouver a `./docs/dev/definition-init/brainstorm`
````

````text
l'ajout rejette seulement ce qui ne va pas, si les autres ingredients de la liste sont valides et avec des valeurs strictement supérieurs a 0, alors elles s'ajoutent a la liste
````


## Lancer spec-elaboration

````text
a partir de .\docs\dev\definition-init\brainstorm lance `spec-elaboration`  
````

````text
fait un argument '--add_multiple' avec -am comme raccourci et le --add doit envoyer recevoir seulement 1 ingredient 
````

````text
j'approuve les spec et il doit etre dans ./docs/dev/definition-init/spec
````

````text
modifie la spec avec le enonce-etc.md 
````

````text
fait le beaucoup moins verbeusement
````

````text
oui
````


## Lancer le planning

````text
lance le planning
````

````text
pour les tests utilise pytest et non unittest
````

````text
juste un import pytest devrait suffire
````

## Lancer l’implémentation du plan

````text
lance l'implementation en utilisant le skill executing-plans et en suivant le plan et les specs
````

[Plan d’implantation](../plan.md) · [Spécification approuvée](../../spec/specification.md)
