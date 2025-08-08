### ESDB3 - At1

---

Em um sistema distribuído, as garantias de entrega de mensagens são cruciais para assegurar a comunicação confiável entre os componentes. Considere um sistema de fila de mensagens que suporta três diferentes semânticas de entrega: entrega pelo menos uma vez, entrega exatamente uma vez e entrega no máximo uma vez.

- _At-Least-Once-Delivery_: As mensagens são entregues uma ou mais vezes.
- _Exactly-Once-Delivery_: As mensagens são entregues exatamente uma vez.
- _At-Most-Once-Delivery_: As mensagens são entregues zero ou uma vez.

**a.** Descreva um cenário onde cada uma dessas garantias de entrega seria apropriada. Para cada cenário, explique por que a garantia de entrega específica é necessária.

**b**. Explique os potenciais desafios e trade-offs associados à implementação de entrega exatamente uma vez em um sistema distribuído. Como esses desafios se comparam com aqueles da entrega pelo menos uma vez e entrega no máximo uma vez?

**c**. Considere um sistema distribuído onde mensagens são processadas por uma fila e um serviço de tasks. Como você desenharia um fluxo de trabalho de processamento de mensagens para alcançar a entrega pelo menos uma vez? Que mecanismos você implementaria para lidar com potenciais duplicatas de mensagens?

**d**. Se o sistema mudasse de entrega pelo menos uma vez para entrega exatamente uma vez, que mudanças seriam necessárias no fluxo de trabalho de processamento de mensagens? Discuta quaisquer potenciais mecanismos ou componentes/protocolos adicionais que possam ser necessários.
