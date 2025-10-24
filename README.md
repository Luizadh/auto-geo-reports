# Projeto Python + React + GIS 🗺️


## 🎯 Objetivo do Projeto

Este projeto tem como objetivo automatizar a extração e integração de informações geoespaciais de diferentes bancos de dados(Oracle, PostGIS), arquivos GPKG e TIFF, que antes só eram acessíveis via **QGIS**, um software livre de Sistema de Informação Geográfica (GIS) usado para visualizar, editar e analisar mapas e camadas geográficas, exigindo consultas manuais.

## 🌐 Contexto
No **Instituto de Pesquisa e Planejamento** da cidade, arquitetos e engenheiros recebem solicitações de outros órgãos públicos que desejam informações cadastrais e espaciais de imóveis ou lotes para diversos fins administrativos. Anteriormente, o processo de resposta envolvia localizar manualmente o imóvel no QGIS, selecionar e destacar o lote desejado, gerar cortes por print da imagem de drone da cidade, copiar informações cadastrais e colar manualmente em relatórios em PDF, o que era massante e propenso a erros, especialmente sob alta demanda.

A solução desenvolvida elimina todo o trabalho manual. O usuário informa o número de inscrição do imóvel, os dados são extraídos diretamente das fontes, as geometrias são processadas e alinhadas automaticamente, e o relatório em PDF é gerado completo, com os dados desejados do imóvel, lote principal destacado, lotes vizinhos contornados e a localização na imagem de drone da cidade, no layout oficial do Instituto pronto para uso.

## ⚙️ Tecnologias Principais

**Backend:** Python (`FastAPI`, `Geopandas`, `Shapely`, `Matplotlib`, `Rasterio`, `ReportLab`, `Pillow`, `Oracledb`, `Psycopg2`)  
**Frontend:** React + Axios  
**Banco de dados:** Oracle e PostGIS  
**GIS:** QGIS + PyQGIS para validação e testes  


## 🗂️ Fontes de dados utilizadas:

- **Oracle** → informações cadastrais de todos os imóveis da cidade

- **PostGIS** → geometrias georreferenciadas dos lotes (MULTIPOLYGON)

- **GPKG** → camada de referência com geometrias de todos os lotes para alinhamento com raster

- **TIFF** → arquivo raster com a imagem de drone da cidade


## ▶️ Instalação e execução (uso interno)

> ⚠️ Este projeto depende de bancos de dados corporativos (Oracle, PostGIS) e arquivos geoespaciais (.GPKG, .TIFF) disponíveis apenas no ambiente interno do Instituto.
> 
> As instruções abaixo ilustram o processo de execução em ambiente interno.

**Pré-requisitos:**

Python >= 3.x

Node.js >= 16.x 

QGIS >= 3.16.0-Hannover (visualização e validação)

**Executar backend localmente:**
```bash

# Instalar as dependências do projeto
cd backend
pip install -r requirements.txt

# Configure as variáveis de ambiente no arquivo .env

# Execute o backend:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Executar frontend localmente**
```bash
#Instalar dependências React e executar:
cd frontend
npm install
npm start
```

**Build para produção**
```bash
npm run build
```
> Isso gera a pasta build/, deve ser colocada no servidor web (como Apache/XAMPP) para servir o frontend


**Acesse o sistema:**
> No próprio servidor: http://localhost:3000
> Em outros computadores na rede: http://< IP-do-servidor >:3000


## Upgrades Futuros
Interface mais completa, mais filtros de análise


## Referências

1. [Python Documentation](https://docs.python.org/3/)
2. [PyQGIS Documentation](https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/)
3. [Oracle Python Driver (python-oracledb / cx_Oracle)](https://python-oracledb.readthedocs.io/en/latest/)
4. [PostGIS Documentation](https://postgis.net/documentation/)
5. [ReportLab (PDF Generation)](https://www.reportlab.com/docs/)
6. [FastAPI Documentation](https://fastapi.tiangolo.com/)
7. [React Documentation](https://react.dev/)
8. [Rasterio Documentation](https://rasterio.readthedocs.io/en/latest/)
9. [GeoPandas Documentation](https://geopandas.org/en/stable/)
10. [Shapely Documentation](https://shapely.readthedocs.io/en/stable/)
11. [NumPy Documentation](https://numpy.org/doc/)
12. [Uvicorn Documentation](https://www.uvicorn.org/)
13. [Flaticon](https://www.flaticon.com/)
14. [Pandas Documentation](https://pandas.pydata.org/docs/)
15. [Pillow Documentation](https://pillow.readthedocs.io/)
16. [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
17. [GeoPackage Format Documentation](https://www.geopackage.org/)


