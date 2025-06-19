import requests
import pandas as pd

# Configurações
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mzg2NiwiZW1haWwiOiJjamNvdXRpbmhvQGdtYWlsLmNvbSIsInJvbGUiOiJVIiwiaWF0IjoxNzUwMzQzMDEwLCJleHAiOjE3NTAzNDY2MTB9.CHOCGkeuKTbnHldIKr2fvJjeiJcNZWf6jaGTR2fqdOk'
BASE_URL = 'https://api-service.fogocruzado.org.br/api/v2/occurrences'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}'
}


# Função para buscar os incidentes de tiroteio no Rio de Janeiro
def fetch_incidents_rj():
    incidents = []
    page = 1
    victimTypes = {}
    types = {}
    reasons = {}
    while True:
        params = {
            'order': 'ASC',
            'page': page,
            'take': 500,
            'idState': 'b112ffbe-17b3-4ad0-8f2a-2038745d1d14',  # ID do estado do Rio de Janeiro
            'idCities': 'd1bf56cc-6d85-4e6a-a5f5-0ab3f4074be3',  # ID da cidade do Rio de Janeiro
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f'Erro {response.status_code}:', response.text)
            break

        data = response.json()
        pageMeta = data.get('pageMeta', {})
        results = data.get('data', [])
        if not results:
            print('Nenhum incidente encontrado.')
            break

        for incident in results:
            contextInfo = incident.get('contextInfo', {})
            mainReason = contextInfo.get('mainReason', {})
            reason = mainReason.get('name', 'Desconhecido')
            if reason not in reasons:
                reasons[reason] = 0
            reasons[reason] += 1

            victims = incident.get('victims', [])
            for victim in victims:
                victimType = victim.get('personType', 'Desconhecido')
                type = victim.get('type', 'Desconhecido')
                if victimType not in victimTypes:
                    victimTypes[victimType] = 0
                victimTypes[victimType] += 1
                if type not in types:
                    types[type] = 0
                types[type] += 1

        incidents.extend(results)
        print(f'Página {page}. Total: {len(incidents)}')
        if not pageMeta.get('hasNextPage'):
            break
        page += 1
    return incidents, types, victimTypes, reasons


# Executa a função e salva os dados
dados, types, victimTypes, reasons = fetch_incidents_rj()
df = pd.DataFrame(dados)
df.to_csv('tiroteios_RJ.csv', index=False, encoding='utf-8-sig')
df = pd.DataFrame(types.keys())
df.to_csv('tipos.csv', index=False, encoding='utf-8-sig')
df = pd.DataFrame(victimTypes.keys())
df.to_csv('tipos_vitimas.csv', index=False, encoding='utf-8-sig')
df = pd.DataFrame(reasons.keys())
df.to_csv('razoes.csv', index=False, encoding='utf-8-sig')

print(f'{len(df)} registros salvos em "tiroteios_RJ.csv"')