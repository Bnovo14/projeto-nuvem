import json
import boto3
from decimal import Decimal

# Inicializa o cliente do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Movies')  # Substitua 'Movies' pelo nome real da sua tabela

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Conta o número total de itens na tabela
        response = table.scan(
            Select='COUNT'
        )
        
        total_movies = response['Count']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Para permitir CORS
            },
            'body': json.dumps({
                'total_movies': total_movies,
                'message': 'Total de filmes encontrados com sucesso'
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Erro ao contar o número de filmes'
            })
        }