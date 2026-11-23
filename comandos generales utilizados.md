## Comandos utilizados

### Crear y consultar buckets

```bash
aws s3api create-bucket --bucket $BUCKET --create-bucket-configuration LocationConstraint=us-west-2 --region us-west-2
```
```bash
aws s3 ls
aws s3 ls s3://$BUCKET
```

### Subir objetos
```bash
aws s3 cp hola.txt s3://$BUCKET/hogar/hola.txt
aws s3 sync datos/ s3://$BUCKET/datos/
```

### Descargar objetos
```bash
aws s3 cp s3://$BUCKET/hogar/hola.txt hola_descargado.txt
```

### Eliminar objetos
```bash
aws s3 rm s3://$BUCKET/hogar/hola.txt
```

### Versionado
```bash
aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Enabled
```
```bash
aws s3api list-object-versions --bucket $BUCKET
aws s3api list-object-versions --bucket $BUCKET --prefix hogar/hola.txt
```
```bash
aws s3api get-object --bucket $BUCKET --key hogar/hola.txt --version-id <VERSION_ID> hola_version_antigua.txt
```
```bash
aws s3api delete-object --bucket $BUCKET --key hogar/hola.txt --version-id <VERSION_ID>
```

### Limpieza de recursos
```bash 
aws s3 rm s3://$BUCKET --recursive
```
```bash
aws s3api delete-bucket --bucket $BUCKET --region us-west-2
```


Esto cubre específicamente **crear, listar, subir, descargar y eliminar objetos**, además de incluir las operaciones de **versionado y limpieza** que también forman parte del desarrollo de la práctica.