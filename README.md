# MinIO Tools

Script para gerenciar a criação de buckets, policies, usuario e acessos ao S3 MinIO instalado standalone MinIO server localmente para teste (debian) e MinIO Client. 

Projeto baseado na documentação https://min.io/docs/minio/linux/index.html e tutoriais https://www.youtube.com/@MINIO

### Pré-requisitos

Instalar o Standalone MinIO Server:

    wget https://dl.min.io/server/minio/release/linux-amd64/archive/minio_20230407052858.0.0_amd64.deb -O minio.deb

    sudo dpkg -i minio.deb

Criar diretório para MinIO armazenar arquivos:

    mkdir ~/minio

    minio server ~/minio --console-address :9090

Saída:

    WARNING: Detected default credentials 'minioadmin:minioadmin', we recommend that you change these values with 'MINIO_ROOT_USER' and 'MINIO_ROOT_PASSWORD' environment variables
    MinIO Object Storage Server
    Copyright: 2015-2023 MinIO, Inc.
    License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl-3.0.html>
    Version: RELEASE.2023-04-07T05-28-58Z (go1.20.3 linux/amd64)

    Status:         1 Online, 0 Offline. 
    API: http://192.168.0.10:9000  http://127.0.0.1:9000       
    RootUser: minioadmin 
    RootPass: minioadmin 
    Console: http://192.168.0.10:9090 http://127.0.0.1:9090    
    RootUser: minioadmin 
    RootPass: minioadmin 

    Command-line: https://min.io/docs/minio/linux/reference/minio-mc.html#quickstart
       $ mc alias set myminio http://192.168.0.10:9000 minioadmin minioadmin

    Documentation: https://min.io/docs/minio/linux/index.html
    Warning: The standard parity is set to 0. This can lead to data loss.

Para conectar seu browser ao MinIO:

    192.168.seu.ip:9090

Para conferir se tudo está funcionando:

Entre com seu usuario e senha e crie um bucket, suba um arquivo nesse bucket.

    Ctrl + C para sair

Para ver o bucket: 

    ls -lah minio 

Para ver o que está dentro do bucket:

    ls -lah minio/my-test-bucket


Instalar o MinIO Client para o Server usando CLI:

Rodar o MinIO Server em segundo plano: 

    minio server ~/minio --console-address :9090 > /dev/null 2>&1 &

Para sair do segundo plano: 
    
    fg

Baixar e instalar no PATH ou rodar binário do ponto de download:

    wget https://dl.min.io/client/mc/release/linux-amd64/mc
    chmod +x mc
    sudo mv mc /usr/local/bin/mc

Use mc alias set para criar um alias associado ao deployment local. Rode os comandos mc usando o alias:

    mc alias set local http://192.168.0.7:9000 minioadmin minioadmin
    mc admin info local

O alias mc aceita quatro argumentos:

name of the alias
hostname ou IP address e porta do MinIO server
Access Key do MinIO user
Secret Key do MinIO user

Ver arquivos localizados aqui usando: 

    mc ls -r

### Comandos do MinIO Client

O comando mc alias é usado para adicionar ou remover os endereços dos servidores que hospedam os dados do objeto S3 compatível e que o cliente MinIO pode se conectar para acessar ou gerenciar.

O comando mc alias tem três opções:

    mc alias set # configurar (adicionar ou atualizar)

    mc alias set myminio https://myminio.ip.address.net:9000 minioadmin miniopasswd

    mc alias list # lista todos os meus aliases, output inclui access e secret key de cada 

    mc alias remove # limpar lista 

O comando mc mb cria novos buckets ou diretório em um path determinado

    mc mb ~/localdir/outrodir

    mc mb minio/meubucket1

    mc mb amazon-s3/meu-bucket-teste

O comando mc rb remove um ou mais buckets (para remover o conteúdo do bucket, use mc rm). Este comando remove permanentemente todo o conteúdo e versionamento do bucket.

    mc rb ~/localdir # remove diretório local

    mc rb --force minio/meubucket # remove bucket especificado

    mc rb --force --dangerous minio/ # remove todos os bucket no alias minio

O comando mc ls lista buckets e objetos no MinIO ou outros serviços compatíveis com S3. Você também pode usar mc ls no seu filesystem local para produzir resultados parecidos com o comando ls.

Listar todos os buckets no diretorio local

    mc ls ~

Listar todos os bucket usando o alias

    mc ls minio

Listar todos os bucket no alias de forma recursiva

    mc ls -r minio

Listar um bucket específico de forma recursiva

    mc ls -r minio/testbucket1

Listar arquivos zipados dentro de um bucket específico

    mc ls minio/testbucket/zip_test.zip --zip

Listar buckets usando mais de um alias ao mesmo tempo

    mc ls minio1/testbucket1 minio2/testbucket2

O comando mc cp copia arquivos e diretórios de um local para outro.

Copia arquivo localmente

    mc cp arq1.txt arq2.txt

Copia o arquivo local para dentro do bucket especificado no cluster minio (alias)

    mc cp ~/arq1.txt minio/meubucket/arq1.txt

Copia o arquivo de um bucket em um cluster para outro bucket, em outro cluster

    mc cp minio1/bucket1/arq1.txt minio2/bucket2/arq1.txt