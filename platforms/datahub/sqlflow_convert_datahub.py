import json
import sys

from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import (
    UpstreamLineageClass,
    UpstreamClass,
    DatasetPropertiesClass,
    ChangeTypeClass,
)
from datahub.emitter.mcp import MetadataChangeProposalWrapper

# datahub server host
emitter = DatahubRestEmitter("http://localhost:8080")


def build_dataset_urn(table_name):
    table_name = table_name.lower()
    return f"urn:li:dataset:(urn:li:dataPlatform:oracle,{table_name},PROD)"


def main(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    relationships = data["data"]["sqlflow"]["relationships"]

    created_tables = set()

    for rel in relationships:
        target_table = rel["target"]["parentName"]

        for src in rel["sources"]:
            source_table = src["parentName"]

            source_urn = build_dataset_urn(source_table)
            target_urn = build_dataset_urn(target_table)

            # 1️⃣ 创建 source dataset（避免页面不显示）
            if source_table not in created_tables:
                mcp_source = MetadataChangeProposalWrapper(
                    entityUrn=source_urn,
                    entityType="dataset",
                    aspect=DatasetPropertiesClass(
                        description="Imported from sqlflow"
                    ),
                    aspectName="datasetProperties",
                    changeType=ChangeTypeClass.UPSERT,
                )
                emitter.emit(mcp_source)
                created_tables.add(source_table)

            # 2️⃣ 创建 target dataset
            if target_table not in created_tables:
                mcp_target = MetadataChangeProposalWrapper(
                    entityUrn=target_urn,
                    entityType="dataset",
                    aspect=DatasetPropertiesClass(
                        description="Imported from sqlflow"
                    ),
                    aspectName="datasetProperties",
                    changeType=ChangeTypeClass.UPSERT,
                )
                emitter.emit(mcp_target)
                created_tables.add(target_table)

            # 3️⃣ 建立血缘（source -> target）
            lineage = UpstreamLineageClass(
                upstreams=[
                    UpstreamClass(
                        dataset=source_urn,
                        type="TRANSFORMED",
                    )
                ]
            )

            mcp_lineage = MetadataChangeProposalWrapper(
                entityUrn=target_urn,
                entityType="dataset",
                aspect=lineage,
                aspectName="upstreamLineage",
                changeType=ChangeTypeClass.UPSERT,
            )

            emitter.emit(mcp_lineage)

    print("Lineage uploaded successfully!")


if __name__ == "__main__":
    main(sys.argv[1])
