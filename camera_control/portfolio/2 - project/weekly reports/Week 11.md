# Week 11 - 23.09/27.09

30/09/2024

Bonjour Monsieur Quitin,

J'espère que vous allez bien.

Voici le rapport de mon avant-dernière semaine.

Vu qu'on approche ma fin bientôt, il ne me reste que peu des tâches à achever avant la fin. Ces tâches sont surtout des implémentations logicielles, remaniement du firmware du microcontrôleur, le montage et test du système dans l'environnement d'utilisation.

J'ai fini l'implémentation du module microcontroller-virtual qui simuler un microcontrôleur et ne sert qu'à des fins de test de recette pour le logiciel. En fait, implémenter ce module m'a permis de trouver énormément de bugs, trouver les bonnes requêtes à implémenter pour le microcontrôleur et encore une fois remanier le code de base pour mieux s'adapter au besoin d'un module microcontrôleur. Je trouve qu'implémenter des modules de mocking comme celui-là est très important pour le développement logiciel et ce sera une pratique que j'essaierai d'appliquer dans mes futurs projets qui demandent un certain niveau de fiabilité.

Vers la fin de la semaine, j'ai commencé finalement l'implémentation du module microcontroller-serial qui est l'interface logicielle qui permet l'interaction avec un microcontrôleur via une communication en série. L'architecture est la même que celle du microcontrôleur virtuel et la seule spécificité est qu'il doit être portable pour différentes plateformes. En effet, pour avoir accès aux interfaces de communication, il faut faire appel au système d'exploitation. Normalement, c'est abstrait par des bibliothèques de communication mais elles restent spécifiques à l'OS. Alors, il faut une architecture qui non seulement abstrait et interface avec ces bibliothèques, mais qui possède une compilation conditionnelle dépendante du système opérationnel utilisé. En révisant ce qui a déjà été dans d'autres modules du logiciel, j'ai appris comment le faire et maintenant, développer un code portable est un concept acquis pour moi.

Bien à vous,

Brenno Ferreira.