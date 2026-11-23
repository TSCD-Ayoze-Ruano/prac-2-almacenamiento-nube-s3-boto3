#!/usr/bin/env python3
"""
Script de automatización con Boto3 para AWS S3 parametrizado por bucket y prefijo.
"""

import argparse
import os
import boto3
from botocore.exceptions import ClientError


def main():
    parser = argparse.ArgumentParser(
        description="Operaciones con S3 usando Boto3 parametrizado por bucket y prefijo."
    )
    parser.add_argument(
        "-b", "--bucket",
        type=str,
        default="tscd-s3-ayoze",
        help="Nombre del bucket de S3 con el que operar (por defecto: tscd-s3-ayoze)"
    )
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        default="classified_material",
        help="Prefijo/carpeta virtual dentro del bucket (por defecto: classified_material)"
    )

    args = parser.parse_args()
    bucket_name = args.bucket
    prefix = args.prefix.strip("/")

    print("=" * 60)
    print("Iniciando script S3:")
    print(f" - Bucket objetivo : {bucket_name}")
    print(f" - Prefijo objetivo: {prefix}")
    print("=" * 60)

    s3 = boto3.client("s3")
    s3r = boto3.resource("s3")

    print("\n--- [Client] Listando todos los buckets ---")
    buckets = s3.list_buckets().get("Buckets", [])
    for b in buckets:
        print(f"  • {b['Name']}")

    print("\n--- [Resource] Listando buckets orientados a objetos ---")
    for b in s3r.buckets.all():
        print(f"  • {b.name}")

    print(f"\n--- [Client] Objetos en '{bucket_name}' ---")
    resp = s3.list_objects_v2(Bucket=bucket_name)
    contents = resp.get("Contents", [])
    if contents:
        for obj in contents:
            print(f"  • {obj['Key']}")
    else:
        print("  (Bucket vacío o sin objetos en la raíz)")

    print(f"\n--- [Resource] Detalle de todos los objetos en '{bucket_name}' ---")
    bucket = s3r.Bucket(bucket_name)
    for obj in bucket.objects.all():
        print(f"  Key          : {obj.key}")
        print(f"  Tamaño (B)   : {obj.size}")
        print(f"  Modificado   : {obj.last_modified}")
        print("  " + "-" * 40)

    print(f"\n--- Operaciones de archivo bajo el prefijo '{prefix}/' ---")

    if not os.path.exists("hola.txt"):
        with open("hola.txt", "w", encoding="utf-8") as f:
            f.write("Hola desde local!\n")
    if not os.path.exists("contenido.txt"):
        with open("contenido.txt", "w", encoding="utf-8") as f:
            f.write("Contenido confidencial o de prueba.\n")

    s3_key_hola = f"{prefix}/hola.txt"
    s3_key_contenido = f"{prefix}/contenido.txt"

    print(f"  Subiendo 'hola.txt' a 's3://{bucket_name}/{s3_key_hola}'...")
    s3.upload_file("hola.txt", bucket_name, s3_key_hola)

    print(f"  Subiendo 'contenido.txt' a 's3://{bucket_name}/{s3_key_contenido}'...")
    s3.upload_file("contenido.txt", bucket_name, s3_key_contenido)

    print(f"\n--- [Comprobación] Objetos en el bucket tras la SUBIDA ---")
    resp_post_upload = s3.list_objects_v2(Bucket=bucket_name)
    for obj in resp_post_upload.get("Contents", []):
        print(f"  • {obj['Key']}")

    print(f"\n  Descargando '{s3_key_hola}' como 'hola_local.txt'...")
    s3.download_file(bucket_name, s3_key_hola, "hola_local.txt")

    print(f"  Borrando '{s3_key_hola}' de S3...")
    s3.delete_object(Bucket=bucket_name, Key=s3_key_hola)

    print(f"\n--- [Comprobación] Objetos en el bucket tras el BORRADO ---")
    resp_post_delete = s3.list_objects_v2(Bucket=bucket_name)
    for obj in resp_post_delete.get("Contents", []):
        print(f"  • {obj['Key']}")

    print(f"\n--- [Resource] Filtrando objetos por prefijo '{prefix}/' ---")
    objetos_filtrados = list(bucket.objects.filter(Prefix=f"{prefix}/"))
    if objetos_filtrados:
        for obj in objetos_filtrados:
            print(f"  • {obj.key} ({obj.size} bytes)")
    else:
        print(f"  (No se encontraron objetos con el prefijo '{prefix}/')")

    print(f"\n--- [Client] Filtrando objetos por prefijo '{prefix}/' ---")
    resp_prefix = s3.list_objects_v2(Bucket=bucket_name, Prefix=f"{prefix}/")
    contents_prefix = resp_prefix.get("Contents", [])
    if contents_prefix:
        for obj in contents_prefix:
            print(f"  • {obj['Key']}")
    else:
        print(f"  (No se encontraron objetos con el prefijo '{prefix}/')")

    print("\n--- Generando URL prefirmada (expira en 300 segundos) ---")
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": s3_key_contenido},
            ExpiresIn=300
        )
        print(f"URL de descarga:\n{url}")
    except ClientError as e:
        print(f"Error generando URL prefirmada: {e}")

    print("\n" + "=" * 60)
    print("Script completado con éxito.")
    print("=" * 60)


if __name__ == "__main__":
    main()