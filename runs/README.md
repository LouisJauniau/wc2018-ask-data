# Runs enregistrés

Chaque dossier contient tout ce qu'il faut pour relire ou renoter un run :

| Fichier | Contenu |
|---|---|
| `config.json` | modèle, variante du prompt, mode, empreintes du jeu et du prompt |
| `prompt.txt` | le prompt système exact |
| `traces.jsonl` | ce que le modèle a fait, question par question |
| `notes.jsonl` | la notation de chaque trace |
| `rapport.md` | la synthèse et le détail des échecs |
| `reponses_rejouees.jsonl` | pour un run rejoué : les réponses brutes du modèle |

`python -m askdata noter runs/<dossier>` renote un run à partir de ses
traces, sans rappeler le modèle : à faire après toute correction du
comparateur ou d'une référence.

## Provenance des vagues 1 et 2

L'environnement où ce projet a été construit n'avait pas de clé d'API
valide. Les deux vagues ont donc été produites hors harnais, puis notées par
lui :

- **Modèles** : Claude Haiku et Claude Sonnet, lancés comme sous-agents
  Claude Code sous les alias `haiku` et `sonnet`. La version exacte servie
  n'est pas exposée par cet outil ; les runs sont étiquetés
  `haiku-sous-agent` et `sonnet-sous-agent` pour ne pas l'inventer.
- **Mode** : `direct` seulement (une requête, sans pouvoir l'exécuter). Le
  mode agent demande une boucle d'outils que seul l'accès à l'API permet.
- **Protocole** : chaque sous-agent recevait un seul fichier, le lot produit
  par `python -m askdata lot` (archivé dans `lots/`), et devait écrire ses
  réponses dans un seul fichier, sans lire quoi que ce soit d'autre. Les
  journaux des sous-agents ont été vérifiés après coup : chacun a fait
  exactement une lecture (son lot) et une écriture (sa sortie), aucun n'a
  ouvert le jeu de questions, les références ou le dictionnaire.
- **Lots** : un lot par split (34 questions dev, 32 test), questions
  mélangées, identifiants opaques, catégories non montrées. Les paires de
  questions qui se renseignent l'une l'autre (« Eden Hazard » et « Hazard »,
  « buts de la France » et « buts de la France en 2022 ») sont dans des
  splits différents.
- **Format** : en vague 1, le lot ne montrait pas le schéma de l'outil
  repondre, donc pas les valeurs permises de `statut`. Tous les modèles ont
  écrit `"ok"` ou `"success"` au lieu de `"reponse"`. Le fournisseur rejeu
  lit un statut inconnu accompagné d'une requête comme `"reponse"` et compte
  chaque correction (voir chaque `rapport.md`). En vague 2, le lot inclut le
  schéma.
- **Graine du mélange** : 0 en vague 1, 1 en vague 2.
- **Vague 2** : Haiku seulement. Sonnet obtient 52 sur 52 dans les trois
  configurations de la vague 1 ; le relancer n'apprendrait rien sur la
  variance, le jeu étant saturé pour lui.

Ces runs mesurent donc la génération de SQL en un coup, à partir d'un
prompt identique à celui de l'API, mais pas l'agent complet.

## Runs de l'agent

`opus_agent_documente_dev`, `opus_agent_documente_test` et
`haiku_agent_documente` ont été produits par le harnais lui-même, en mode
agent, par l'API Anthropic (`claude-opus-5-5` avec un effort `medium`,
`claude-haiku-4-5`), questions appelées une par une, quatre en parallèle.
Le split test d'Opus a tourné une seule fois, après le split dev, sans
modification du prompt entre les deux.

Deux verdicts du comparateur sur ces runs ont été corrigés à la main : voir
`evals/arbitrages.toml` et la section « Verdicts corrigés à la main » des
rapports concernés.
