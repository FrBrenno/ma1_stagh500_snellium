# Week 5 - 12.08/16.08

19/08/2024

Bonjour Monsieur Quitin,

J'espère que vous allez bien et que vous profitez bien de vos vacances.

Voici mon rapport de la semaine 5.

Depuis une ou deux semaines, mon projet possède deux fronts: software et microcontrôleur (uC). En effet, je peux travailler séparément dans un des ces fronts sans impacter l'autre.

En début de semaine, le côté uC s'est vu bloqué car je devrais attendre l'arrivée du module USB-to-UART pour que je puisse essayer d'établir une communication en série avec l'ordinateur. Alors, je me concentrer sur le développement du logiciel qui interagira avec le uC et surtout sur son intégration avec le logiciel déjà développé par la start-up. D'abord, j'ai fait une étude de l'architecture de leur codebase et j'ai établi un schéma pour faciliter la visualisation. Le schéma est celui-ci :

![[portfolio/2 - project/documentation/Architecture/doc/microcontroller_communication_daemon_architecture-v1.pdf|microcontroller_communication_daemon_architecture-v1]]

En général, l'architecture est modulaire avec un module core responsable des fonctionnalités de base. Les autres modules sont implémentés en deux fois : premièrement on définit l'interface et les fonctionnalités de base du module, ainsi que certains objets nécessaires pour son utilisation ; ensuite, on implémente le module en lui-même. En ce qui concerne mon module, chaque implémentation de l'interface va définir un nouveau type de communication, que ce soit en série, Ethernet ou wifi. 

C'était une expérience assez intéressante et instructive de découvrir l'architecture et de pouvoir en discuter avec mon maître de stage, qui a été le développeur.

Alors avant de faire ma propre implémentation, je suis parti à la recherche des librairies qui me permettrait de monitorer des ports et d'établir une communication en série. Pour la communication en série, la librairie boostasio s'en charge de tout et elle est même portable à différentes plateformes. Pour le port monitoring, c'était un peu moins évident car cette tâche est dépendante de l'OS. Au final, pour linux la libraires libsystemd possède une API qui permet d'exécuter cette tâche. Pour Windows, l'API s'appelle SetupAPI.

Vers la fin de la semaine, le module USB-to-UART est arrivé. De ce fait, je me suis mis à programmer le uC afin de tester ce module et d'avoir un exemple de code par après. Comme toujours, coder le uC que j'ai choisi était une tâche longue et difficile car je ne savais pas où chercher ce que je ne voulais ni comment configurer et programmer les composants. Au final, j'ai réussi à tout faire et j'ai compris que le module USB-to-UART est un gros élément d'accélération du développement. L'API pour le SCI est très simple and m'a permis d'implémenter et tester très vite. Par contre, de sa simplicité, il a fallu trouver comment bien recevoir le message car j'avais des problèmes de null-terminators que n'était pas correctement placé ou des buffers trop petits. Bref, j'ai dû trouver par essai-et-erreur découvrir comment établir une communication fiable.

Une chose qu'a difficulté la majorité des mes tâches cette semaine est le manque de documentation des librairies, que ce soit libsystemd ou que ce soit celle de SCI de Renesas. Elles étaient soit incomplète, soit inexistante. Du coup, je reviens encore une fois dire que la documentation doit être un élément crucial dans le choix de design car le temps de développement est très fortement impacté par cela. 

Voilà ce que j'ai accompli cette semaine.

Bien à vous,

Brenno Ferreira.