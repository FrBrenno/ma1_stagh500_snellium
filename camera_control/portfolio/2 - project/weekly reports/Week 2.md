29/07/2024

Bonjour Monsieur Quitin,

J'espère que vous allez bien et que vous profitez des vos vacances !

Je ferai mes rapports dorénavant en Français. 

En ce qui concerne la visite de mi-parcours, il y a un autre étudiant de polytech qui fait son stage chez Snellium et on s'est dit que nous pourrions organiser la visite au même temps. Il en a déjà parlé avec son superviseur et Cédric Boey pour faire la visite le 16 septembre à 10h. Si cela semble possible pour vous, je le contacterai pour avoir plus de détails.

Rapport:

Cette semaine était une semaine de 4 jours de travail car nous avons eu le congé de la Fête National le vendredi 26/07. En début de semaine, j'ai passé commande du microcontrôleur et des composants que j'ai soigneusement choisi la semaine passée. J'ai pris un board de développement du microcontrôleur RX65N de la société Resenas et quelques pins, sockets et screw headers dont j'aurai peut-être besoin pour mettre en place le système.  Le prix total de la commande n'a pas dépassé le 40€. Je suis assez fier de mon choix car ce microcontrôleur répond à tous les critères techniques que nous avions définis mais j'ai quand-même des craintes à propos de l'environnement de développement, car l'IDE pour ce microcontrôleur est propriétaire et je ne sais pas si j'aurai un environnement assez riche en bibliothèque. Au pire des cas, j'aurai besoin de coder certaines librairies moi-même et j'aurai peu plus du mal à debugger.

Une fois la commande faite, mon maître de stage m'a fourni un clone d'Arduino UNO pour que je puisse commencer à jongler avec l'environnement et à esquisser le système qui sera mis en place. La chose la plus important que je dois implémenter en ce moment est le **protocole de communication** entre l'ordinateur et le microcontrôleur, ainsi le microcontrôleur en recevant les commandes venant du logiciel via communication en série (USB), pourra effectuer les tâches demandées.

Du côté PC, dans le but de développer rapidement, j'ai créé un script python en utilisant la bibliothèque pyserial qui se communiquera avec le microcontrôleur. Ce script sera l''interface de communication entre le logiciel existant et le uC (microcontrôleur). Il contient un objet uC_serialCommunication qui permet de scanner les ports, trouver le uC, établir la communication et s'en occupera de transmettre les commandes. Une fois toutes les fonctionnalités testées et l'architecture validée, ce script sera traduit en C++ avec une bibliothèque équivalente et va intégrer le logiciel de la société. 

Les commandes doivent pouvoir prendre des options et des arguments. Également, il faut que le protocole soit extensible pour supporter des fonctionnalités qui viendront dans des futurs projets. J'ai établi une grammaire similaire à celle de bash linux et les commandes sont encapsulées dans leurs propres classes. La classe commande s'en occupera de la récupériation des données comme l'option et les arguments mais aussi de la sérialisation de toutes ces données avant de transmettre le string nécessaire au uC. Voici la grammaire et des exemples de command qu'on pourra passer et leurs sérialisation :

**GRAMMAIRE: rien de très formel pour le moment**

COMMAND -OPTION ARG1 ARG2       ----- sérialisé en -------> || command-opt | nb_args - arg1 - arg2 - ... ||

COMMAND     info        Obtenir des informations sur le uC

                ping        Vérifier la communication avec le uC en le demandant de répondre à un msg

                   trigger      Envoyer signal de trigger sur toutes les caméras

                help         Aide avec les commandes

OPTION        info            custom_name, board, uC ID, mcu_type    

                trigger                selective                              

                help             info, ping, trigger

                ping

ARG           [a-zA-Z0-9]+    

**EXEMPLES:**

PING                                ----- sérialisé en -------> ||ping||

INFO device-name                    ----- sérialisé en -------> ||info|1-device_name||

TRIGGER -SELECTIVE cam_1 cam_4         ----- sérialisé en -------> ||trigger-selective|2-cam_1-cam_4||

Avec une telle grammaire, les commandes peuvent être plus puissantes car on donne la possibilité d'implémenter des options et d'introduire différents arguments. L'objectif est de rester le plus simple et compact possible mais faire une communication permettant beaucoup des fonctionnalités.

Alors, du côté uC, il va recevoir le string sérialisé de la commande et il faudra le désérialiser pour pouvoir l'exécuter correctement.  C'est là que j'ai passée toute ma semaine, en essayant d'implémenter un deserializer/parser qui pourra lire ces commandes.

Dans le but d'avoir des tests automatisés, j'ai créé un autre script python qui effectue plein des commandes dont la réponse est connue afin de tester que la communication fonctionne telle quelle. Ce script compare donc la réponse reçue avec la réponse attendue et signale quelle commande n'a fonctionné. Ceci me permet de retrouver des bugs dans le deserializer/parser de manière très efficace et précise car je sais où chercher l'erreur en regardant quelle commande n'a pas réussi le test.

Pour l'instant, ma seule crainte est que le système soit lent à cause de la communication en série et à cause du parsing des commandes. En effet, en regardant sur WireShark le temps de transmission de la commande et sa réponse, on voit que cela prendre environ 1.10 secondes. Par contre, avant de tirer mes conclusions sur le temps d'exécution et d'essayer de l'optimiser, je dois finir l'implémentation et tester la communication telle qu'elle est définie maintenant. 

Voilà ce que j'ai fait cette semaine.