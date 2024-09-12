# Week 3 - 29.07/02.08

05/08/2024

Bonjour Monsieur Quitin,

Ma troisième semaine de stage est finie et c'était une semaine qui m'a stressé un peu.

En début de semaine, j'ai fini d'implémenter le deserializer dans le uC. En fait, ceci ne consiste qu'en plein des petites fonctions qui vont casser le string envoyer par le PC, le charger dans un struct au sein du uC et après valider les données reçues. Après avoir fini, j'ai établi un response serializer qui transforme le message de retour en un format spécifique qui sera deserialized par le PC. Ainsi, le protocole de communication en série en le PC et le uC est fini et bien robuste, c'est-à-dire que toutes les commandes sont bien reconnues et que l'interprétation du string est bien déterminée. Par contre, j'étais curieux de voir la performance que le deserializer avait dans le uC. Alors, j'ai collecté des données et je les ai analysées afin de déterminer si l'algorithme était rapide et quelle était sa complexité. Les résultats ont montré que le uC pouvait traiter les strings dans le pire des cas en 4 ms, et que la complexité était linéaire en fonction de la taille du string.

Le mercredi, j'ai reçu les composants qui j'avais commandé, la plaque de microcontrôleur et les headers. Alors, ma mission était de tester les plaques en laçant un programme simple avec des LEDs. Par contre, c'est la que ma semaine est devenue stressante. L'installation et la prise en main de l'environnement de développement proposé par Renesas, compagnie qui fabrique les cartes, étaient des vrais défis. D'abord, des problèmes de bibliothèques Java m'ont empêché pendant deux jours d'installer le logiciel. Heureusement, la communauté autour de composants de Renesas est assez active et via des échanges sur leur forum, j'ai pu trouver une solution. Une fois le logiciel installé, il fallait le comprendre pour pouvoir l'utiliser. Malgré leur grande documentation, leur logiciel est très complet avec plein des fonctionnalités et d'outils dont je ne sais pas du tout m'en servir. C'est ainsi que pouvoir lancer un programme qui allume des LEDs en alternance m'a pris presque deux jours entiers. Ces défis m'ont appris trois choses : 1) l'environnement de développement est aussi important que les caractéristiques techniques des composants et ne peut pas être sous-estimé, j'estime que j'aurai pas mal de souci encore à cause de cela ; 2) si tu ne sais pas, pose des questions. Il aura toujours quelqu'un qui pourra venir t'aider et c'est mieux de les poser aussitôt que perdre du temps en essayant par toi même. Peut-être, la solution est à une question près d'être trouvée ; 3) Il faut être résilient et ne pas se sous-estimer. Tout au long de ces quatre jours, je n'ai pas mal douté de mes capacités, j'ai regretté mon choix et j'ai voulu tout lâché. Il m'a fallu beaucoup de courage pour continuer. Le syndrome de l'imposteur est très fort en ces moments et il faut savoir gérer ce stress et persévérer. Ce que m'a aidé à m'en sortir c'était juste d'aller marcher et me déconnecter un peu, cela aère l'esprit et te donne des forces pour continuer.

En fin de semaine, j'ai commencé le refactoring de mon script PC qui communiquera avec le uC. Avec mon maître de stage, nous nous sommes mis d'accord sur la meilleure architecture qui permettrait un PC à se communiquer avec plusieurs uC. Cette nouvelle architecture est plus modulaire avec des classes spécialisées, plus petites avec des responsabilités spécifiques, qui peuvent être testé facilement.

Voilà pour cette semaine.

À la semaine prochaine,

Brenno Ferreira.