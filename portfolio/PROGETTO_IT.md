# High-Dimensional Time Series: dai sensori ai modelli predittivi

**Un progetto tra statistica, machine learning e qualità dell'aria.**

Come si analizzano centinaia di serie temporali che si influenzano a vicenda? E quanto può migliorare una previsione se, oltre allo storico di un sensore, utilizziamo anche informazioni dalla rete e dalle condizioni atmosferiche?

Il lavoro nasce da un **progetto universitario di gruppo**, realizzato con **Emidio Grillo e Luca Nudo**, su 516 serie di sensori AirBox a Taiwan. Il problema era quello tipico dell'alta dimensionalità: moltissime variabili, osservazioni limitate e la necessità di regolarizzare i modelli per evitare stime instabili.

Successivamente ho approfondito il tema con un **benchmark distinto in Python** sui dati UCI di 12 stazioni a Beijing, confrontando un modello molto semplice — prevedere per l'ora successiva lo stesso PM2.5 dell'ora precedente — con modelli statistici e di machine learning.

Nel confronto retrospettivo del 2016, LightGBM con informazioni ambientali ritardate ha ottenuto un **MAE di 8,682**, contro **9,663** della persistenza: una riduzione del **10,15%** su 102.298 osservazioni stazione-ora valutabili. Anche la versione con solo PM2.5 ha migliorato la baseline.

**La parte più importante non è soltanto il numero.** Ho lavorato su separazione cronologica, variabili disponibili al momento della previsione, dati mancanti, confronto equo fra modelli e verifiche di riproducibilità. Il periodo 2016 è stato consultato più volte durante lo sviluppo: il risultato è quindi **esplorativo e non costituisce una validazione indipendente**.

**Tecnologie:** R, Python, pandas, NumPy, LightGBM, modellazione VAR regolarizzata, valutazione temporale.

[Codice e metodologia](../beijing/README.md) · [Studio Taiwan](../taiwan/README.md) · [Limiti e trasparenza](../docs/RESEARCH_INTEGRITY.md)
