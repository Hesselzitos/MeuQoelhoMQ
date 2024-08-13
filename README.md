# MeuQoelhoMQ
Serviço de mensageria feito em casa

## Requisitos

- Toda a comunicação entre o servidor e os seus clientes (sejam produ
  tores ou consumidores) deve ser feita utilizando gRPC sobre Protocol
  Buffers.
- Você é responsável por definir o seu próprio protocolo de comunicação
  (usando um ou mais arquivos .proto).
- O seu servidor deve ter suporte a:
  - Criação de canais/filas de mensagens identificadas por nome 
  - Remoção de canais/filas de mensagens identificadas por nome
  - Listagem dos canais disponíveis incluindo o seu tipo e o número de mensagens pendentes de entrega
- Publicação de novas mensagens em uma fila especificada pelo seu nome. O conteúdo dessas mensagens pode ser um texto ou
uma sequência de bytes de tamanho arbitrário.
- Assinatura de canais para recebimento das mensagens publicadas.
- Salvamento das mensagens em disco para que, em caso de falha de energia por exemplo, o servidor seja capaz de retomar 
a execução com as mensagens das filas intactas.

Mais detalhes em [enunciado projeto 1](http://professor.ufabc.edu.br/~e.francesquini/2024.q2.sd/#org93aca30).

## Tests
- cd python/src
- python ../test/MeuCoelhoMQTest.py 