# Scalable Chain of Table

Dieses System ist inspiriert durch 'chain-of-table' [Quelle]. Die Idee ist es, eine Tabelle Schritt für Schritt zu verformen, um so eine Nutzungsanfrage zu beantworten.

# Einstieg

Die main.py Funktion dient als Einstiegspunkt zum Testen des Systems. Dort lassen sich alle relevanten Parameter spezifizieren: 

- Model: Aktuell werden ChatGPT und Mistral Nemo unterstützt
- Der Datensatz: Es gibt zwei Beispieldatensätze unter data. data\tabfacts.py wurde von der chain-of-table Quelle übernommen und zu einigen Einträgen Erläuterungen zu den Spalten hinzugefügt. Enthalten die Einträge keine Erläuterungen kommt es zu einem Fehler.

# Architektur

Die Agentenstruktur, um die Tabellenumformung zu erhalten, basiert auf Langgraph und ist im Ordner \graph spezifiziert.

<img src="assets/AgentArchitecture.png" alt="Übersicht der Agenetenarchitektur"/>

# Integration & Validierung

Die LLMs wurden mit <a href="https://python.useinstructor.com/">Instructor</a> modifiziert, wodurch sie strukturierte Objekte basierend auf Pydantic ausgeben können. Dadurch ist es möglich, die Ausgabe zu validieren und fehlerhaft Ausgaben an das Modell zurückzuspielen.

# Aktuelle Probleme:

Obwohl CoT funktioniert, kommt es häufig vor, dass das Modell zwar richtig argumentiert, aber dann eine falsche Antwort gibt.

## Beispiel: Richtige Argumentation, falscher Output

<i>user query: the wildcats lost one game in september and two games in november

function chain:
Selected rows based on the following conditions:
date contains september, result contains loss, record == 1, date contains november, record == 2, 

table caption : 1947 kentucky wildcats football team

col : game | date | opponent | result | wildcats points | opponents | record
row 1 : 1 | sept 20 | ole miss | loss | 7 | 14 | nan
row 2 : 7 | nov 1 | 18 alabama | loss | 0 | 13 | nan
row 3 : 10 | nov 22 | tennessee | loss | 6 | 13 | nan

evaluation output:
The user statement claims that the Wildcats lost one game in September and two games in November. However, according to the table, they lost one game in September (Ole Miss) and two games in November (Alabama and Tennessee), <b>which confirms the user's statement is true</b>. The operations selected the correct rows based on the conditions, confirming the user's claim.

<b>model evaluation: False</b></i>

## Beispiel: Bei Datumsangaben, wird nicht die Grammatik in der Tabelle berücksichtigt

Es kommt vor, dass das LLM nach "november" filtern will, obwohl die Datums-Spalte so formatiert ist: "nov 24"

<i>user query: the wildcats loss one game in november and two games in september

function chain:
Selected rows based on the following conditions:
result contains loss, date <b>contains november</b>, result contains loss, date <b>contains september</b>, 

table caption : 1947 kentucky wildcats football team
col : game | date | opponent | result | wildcats points | opponents | record
row 1 : 1 | <b>sept 20</b> | ole miss | loss | 7 | 14 | 0 - 1
row 2 : 7 | nov 1 | 18 alabama | loss | 0 | 13 | 5 - 2
row 3 : 10 | nov 22 | tennessee | loss | 6 | 13 | 7 - 3

evaluation output:
The wildcats lost only one game in November (on Nov 1 vs Alabama) and zero games in September.
model evaluation: False</i>

## Beispiel: ID-Spalten werden grundlos zum Filtern genutzt

<i>user query: the wildcats played four games in september , two games in october , and two games in november

function chain:
Selected rows based on the following conditions:

<b>game >= 3</b>, 

table caption : 1947 kentucky wildcats football team

col : game | date | opponent | result | wildcats points | opponents | record
row 1 : 3 | oct 4 | xavier | win | 20 | 7 | 2 - 1
row 2 : 4 | oct 11 | 9 georgia | win | 26 | 0 | 3 - 1 , 20
row 3 : 5 | oct 18 | 10 vanderbilt | win | 14 | 0 | 4 - 1 , 14
row 4 : 6 | oct 25 | michigan state | win | 7 | 6 | 5 - 1 , 13
row 5 : 7 | nov 1 | 18 alabama | loss | 0 | 13 | 5 - 2

evaluation output:
According to the given table, the Wildcats played only one game in September, two games in October, and one game in November.

model evaluation: False</i>