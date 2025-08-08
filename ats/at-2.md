### ESDB3 - At2

---

#### Contexto:

Durante a primeira aula do módulo 2, vimos algumas estruturas e maneiras de criar/atualizar/invalidar um cache. Durante a aula foi feito um sistema com cache utilizando o redis implementado com escrita _write-through_, você deve implementar um sistema com cache em escrita _write-back_. Utilize uma maneira assíncrona para a atualização. De forma que a escrita seja o mais rápida possível.

#### Objetivo:

- Implementar um sistema de cache utilizando o método de escrita _write-back_.
- A atualização deve ser feita de forma assíncrona, garantindo que a escrita seja a mais rápida possível.

#### Ambiente:

- (Preferencialmente) utilize Docker para rodar os bancos-de-dados, configurando o ambiente com Docker Compose.

#### Instruções Adicionais:

- O disparo assíncrono pode ocorrer da maneira que achar melhor, porém lembre-se de condições de corrida: O que ocorre caso haja duas escritas de um mesmo dado muito próxima uma da outra? Há certeza de que a última será mantida? Lembre-se que filas (distribuídas ou não) junto com mutexes/locks/semáforos podem ajudar com estes casos.
- Certifique-se de documentar seu código de forma clara.
- Explique no arquivo `.pdf` como seu sistema lida com as condições de corrida e a integridade de dados. Seu arquivo `.pdf` deve abordar a lógica da implementação, as limitações do método de escrita _write-back_.
- Forneça 2 exemplos (apenas rápida explicação em um parágrafo já está suficiente), um de um momento que **não é** ideal utilizar _write-back_ e um onde **é** de interesse utilizar _write-back_.

Caso queira, sinta-se à vontade para utilizar o dataset visto em aula:

https://github.com/lerocha/chinook-database
