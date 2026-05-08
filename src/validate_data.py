import pandas as pd
from sqlalchemy import create_engine
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest

print("Carregando dados...")
engine = create_engine('postgresql://postgres:123@localhost:5434/lab01b')
df = pd.read_sql_table('spotify_tracks', engine, schema='raw')
print(f"✅ {len(df)} linhas carregadas")

# Contexto
context = gx.get_context()

# Datasource pandas
datasource_config = {
    "name": "pandas_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "PandasExecutionEngine"
    },
    "data_connectors": {
        "runtime_data_connector": {
            "class_name": "RuntimeDataConnector",
            "batch_identifiers": ["batch_id"]
        }
    }
}

context.add_datasource(**datasource_config)

# Batch request
batch_request = RuntimeBatchRequest(
    datasource_name="pandas_datasource",
    data_connector_name="runtime_data_connector",
    data_asset_name="spotify_tracks",
    runtime_parameters={"batch_data": df},
    batch_identifiers={"batch_id": "default_batch"}
)

# Suite
suite_name = "spotify_suite"
context.add_or_update_expectation_suite(suite_name)

# Validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=suite_name
)

# Expectations
print("\nCriando expectations...")
validator.expect_column_values_to_not_be_null("track_id")
validator.expect_column_values_to_be_between("popularity", 0, 100)
validator.expect_column_values_to_be_between("year", 1900, 2025)
validator.expect_column_values_to_be_between("danceability", 0, 1)
validator.expect_column_values_to_be_between("energy", 0, 1)
validator.expect_column_values_to_not_be_null("artist_name")

validator.save_expectation_suite()

# Validar
results = validator.validate()

print(f"\n{'✅' if results['success'] else '❌'} Validação: {'PASSOU' if results['success'] else 'FALHOU'}")
print(f"Expectations: {len(results['results'])}")
print(f"Sucessos: {sum(1 for r in results['results'] if r['success'])}")

# Data docs
context.build_data_docs()
print("\n📊 Relatório: great_expectations/uncommitted/data_docs/local_site/index.html")