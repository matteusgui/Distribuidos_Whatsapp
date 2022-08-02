# Distribuidos_Whatsapp
Trabalho de Sistemas Distribuídos para implementação de um chat estilo Whatsapp

## Pré requisitos
Para utilizar tal programa precisa-se de um sistema com interpretador Python3 instalado. Precisa-se também da instalação da biblioteca zmq, requisito básico do trabalho. Para tal pode-se utilizar os comandos abaixo em um sistema Linux:

1. sudo apt install pip

2. pip install pyzmq

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

Para rodar o programa devemos abrir no mínimo 3 terminais, 2 para clientes e 1 para o broker, pois como será melhor detalhado abaixo, o grupo não foi capaz de fazer a comunicação entre 2 ou mais máquinas.

# Resultado

O grupo conseguiu realizar a implementação do sistema de comunicação, utilizando a biblioteca pyzmq, de modo que na mesma máquina fosse possível realizar a comunicação entre diferentes programas, que se comunicavam com o broker de mensagens, responsável por fazer o encaminhamento das mensagens para as devidas filas de cada tópico.

O grupo porém não conseguiu, em diversas configurações, utilizando, ou não, a rede eduroam da UFSCar e/ou os computadores dos laboratórios do Departamento de Computação, fazer com que o sistema se comunicasse entre diferentes máquinas.

### Integrantes
<center>
Matteus Guilherme de Souza, R.A.: 769816
<br>
Fernando Kiyoshi Kayda, R.A.: 769667
</center>