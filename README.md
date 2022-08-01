# Distribuidos_Whatsapp
Trabalho de Sistemas Distribuídos para implementação de um chat estilo Whatsapp

## Pré requisitos
Para utilizar tal programa precisa-se de um sistema com interpretador Python3 instalado. Precisa-se também da instalação da biblioteca zmq, requisito básico do trabalho. Para tal pode-se utilizar os comandos abaixo em um sistema Linux:

sudo apt install pip

pip install pyzmq

# O funcionamento do sistema

O sistema funciona apartir do uso de comandos de terminal, os comandos estão listados abaixo:

Para se tornar subscrito de um tópico, deve-se utilizar o comando:

* subscribe <tópico>, onde <tópico> deve ser o nome do tópico ao qual deseja-se ouvir as mensagens enviadas

Para o envio de mensagens em um determinado tópico deve-se usar o comando:

* create_message <tópico> <mensagem>, onde, <tópico> deve ser o nome do tópico ao qual deseja-se enviar a mensagem e <mensagem> deve ser a mensagem a ser enviada para o tópico escolhido

Para parar de ouvir um determinado tópico deve-se utilizar o comando:

* unsubscribe <tópico>, onde <tópico> deve ser o nome do tópico ao qual deseja-se parar de receber mensagens

E, finalmente, para que seja possível encerrar o programa, deve-se utilizar o comando:

* exit, sem nenhum argumento de comando

Caso qualquer um dos comandos acima receba a quantidade errada de argumentos, ou seja digitado com a grafia errada, lembrando que tais comandos são case sensitive, ou seja, receber letras maiúsculas, o usuário receberá uma mensagem de erro.

### Integrantes
<center>
Matteus Guilherme de Souza, R.A.: 769816
<br>
Fernando Kiyoshi Kayda, R.A.: 769667
</center>